# -*- coding: UTF-8 -*-

from flask import render_template, flash, redirect, g, session, url_for
from flask import request
from . import app, lm, oid, db, babel
from .forms import LoginForm, EditForm, PostForm, SeachForm
from .models import User, Post
from flask.ext.login import login_user, current_user, login_required, logout_user
from flask.ext.babel import gettext
from flask.ext.sqlalchemy import get_debug_queries
from datetime import datetime
from .emails import follower_notification


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(),
                    author=g.user)
        db.session.add(post)
        db.session.commit()
        flash(gettext('Your post is now live!'))
        return redirect(url_for('index'))
    posts = g.user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html', title=gettext('Home'),
                           form=form, posts=posts)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SeachForm()
    g.locale = get_locale()


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config['DATABASE_QUERY_TIMEOUT']:
            app.logger.warning('''
            SLOW QUERY: {}
            Parameters: {}
            Duration: {}
            Context: {}
            '''.format(query.statement, query.parameters,
                       query.duration, query.context))
    return response


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', title=gettext('Sign In'), form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@oid.after_login
def after_login(resp):
    if not resp.email:
        flash(gettext('Invalid login. Please try again.'))
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if not user:
        nickname = resp.nickname
        if not nickname:
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    # make the user follow him/herself
    if not user.is_following(user):
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = session.get('remember_me', False)
    session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        flash(gettext('User %(nickname)s not found.', nickname=nickname))
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.errorhandler(404)
def notfound_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User %(nickname)s not found.', nickname=nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t follow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash(gettext('Cannot follow %(nickname)s', nickname=nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You are now following %(nickname)s', nickname=nickname))
    follower_notification(followed=user, follower=g.user)
    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User %(nickname)s not found.', nickname=nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t unfollow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash(gettext('Cannot unfollow %(nickname)s', nickname=nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You have stop following %(nickname)s', nickname=nickname))
    return redirect(url_for('user', nickname=nickname))


@app.route('/search', methods=['POST'])
@login_required
def search():
    if g.search_form.validate_on_submit():
        return redirect(url_for('search_result', query=g.search_form.search.data))
    return redirect(url_for('index'))


@app.route('/search_result/<query>')
@login_required
def search_result(query):
    resultlist = Post.query.whoosh_search(query, app.config['MAX_SEARCH_RESULTS']).all()
    return render_template('search_result.html',
                           query=query, resultlist=resultlist)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(gettext('Post not found.'))
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash(gettext('You cannot delete this post.'))
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash(gettext('Your post has been deleted.'))
    return redirect(url_for('index'))









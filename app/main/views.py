import os
from . import main
from .. import db, bcrypt
import secrets
from PIL import Image
from flask_wtf import FlaskForm
# from PIL.Image import core as _imaging
from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from ..models import User, Breakfast, Dinner, Lunch, CommentsBreakfast, CommentsDinner, CommentsLunch
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, BreakfastForm, DinnerForm, LunchForm, BreakfastCommentForm, LunchCommentForm, DinnerCommentForm
from flask_login import login_user, current_user, logout_user, login_required



@main.route('/')
@main.route('/home')
def home():
    return render_template('index.html', title='Home')

@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/Breackfast_home')
def breakfast_home():
    breakfasts = Breakfast.query.all()
    return render_template('breakfast_home.html', breakfasts=breakfasts)

@main.route('/lunch_home')
def lunch_home():
    lunchs = Lunch.query.all()
    return render_template('lunch_home.html', lunchs=lunchs)

@main.route('/dinner_home')
def dinner_home():
    dinners = Dinner.query.all()
    return render_template('dinner_home.html', dinners=dinners)

@main.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login','success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@main.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form)


@main.route('/breakfast/new', methods=['GET','POST'])
@login_required
def new_breakfast():
    form = BreakfastForm()
    if form.validate_on_submit():
        breakfast = Breakfast(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(breakfast)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.breakfast_home'))
    return render_template('create_breakfast.html', title='New Breakfast Recipe', form=form, legend='New Breakfast Recipe')



@main.route('/breakfast/<int:breakfast_id>/',methods=["GET","POST"])
def breakfast(breakfast_id):
    breakfast = Breakfast.query.get_or_404(breakfast_id)
    form = BreakfastCommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_breakfast_comment = CommentsBreakfast(comment=comment, breakfast_id=breakfast_id, user_id=current_user.id)
        # new_post_comment.save_post_comments()
        db.session.add(new_breakfast_comment)
        db.session.commit()
    comments = CommentsBreakfast.query.all()
    return render_template('breakfast.html', title=breakfast.title, breakfast=breakfast, breakfast_form=form, comments=comments)


@main.route('/breakfast/<int:breakfast_id>/update', methods=['GET','POST'])
@login_required
def update_breakfast(breakfast_id):
    breakfast = Breakfast.query.get_or_404(breakfast_id)
    if breakfast.author != current_user:
        abort(403)
    form = BreakfastForm()
    if form.validate_on_submit():
        breakfast.title = form.title.data
        breakfast.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.breakfast', breakfast_id=breakfast.id))
    elif request.method == 'GET':
        form.title.data = breakfast.title
        form.content.data = breakfast.content
    return render_template('create_breakfast.html', title='Update Breakfast', form=form, legend='Update Recipe')

@main.route('/breakfast/<int:breakfast_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_breakfast(breakfast_id):
    breakfast = Breakfast.query.get_or_404(breakfast_id)
    for comment in breakfast.comments.all():
        db.session.delete(comment)
        db.session.commit()
    if breakfast.author != current_user:
        abort(403)
    db.session.delete(breakfast)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.breakfast_home'))



@main.route('/lunch/new', methods=['GET','POST'])
@login_required
def new_lunch():
    form = LunchForm()
    if form.validate_on_submit():
        lunch = Lunch(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(lunch)
        db.session.commit()
        flash('Your Product Pitch has been created!', 'success')
        return redirect(url_for('main.lunch_home'))
    return render_template('create_lunch.html', title='New Lunch Recipe', form=form, legend='New Recipe')



@main.route('/lunch/<int:lunch_id>/', methods=['GET','POST'])
def lunch(lunch_id):
    lunch = Lunch.query.get_or_404(lunch_id)
    form = LunchCommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_lunch_comment = CommentsLunch(comment=comment, lunch_id=lunch_id, user_id=current_user.id)
        db.session.add(new_lunch_comment)
        db.session.commit()
    comments = CommentsLunch.query.all()
    return render_template('lunch.html', title=lunch.title, lunch=lunch, lunch_form=form, comments=comments)

@main.route('/lunch/<int:lunch_id>/update', methods=['GET','POST'])
@login_required
def update_lunch(lunch_id):
    lunch = Lunch.query.get_or_404(lunch_id)
    if lunch.author != current_user:
        abort(403)
    form = LunchForm()
    if form.validate_on_submit():
        lunch.title = form.title.data
        lunch.content = form.content.data
        db.session.commit()
        flash('Your Product Pitch has been updated!', 'success')
        return redirect(url_for('main.lunch', lunch_id=lunch.id))
    elif request.method == 'GET':
        form.title.data = lunch.title
        form.content.data = lunch.content
    return render_template('create_lunch.html', title='Update Lunch Recipe', form=form, legend='Update Recipe')

@main.route('/lunch/<int:lunch_id>/delete', methods=['GET','POST'])
@login_required
def delete_lunch(lunch_id):
    lunch = Lunch.query.get_or_404(lunch_id)
    for comment in lunch.comments.all():
        db.session.delete(comment)
        db.session.commit()
    if lunch.author != current_user:
        abort(403)
    db.session.delete(lunch)
    db.session.commit()
    flash('Your Product Pitch has been deleted!', 'success')
    return redirect(url_for('main.lunch_home'))

@main.route('/dinner/new', methods=['GET','POST'])
@login_required
def new_dinner():
    form = DinnerForm()
    if form.validate_on_submit():
        dinner = Dinner(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(dinner)
        db.session.commit()
        flash('Your Pick Up Line has been created!', 'success')
        return redirect(url_for('main.dinner_home'))
    return render_template('create_dinner.html', title='New Dinner Recipe', form=form, legend='New Recipe')



@main.route('/dinner/<int:dinner_id>/', methods=['GET','POST'])
def dinner(dinner_id):
    dinner = Dinner.query.get_or_404(dinner_id)
    form = DinnerCommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        new_dinner_comment = CommentsDinner(comment=comment, dinner_id=dinner_id, user_id=current_user.id)
        db.session.add(new_dinner_comment)
        db.session.commit()
    comments = CommentsDinner.query.all()
    return render_template('dinner.html', title=dinner.title, dinner=dinner, dinner_form=form, comments=comments)


@main.route('/dinner/<int:dinner_id>/update', methods=['GET','POST'])
@login_required
def update_dinner(dinner_id):
    dinner = Dinner.query.get_or_404(dinner_id)
    if dinner.author != current_user:
        abort(403)
    form = DinnerForm()
    if form.validate_on_submit():
        dinner.title = form.title.data
        dinner.content = form.content.data
        db.session.commit()
        flash('Your Pick Up Line has been updated!', 'success')
        return redirect(url_for('main.dinner', dinner_id=dinner.id))
    elif request.method == 'GET':
        form.title.data = dinner.title
        form.content.data = dinner.content
    return render_template('create_dinner.html', title='Update Dinner Recepie', form=form, legend='Update Recipe')

@main.route('/dinner/<int:dinner_id>/delete', methods=['GET','POST'])
@login_required
def delete_dinner(dinner_id):
    dinner = Dinner.query.get_or_404(dinner_id)
    for comment in dinner.comments.all():
        db.session.delete(comment)
        db.session.commit()
    if dinner.author != current_user:
        abort(403)
    db.session.delete(dinner)
    db.session.commit()
    flash('Your Pick Up Line has been deleted!', 'success')
    return redirect(url_for('main.dinner_home'))

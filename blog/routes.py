from flask import render_template, request, send_file
from blog.forms import LoginForm,SignupForm,PostForm,UpdateUsernameForm,UpdateEmailForm,UpdateImg,RequestResetForm
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import app , bcrypt , db , mail
from blog.models import User,Post
from io import 	BytesIO
from flask_mail import Message

@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.date_posted).paginate(per_page=5,page=page)
	post_form = PostForm()
	if post_form.validate_on_submit():
		post = Post(post_form.title.data,post_form.content.data,current_user.id)
		db.session.add(post)
		db.session.commit()
		flash('Your Post has been published','success')
		return redirect(url_for('home'))
	return render_template('index.html',title='Blog',posts=posts,post_form=post_form)

@app.route("/signup", methods=['GET','POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = SignupForm()
	if form.validate_on_submit():
		password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(form.username.data,form.email.data,password)
		db.session.add(user)
		db.session.commit()
		flash(f'Congratulations {form.username.data} You Can Login Now !','success')
		return redirect(url_for('login'))
	return render_template('signup.html',title='Sign Up',form=form)
 
@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get('next') # returns the login required page after logging in or None 
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Failed Login. Please Check Your Email and Password','danger')
	return render_template('login.html',title='Log in',form=form)         

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html',post=post,title=post.title)	

@login_required
@app.route("/post/<int:post_id>/update",methods=['GET', 'POST'])
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()

	if form.validate_on_submit():
		post.title = form.title.data 
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been updated','success')
		return redirect(url_for('post',post_id=post.id))	

	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('update_post.html',post=post,title='Update Post',form=form)

@login_required
@app.route("/post/<int:post_id>/delete",methods=['POST'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted','success')
	return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	posts = Post.query.filter_by(user_id=current_user.id)
	username_form = UpdateUsernameForm()
	if username_form.validate_on_submit():
		current_user.username = username_form.username.data
		db.session.commit()
		flash('Your Username Has Been Updated !','success')
		return redirect(url_for('account'))

	email_form = UpdateEmailForm()
	if email_form.validate_on_submit():
		current_user.email = email_form.email.data
		db.session.commit()
		flash('Your Email Has Been Updated !','success')
		return redirect(url_for('account'))

	img_form = UpdateImg()
	if img_form.validate_on_submit():
		current_user.img = img_form.img.data.read()
		db.session.commit()
		flash('Your Image Has Been Updated !','success')
		return redirect(url_for('account'))

	elif request.method == 'GET':
		username_form.username.data= current_user.username 
		email_form.email.data = current_user.email 
	return render_template('account.html',title='Account',
		username_form=username_form,email_form=email_form,img_form=img_form,posts=posts)     

@app.route("/user/<string:username>")
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page',1,type=int)
	posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted).paginate(per_page=5,page=page)
	img = url_for('user_img',user_id=user.id)
	return render_template('user.html',title='User Account',posts=posts,img=img,user=user)

@app.route('/user_img/<int:user_id>')
def user_img(user_id):
	user = User.query.filter_by(id=user_id).first()
	return send_file(BytesIO(user.img),mimetype='image/png')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request ():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
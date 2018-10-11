from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed , FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User
from flask import flash

class SignupForm(FlaskForm):
	username = StringField(validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField(validators=[DataRequired(),Email()])
	password = PasswordField(validators=[DataRequired()])
	confirm = PasswordField(validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Submit')

	def validate_username(self,username):
		exist = User.query.filter_by(username=username.data).first()
		if exist:
			raise ValidationError('This Username is Aleardy Existes.')

	def validate_email(self,email):
		exist = User.query.filter_by(email=email.data).first()
		if exist:
			raise ValidationError('This Email is Aleardy Existes.')

class LoginForm(FlaskForm):
	email = StringField(validators=[DataRequired(),Email()])
	password = PasswordField(validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log In')	

class UpdateUsernameForm(FlaskForm):
	username = StringField(validators=[DataRequired(),Length(min=2,max=20)])
	submit = SubmitField('Update')

	def validate_username(self,username):
		if username.data != current_user.username:
			exist = User.query.filter_by(username=username.data).first()
			if exist:
				flash('This Username Aleardy Existes.','danger')
				raise ValidationError('This Username Aleardy Existes.')

class UpdateEmailForm(FlaskForm):
	email = StringField(validators=[DataRequired(),Email()])
	submit = SubmitField('Update')

	def validate_email(self,email):
		if email.data != current_user.email:
			exist = User.query.filter_by(email=email.data).first()
			if exist:
				flash('This Email Aleardy Existes.','danger')
				raise ValidationError('This Email Aleardy Existes.')

class UpdateImg(FlaskForm):
    img = FileField(validators=[FileRequired(),FileAllowed(['jpg', 'png'])])	
    submit = SubmitField('Update')

class RequestResetForm(FlaskForm):
	email = StringField(validators=[DataRequired(),Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self,email):
		exist = User.query.filter_by(email=email.data).first()
		if exist is None:
			raise ValidationError('This Email Doesn\'t Existes.')

class ResetPasswordForm(FlaskForm):
	password = PasswordField(validators=[DataRequired()])
	confirm = PasswordField(validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Reset Password')

class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired()])
	content = TextAreaField('Content',validators=[DataRequired()])
	submit = SubmitField('Post')
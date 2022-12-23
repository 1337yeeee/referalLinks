from flask import Blueprint, render_template, g, request, redirect, flash, make_response
from website.database import db_session, User

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
	return render_template('general/index.html')


@mod.route('/signin', methods=['GET'])
def get_sign_in():
	return render_template('general/login.html')

@mod.route('/signin', methods=['POST'])
def sign_in():
	user = User.query.filter_by(
		login=request.form['login'],
		password=request.form['password']
	).first()

	if user:
		resp = make_response(redirect('/'))
		resp.set_cookie('user', str(user.id))
		return resp
	else:
		return render_template('general/login.html', message='Wrong login or/and password')


@mod.route('/signup', methods=['GET'])
def get_sign_up():
	return render_template('general/signup.html')

@mod.route('/signup', methods=['POST'])
def sign_up():
	if g.user is None:
		if User.query.filter_by(login=request.form['login']).first():
			return render_template('general/signup.html', message='Login already registered')
		else:
			new_user = User(
				login=request.form['login'],
				password=request.form['password'],
				name=request.form['name'],
			)
			db_session.add(new_user)
			db_session.commit()
			flash(u'Successfully created profile and logged in')
			resp = make_response(redirect('/'))
			resp.set_cookie('user', str(new_user.id))
			return resp


@mod.route('/logout')
def logout():
	resp = make_response(redirect('/'))
	resp.delete_cookie('user')
	return resp

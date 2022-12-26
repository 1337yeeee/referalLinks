from flask import Blueprint, render_template, g, request, redirect, flash, make_response
from website.database import db_session, User, RefLink, Referral
from sqlalchemy import func

mod = Blueprint('referral', __name__)

@mod.route('/referral')
def referral():
	referrals = None

	if g.user:
		current_link = RefLink.query.filter_by(
			user_id=g.user.id,
			date_created=db_session.query(func.max(RefLink.date_created)
				)
		).first()

		if current_link:
			current_link = 'http://127.0.0.1:5000/referral/' + current_link.link
		else:
			current_link = ''

		referrals = Referral.query.filter_by(owner_id=g.user.id).all()

	return render_template('referral/index.html', referrals=referrals, link=current_link)


@mod.route('/referral/click')
def click():
	if not g.user:
		return '404'

	link = RefLink(g.user.id)
	db_session.add(link)
	db_session.commit()

	return 'http://127.0.0.1:5000/referral/' + link.link


@mod.route('/referral/<link>', methods=['GET', 'POST'])
def make_ref(link):
	ref_link = RefLink.query.filter_by(link=link).first()

	if ref_link is None:
		return '<h1 style="text-align:center; margin-top: 10rem; font-size: 4rem">NOT FOUND 404</h1>'

	if request.method == 'GET':
		return render_template('general/signup.html', ref=True)

	elif request.method == 'POST':
		if g.user is None:
			if User.query.filter_by(login=request.form['login']).first():
				return render_template('general/signup.html', message='Login already registered')
			else:
				new_user = User(
					login=request.form['login'],
					password=request.form['password'],
					name=request.form['name'],
					invite_id=ref_link.id
				)
				db_session.add(new_user)
				db_session.commit()

				ref_link = RefLink.query.filter_by(link=link).first()
				new_referral = Referral(
					user_id=new_user.id,
					owner_id=ref_link.user_id,
				)

				db_session.add(new_referral)
				db_session.commit()
				flash(u'Successfully created profile and logged in')
				resp = make_response(redirect('/'))
				resp.set_cookie('user', str(new_user.id))
				return resp

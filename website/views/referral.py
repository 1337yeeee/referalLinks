from flask import Blueprint, render_template, g, request, redirect, flash, make_response
from website.database import db_session, User, RefLink

mod = Blueprint('referral', __name__)

@mod.route('/referral')
def referral():
	return render_template('referral/index.html')


@mod.route('/referral/click')
def click():
	if not g.user:
		return '404'

	link = RefLink.query.filter_by(user_id=g.user.id).first()

	if link:
		link.link = RefLink.generateLink()
		db_session.commit()
	else:
		link = RefLink(g.user.id)
		db_session.add(link)
		db_session.commit()

	return 'http://127.0.0.1:5000/referral/' + link.link

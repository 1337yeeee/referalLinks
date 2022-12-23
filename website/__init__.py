from datetime import datetime
from flask import Flask, session, g, request

app = Flask(__name__)
app.config.from_object('websiteconfig')


@app.before_request
def load_current_user():
    g.user = User.query.filter_by(id=int(request.cookies['user'])).first() \
        if 'user' in request.cookies else None
    print(g.user)


from website.views import index
app.register_blueprint(index.mod)


from website.database import User

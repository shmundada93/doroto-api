#!/usr/bin/env python
import os
from doroto import create_app, db
from doroto.models import User

app = create_app(os.environ.get('FLASK_CONFIG', 'testing'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # create a development user
        if User.query.get(1) is None:
            u = User(email='admin@test.com')
            u.set_password('admin')
            db.session.add(u)
            db.session.commit()
    app.run(host="0.0.0.0", port=8000)

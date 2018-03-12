#!/usr/bin/env python
import os
from doroto import create_app, db
from doroto.models import CompanyUser

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # create a development user
        if CompanyUser.query.get(1) is None:
            u = CompanyUser(email='admin@test.com')
            u.set_password('admin')
            db.session.add(u)
            db.session.commit()
    app.run(host="0.0.0.0", port=8000)

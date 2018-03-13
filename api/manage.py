import os
from doroto import create_app, db
from doroto.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.environ.get('FLASK_CONFIG', 'testing'))
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    with app.app_context():
        db.create_all()
        # create a development user	
        if User.query.get(1) is None:	
            u = User(email='admin@test.com')	
            u.set_password('admin')	
            db.session.add(u)	
            db.session.commit()
    app.run(host="0.0.0.0", port=8000)

if __name__ == '__main__':
    manager.run()

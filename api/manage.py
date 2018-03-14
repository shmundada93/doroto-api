import os
from doroto import create_app, db
from doroto.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from seed import seed_roles, seed_departments_and_positions
from flask_cors import CORS, cross_origin

app = create_app(os.environ.get('FLASK_CONFIG', 'testing'))
if os.environ.get('FLASK_CONFIG') == 'testing':
    CORS(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host="0.0.0.0", port=8000)

@manager.command
def seed():
    "Add seed data to the database."
    print("Seeding started..")
    seed_roles(db)
    seed_departments_and_positions(db)
    print("Seeding completed.")

if __name__ == '__main__':
    manager.run()

#!/usr/bin/env python
import os
import config
from project import create_app
from flask.ext.script import Manager, Shell
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app('default')

with app.app_context():
    db = SQLAlchemy(app)
    db.create_all()

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app)

manager.add_command("Shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()

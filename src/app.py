#!/usr/bin/env python3

__author__ = 'golim'

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import logging
import os

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:password@localhost/db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

app.secret_key = 'secretkey'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))

    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id=user_id).first()

def create_database():
    db.drop_all()
    db.create_all()

def populate_database():
    # Add the admin user
    new_user = User(None, 'admin', ADMIN_PASSWORD)
    db.session.add(new_user)
    db.session.commit()

    # Get all from the database
    users = db.session.query(User).all()
    logger.debug('Users: %s', users)

# Create the database
with app.app_context():
    create_database()

# Populate the database with the admin user and the products
with app.app_context():
    populate_database()

@app.route('/query', methods=['GET'])
def query():
    query = request.args.get('query')

    logger.debug('Query: %s', query)

    if query:
        sql_query = text(query)

        with db.engine.connect() as connection:
            result = connection.execute(sql_query)

        results = result.fetchall()
        column_names = result.keys()

        if result:
            flash("Success", category='success')
            return render_template('query.html', results=results, column_names=column_names)
        else:
            flash('Error executing query.', category='error')
    else:
        flash('Invalid query.', category='error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Development
    app.run(debug=True, host='0.0.0.0', port=5000)

    # Production
    # serve(app, host='0.0.0.0', port=5000)

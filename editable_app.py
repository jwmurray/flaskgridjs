#!/usr/bin/env python3

from app import app, db
from app.models import User


@app.before_first_request
def create_tables():
    db.create_all()
    
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
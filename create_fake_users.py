#!/usr/bin/env python3

import random
import sys
from faker import Faker
from app import db, app
from app.models import User


def create_fake_users(n):
    """Generate fake users."""
    with app.app_context():
        faker = Faker()
        for i in range(n):
            user = User(name=faker.name(),
                        age=random.randint(20, 80),
                        address=faker.address().replace('\n', ', '),
                        phone=faker.phone_number(),
                        email=faker.email())
            db.session.add(user)
        db.session.commit()
        query = User.query
        count = query.count()
        print(f'Added {n} new fake users.  Total: {count}.')


if __name__ == '__main__':
    # if len(sys.argv) <= 1:
    #     print('Pass the number of users you want to create as an argument.')
    #     sys.exit(1)
    if len(sys.argv) <= 1:
        print('adding 100 users')
        users = 100
    else:
        count = int(sys.argv[1])
    create_fake_users(users)

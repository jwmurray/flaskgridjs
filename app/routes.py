from app.models import User
from app import app, db
from flask import render_template, request, abort
from random_address import real_random_address
import names, random


@app.route('/fill')
def fill_db():
    users = User.query
    user_list = []
    
    for index in range(100):
        raddress = real_random_address()
        faddress = raddress['address1']
        faddress += f", {raddress['address2']}" if  'address2' in raddress.keys() else ""
        faddress += f", {raddress['city']}" if 'city' in raddress.keys() else ""
        faddress += f", {raddress['state']}" if 'state' in raddress.keys() else ""
        faddress += f" {raddress['postalCode']}" if 'postalCode' in raddress.keys() else ""
        user = User(
            name = f"{names.get_first_name()} {names.get_last_name()}",
            age = random.randint(10,100),
            address = faddress 
            # phone = 
            # email = 
        )
        db.session.add(user)
        db.session.commit()
    users = User.query
    return render_template('editable_table.html', users=users)


@app.route('/clear')
def clear():
    users = User.query.delete()
    db.session.commit()
    return index()
    # return render_template('editable_table.html', users=users)


@app.route('/')
def index():
    users = User.query
    return render_template('editable_table.html', users = users)


@app.route('/api/data')
def data():
    query = User.query

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            User.name.like(f'%{search}%'),
            User.email.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['name', 'age', 'email']:
                name = 'name'
            col = getattr(User, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'total': total,
    }


@app.route('/api/data', methods=['POST'])
def update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    user = User.query.get(data['id'])
    for field in ['name', 'age', 'address', 'phone', 'email']:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return '', 204





from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required

from laundry import db
from laundry.admin import admin
from laundry.models import Order, User, Message

from sqlalchemy import desc



@admin.route('/dashboard')
@login_required
def dashboard():
    orders = Order.query
    order_count = orders.count()
    in_progress = orders.filter_by(status=False).count()
    completed = orders.filter_by(status=True)
    total = sum([order.amount for order in completed.all()])
    return render_template(
        'admin/dashboard.html', 
        orders=orders, 
        total=total, 
        order_count=order_count,
        in_progress=in_progress,
        completed=completed.count()
    )


@admin.route('/inprogress')
@login_required
def inprogress():
    orders = Order.query.filter_by(status=False).all()
    types = {order.service_type for order in orders}
    return render_template('admin/inprogress.html', User=User, orders=orders, types=types)


@admin.route('/inprogress/<service_type>')
@login_required
def inprogress_filt(service_type):
    orders = Order.query.filter_by(status=False)
    types = {order.service_type for order in orders.all()}
    orders = orders.filter_by(service_type=service_type).all()
    return render_template('admin/inprogress.html', User=User, orders=orders, types=types, service_type=service_type)


@admin.route('/completed')
@login_required
def completed():
    orders = Order.query.filter_by(status=True).all()
    types = {order.service_type for order in orders}
    return render_template('admin/completed.html', User=User, orders=orders, types=types)


@admin.route('/completed/<service_type>')
@login_required
def completed_filt(service_type):
    orders = Order.query.filter_by(status=True)
    types = {order.service_type for order in orders.all()}
    orders = orders.filter_by(service_type=service_type).all()
    return render_template('admin/completed.html', User=User, orders=orders, types=types, service_type=service_type)


@admin.route('/complete_order/<int:id>', methods=['POST'])
@login_required
def complete_order(id: int):
    order = Order.query.get(id)
    order.status = True
    db.session.commit()
    flash('Order #{:03d} completed'.format(order.id), 'success')
    return redirect(url_for('.inprogress'))


@admin.route('/review')
@login_required
def reviews():
    messages = Message.query.order_by(desc(Message.timestamp)).all()
    return render_template('admin/reviews.html', messages=messages)


@admin.route('/review/<int:id>')
@login_required
def review(id):
    message = Message.query.get(id)
    user = User.get(message.user_id)
    return render_template('admin/review.html', message=message, user=user)

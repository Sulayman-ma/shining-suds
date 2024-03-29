import datetime
import random

from flask import render_template, url_for, redirect, flash, session, current_app, request
from flask_login import current_user, login_required
from wtforms.validators import ValidationError
from sqlalchemy.exc import IntegrityError, DatabaseError

from laundry import db
from laundry.main import main
from laundry.models import Order, Message, User
from laundry.main.forms import EditProfile, ScheduleOrder



@main.route('/')
def home():
    return render_template('shared/home.html')


@main.route('/home')
@login_required
def user_home():
    return render_template('main/user_home.html')


@main.route('/terms', methods=['GET', 'POST'])
def terms():
    if request.method == 'POST':
        current_user.accepted_terms = True
        db.session.commit()
        return redirect(url_for('.user_home'))
    return render_template('shared/terms.html')


@main.route('/support')
@login_required
def support():
    return render_template('shared/support.html')


@main.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        try:
            form = request.form
            pass2 = form.get('confirm_password')
            pass1 = form.get('password')
            if pass1 != pass2:
                flash('Passwords must match', 'misc')
                return redirect(url_for('.create_account'))
            user = User(
                name=form.get('name'),
                email=form.get('email'),
                phone=form.get('phone'),
                address=form.get('address'),
                password=pass1
            )
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            flash('Email is already taken', 'misc')
            return redirect(url_for('.create_account'))
        except:
            flash('An error has occured, please try again', 'light-error')
            return redirect(url_for('.create_account'))
    return render_template('main/create_account.html')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfile(obj=current_user)
    if form.is_submitted():
        try:
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.address = form.address.data
            current_user.phone = form.phone.data
            # Change password logic
            if form.current_password.data and form.new_password.data:
                if not current_user.verify_password(form.current_password.data):
                    flash('Incorrect current password', 'error')
                    return redirect(url_for('.profile'))
                else:
                    current_user.password = form.new_password.data
            db.session.commit()
            flash('Changes saved', 'success')
        except ValidationError:
            flash('Invalid inputs', 'misc')
            return redirect(url_for('.profile'))
        except IntegrityError:
            if current_user.email != form.email.data:
                flash('Email already taken', 'misc')
                return redirect(url_for('.profile'))
            else:
                pass
        except:
            flash('An error has occured, please try again', 'error')
            return redirect(url_for('.profile'))
        return redirect(url_for('.profile'))
    return render_template('main/profile.html', form=form)


@main.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id = current_user.id).order_by(Order.created.desc()).all()
    return render_template('main/orders.html', orders=orders)


@main.route('/write_review/<int:id>', methods=['GET', 'POST'])
@login_required
def write_review(id: int):
    order = Order.query.get(id)
    orders = current_user.orders
    if order not in orders:
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        if 'subject' in request.form and 'message' in request.form:
            message = Message(
                subject=request.form.get('subject'),
                message=request.form.get('message'),
                user_id=current_user.id,
                order_id=id
            )
            # mark order as reviewed
            order.reviewed = True
            db.session.add(message)
            db.session.commit()
            flash('Review sent', 'success')
            return redirect(url_for('.orders'))
        else:
            # print("Subject or message not found in request.form")  # Debug statement
            flash('Please enter a review subject and message')
            return redirect(url_for('.write_review'))

    return render_template('main/write_review.html', id=id)


def create_order(data: dict) -> Order:
    """Helper function for creating an order after scheduling and/or making the payment
    
    Keyword arguments:
    data -- Order form data
    Return: None
    """

    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return order


def random_delivery_date(pickup_date):
    number = random.randint(3, 7)
    return pickup_date + datetime.timedelta(days=number)


@main.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    form = ScheduleOrder()
    services = {
        'WASH & IRON': 200, 
        'WASH': 100, 
        'IRON': 100, 
        'STEAM': 150, 
        'BLEACH': 200, 
        'STAIN REMOVAL': 300
    }
    if form.validate_on_submit():
        try:
            service = request.form.get('service')
            clothes_count = form.clothes_count.data
            service_cost = services.get(service)
            amount = service_cost * form.clothes_count.data
            pickup_date = datetime.datetime.strptime(str(form.pickup_date.data), '%Y-%m-%d')
            delivery_date = random_delivery_date(pickup_date)
            # store form data for processing
            session.setdefault('order_data', {
                'amount': amount,
                'special_instr': form.special_instr.data,
                'service_type': service,
                'clothes_count': clothes_count,
                'pickup_date': pickup_date,
                'delivery_date': delivery_date,
                'pickup_addr': form.pickup_addr.data or current_user.address,
                'delivery_addr': form.delivery_addr.data or current_user.address,
                'user_id': current_user.id
            })
            if form.payment_option.data == 'Online':
                return redirect(url_for('.pay_paystack'))
            else:
                return redirect(url_for('.place_order'))
        except ValidationError:
            flash('Invalid inputs', 'misc')
            return redirect(url_for('.schedule'))
        except:
            flash('An error has occured, please try again', 'error')
            return redirect(url_for('.schedule'))
    return render_template('main/schedule.html', form=form, services=services)


@main.route('/schedule/<int:id>')
@login_required
def order_success(id):
    order = Order.query.get(id)
    return render_template('main/success_order.html', order=order)


@main.route('/pay_paystack', methods=['GET', 'POST'])
@login_required
def pay_paystack():
    order_data = session.get('order_data')
    cost = order_data.get('amount')
    transaction = current_app.config.get('API_OBJECT')
    # initialize transaction
    response = transaction.initialize(
        email = current_user.email,
        amount = cost * 100,
        label = current_user.name,
        callback_url = url_for(endpoint='.place_order', _external=True)
    )
    session['reference'] = response.get('reference')
    return redirect(response.get('authorization_url'))


@main.route('/place_order')
@login_required
def place_order():
    try:
        order = create_order(session.pop('order_data'))
    except IntegrityError:
        flash('Please fill the address fields', 'misc')
        return redirect(url_for('.schedule'))
    except DatabaseError:
        flash('A database error has occured, please try again.', 'error')
        return redirect(url_for('.schedule'))
    except:
        flash('An error has occured, please try again', 'error')
        return redirect(url_for('.schedule'))
    return redirect(url_for('.order_success', id=order.id))

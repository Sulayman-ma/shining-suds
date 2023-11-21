import datetime

from flask import render_template, url_for, redirect, flash, session, current_app, request
from flask_login import current_user, login_required
from wtforms.validators import ValidationError
from sqlalchemy.exc import IntegrityError, DatabaseError

from laundry import db
from laundry.main import main
from laundry.models import Order, Message, User
from laundry.main.forms import EditProfile, ScheduleOrder, WriteReview
from laundry.duckstack.transaction import Transaction



@main.route('/')
def home():
    return render_template('shared/home.html')


@main.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'post':
        form = request.form
        second_pass = form.get('confirm_password')
        password = form.get('password')
        if password != second_pass:
            flash('Passwords much match', 'misc')
            return redirect(url_for('.create_account'))
        try:
            user = User(
                name=form.get('name'),
                email=form.get('email'),
                phone=form.get('phone'),
                address=form.get('address'),
                password=form.get('password')
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
                else:
                    current_user.password = form.new_password.data
            db.session.commit()
            flash('Changes saved', 'success')
        except ValidationError:
            flash('Invalid inputs', 'misc')
            return redirect(url_for('.profile'))
        except IntegrityError:
            flash('Email already taken', 'misc')
            return redirect(url_for('.profile'))
        except:
            flash('An error has occured, please try again', 'error')
            return redirect(url_for('.profile'))
        return redirect(url_for('.profile'))
    return render_template('main/profile.html', form=form)


@main.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    orders = Order.query.filter_by(user_id = current_user.id).order_by(Order.created).all()
    return render_template('main/orders.html', orders=orders)


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


@main.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    form = ScheduleOrder()
    if form.validate_on_submit():
        try:
            clothes_count = form.clothes_count.data
            pickup_date = datetime.datetime.strptime(str(form.pickup_date.data), '%Y-%m-%d')
            delivery_date = datetime.datetime.strptime(str(form.delivery_date.data), '%Y-%m-%d')
            if pickup_date > delivery_date:
                flash('Pickup cannot be after delivery.', 'misc')
                return redirect(url_for('.schedule'))
            # store form data for processing
            session.setdefault('order_data', {
                'amount': clothes_count * 50,
                'message': form.message.data,
                'service_type': form.service_type.data,
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
        except IntegrityError:
            flash('Email already taken', 'misc')
            return redirect(url_for('.schedule'))
        except:
            flash('An error has occured, please try again', 'error')
            return redirect(url_for('.schedule'))
    return render_template('main/schedule.html', form=form)


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
        flash('Please input number of clothes', 'misc')
        return redirect(url_for('.schedule'))
    except DatabaseError:
        flash('A database error has occured, please try again.', 'error')
        return redirect(url_for('.schedule'))
    except:
        flash('An error has occured, please try again', 'error')
        return redirect(url_for('.schedule'))
    return redirect(url_for('.order_success', id=order.id))


@main.route('/review_order/<int:id>', methods=['GET'])
@login_required
def write_review(id: int):
    order = Order.query.get(id)
    form = WriteReview()
    if form.validate_on_submit():
        # try:
        message = Message(
            subject=form.subject.data,
            message=form.message.data,
            user_id=current_user.id
        )
        db.session.add(message)
        db.session.commit()
        flash('Review sent', 'success')
        return redirect(url_for('.orders'))
        # except:
        # flash('Your message failed to send, please try again.', 'error')
        # return redirect(url_for('.write_review', id=id))
    return render_template('main/write_review.html', order=order, form=form)

from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
    EmailField,
    TelField,
    SubmitField,
    SelectField,
    TextAreaField,
    DateField,
    IntegerField
)
from wtforms.validators import Email, InputRequired



class EditProfile(FlaskForm):
    name = StringField(label="Name", render_kw={
        'placeholder': 'Name'
    })
    email = EmailField(label="E-mail", render_kw={
        'placeholder': 'Email'
    }, validators=[Email()])
    phone = TelField(label="Mobile Phone", render_kw={
        'placeholder': 'Mobile Phone'
    })
    address = StringField(label="Default Address", render_kw={
        'placeholder': 'Default Address'
    })
    current_password = PasswordField(render_kw={
        'placeholder': 'Current Password'
    })
    new_password = PasswordField(render_kw={
        'placeholder': 'New Password'
    })
    save = SubmitField(label='Save Changes')


class ScheduleOrder(FlaskForm):
    payment_option = SelectField(label='Payment Option', choices=[
        'Cash On Delivery', 'Online'
    ])
    service_type = SelectField(label='Service Type', choices=[
        'WASH & IRON', 'WASH', 'IRON', 'STEAM', 'BLEACH', 'STAIN REMOVAL'
    ])
    pickup_date = DateField(label='Pickup Date', render_kw={
        'required': 'required'
    })
    delivery_date = DateField(label='Delivery Date', render_kw={
        'required': 'required'
    })
    pickup_addr = StringField(label='Pickup Address', render_kw={
        'placeholder': 'Leave blank to use default address set in profile'
    })
    delivery_addr = StringField(label='Delivery Address', render_kw={
        'placeholder': 'Leave blank to use default address set in profile'
    })
    message = TextAreaField(label='Special Instructions')
    clothes_count = IntegerField(label='Clothes Count', render_kw={
        'placeholder': 'Number of clothes',
        'required': 'required'
    }, validators=[InputRequired()])
    confirm = SubmitField(label='Confirm Order')


class WriteReview(FlaskForm):
    subject = StringField(label='Subject', render_kw={
        'placeholder': 'Review subject',
        'required': 'required'
    })
    message = TextAreaField(label='Message', render_kw={
        'placeholder': 'Tell us about your experience...',
        'required': 'required'
    })
    send = SubmitField(label='Send Review')

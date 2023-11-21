from laundry import create_app, db
from laundry.models import User, Order, Message
from laundry.duckstack.transaction import Transaction
from config import config



app = create_app(config)

# PAYSTACK TRANSACTION OBJECT FOR WHOLE APP
transaction = Transaction(app.config.get('PAY_STACK_KEY'))
app.config.setdefault('API_OBJECT', transaction)

@app.shell_context_processor
def context_processor():
    return dict(
        db=db,
        User=User,
        Order=Order,
        Message=Message
    )

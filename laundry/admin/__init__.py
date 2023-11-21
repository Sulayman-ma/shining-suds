from flask import Blueprint

admin = Blueprint(
    name='admin', 
    import_name=__name__,
    url_prefix='/admin'
)

from . import views
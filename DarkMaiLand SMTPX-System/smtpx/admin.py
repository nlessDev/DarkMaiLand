from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import User, Email, Attachment, Session

class UserModelView(ModelView):
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['emails']
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password_hash = ph.hash(form.password.data)

def create_admin(app):
    admin = Admin(app, name='SMTPX Admin')
    admin.add_view(UserModelView(User, Session()))
    admin.add_view(ModelView(Email, Session()))
    admin.add_view(ModelView(Attachment, Session()))

from flask import render_template, request, redirect, url_for
from .forms import ComposeForm
from ..client import SMTPXClient

@web.route('/')
def inbox():
    return render_template('inbox.html')

@web.route('/compose', methods=['GET', 'POST'])
def compose():
    form = ComposeForm()
    if form.validate_on_submit():
        with SMTPXClient('localhost') as client:
            client.send_mail(
                form.sender.data,
                form.recipients.data,
                form.body.data
            )
        return redirect(url_for('web.inbox'))
    return render_template('compose.html', form=form)

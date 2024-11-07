from flask import request


def contact_form():
    contact_name = request.form.get('contact-name')
    user_email = request.form.get('user-email')
    admin_email = request.form.get('admin-email')
    message = request.form.get('message')

    contact_data = {
        'contact_name': contact_name,
        'user_email': user_email,
        'admin_email': admin_email,
        'message': message
    }

    return contact_data
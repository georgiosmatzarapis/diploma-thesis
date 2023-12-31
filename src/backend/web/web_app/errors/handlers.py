from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    requested_page = '404'
    return render_template('errors/404.html', requested_page=requested_page), 404


@errors.app_errorhandler(403)
def error_403(error):
    requested_page = '403'
    return render_template('errors/403.html', requested_page=requested_page), 403


@errors.app_errorhandler(500)
def error_500(error):
    requested_page = '500'
    return render_template('errors/500.html', requested_page=requested_page), 500
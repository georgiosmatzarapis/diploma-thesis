""" Routes about user functionality. """
from flask import render_template, url_for, flash, redirect, request, session, Blueprint
from backend import bcrypt, lg
from backend.web.database_api import UserInsertManager, UserFindManager, UserDeleteManager
from backend.web.web_app.users_auth import forms
from backend.web.web_app.users_auth import lib
from backend.web.lib import check_if_all_settings_exist


LOGGER = lg.get_logger(__name__)
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):


        if session.get('first_login'):
            return redirect(url_for('users.logout'))
            
        else:    
            return redirect(url_for('main.home'))


    else:
        form = forms.RegistrationForm()
        if form.validate_on_submit():
            lib.registry_process(form, LOGGER)
            return redirect(url_for('users.login'))

        requested_page = 'register'
        return render_template('users_auth/register.html', title='Register', form=form, requested_page=requested_page)


@users.route("/login", methods=['GET', 'POST'])
def login():

    if session.get('logged_in'):


        if session.get('first_login'):
            return redirect(url_for('users.logout'))

        else:
            return redirect(url_for('main.home'))

    else:
        form = forms.LoginForm()
        
        if form.validate_on_submit():
            user = UserFindManager.find_user('email', form.email.data)

            if user and bcrypt.check_password_hash(user['password'], form.password.data):
                lib.login_process(form, LOGGER, user)

                # CHECK If USER'S FIRST_LOGIN
                if (check_if_all_settings_exist()): 
                    session['first_login'] = False
                    return redirect(url_for('main.home'))
                else:
                    UserDeleteManager.delete_user_settings(session.get('email'))
                    session['first_login'] = True
                    return redirect(url_for('allergy_settings.allergy_data'))
            else:
                flash('Login Unsuccessful. Please check username or password.', 'danger')

        requested_page = 'login'
        return render_template('users_auth/login.html', title='Login', form=form, requested_page=requested_page)


@users.route("/logout")
def logout():
    lib.logout_process(LOGGER)
    return redirect(url_for('main.home'))


@users.route("/profile", methods=['GET', 'POST'])
def profile():

    if session.get('logged_in'):


        if session.get('first_login'):
            return render_template('allergy_settings/warning.html', title='Warning')

        else:

            # Info from mongodb for print user's informations
            account_info = lib.retrieve_account_info_from_db()
            allergy_info = lib.retrieve_allergy_info_from_db()
            allergy_affection_list_len = len(allergy_info.get('allergy_data').get('allergy_affection'))
            symptoms_list_len = len(allergy_info.get('allergy_symptoms').get('symptoms'))
            allergens_list_len = len(allergy_info.get('allergens').get('allergens'))
            # ------------------------------------------------

            form_update = forms.UpdateAccountForm()
            form_delete = forms.DeleteAccountForm()
            form_change_password = forms.ChangePasswordForm()
            LOGGER.debug(f' Change password button: {form_change_password.submit_change_password.data} | Update info button: {form_update.submit_update.data} | Delete button: {form_delete.submit_deletion.data}')

            if request.method == 'GET':
                LOGGER.info(f'GET Request')
                form_update.username.data = session.get('username')
                requested_page = 'profile'
                return render_template('users_auth/profile.html', title='Profile', form_update=form_update, form_delete=form_delete, form_change_password=form_change_password,
                                    account_info=account_info, allergy_info=allergy_info, allergy_affection_list_len=allergy_affection_list_len, 
                                    symptoms_list_len=symptoms_list_len, allergens_list_len=allergens_list_len, requested_page=requested_page)

            elif request.method == 'POST':   
                LOGGER.info(f'POST Request')
                if form_change_password.submit_change_password.data and form_change_password.validate_on_submit(): # CHANGE PASSWORD
                    lib.change_password(form_change_password, LOGGER)
                    return redirect(url_for('users.profile'))
                elif form_update.submit_update.data and form_update.validate_on_submit(): # UPDATE INFO
                    lib.update_username(form_update, LOGGER)
                    return redirect(url_for('users.profile'))
                elif form_delete.submit_deletion.data and form_delete.is_submitted(): # DELETE ACCOUNT
                    lib.delete_account(LOGGER)
                    return redirect(url_for('users.logout'))


    else:
        LOGGER.warning('No authorized user tried to access the accounts settings page!')
        flash('Please log in to access this page.', 'dark')
        return redirect(url_for('users.login'))
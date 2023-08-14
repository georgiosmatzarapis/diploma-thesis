from flask import flash, session
from backend import bcrypt
from backend.web.database_api import UserInsertManager, UserUpdateManager, UserFindManager, UserDeleteManager


def registry_process(form, LOGGER):
    """ Implements user's registry process. """

    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = UserInsertManager.insert_user(form.username.data, form.email.data, hashed_password, form.birthday.data, form.first_name.data, form.last_name.data)
    LOGGER.debug(f'Registration with the following info: {form.username.data} - {form.email.data} - {hashed_password} - {form.birthday.data} - {form.first_name.data} - {form.last_name.data}')
    flash('Your account has been created! You are now able to log in', 'success')


def login_process(form, LOGGER, user):
    """ Implements user's log-in process (sets sessions). """

    session['logged_in'] = True
    session['username'] = user['username']
    session['email'] = user['email']
    if form.remember.data is True: # if remember check box is checked
        session.permanent = True
    username = session.get('username')
    LOGGER.info(f'Successfull log in for user \'{username}\'')


def logout_process(LOGGER):
    """ Implements user's log-out process (pops sessions). """

    username = session.get('username')
    LOGGER.info(f'Successfull log out for user \'{username}\'')
    session.pop('username', None)
    session.pop('email', None)
    session.pop('logged_in', None)
    session.pop('first_login', None)
    if session.permanent:
        session.permanent = False


def retrieve_account_info_from_db():
    """ Returns user's account info. """

    first_name = UserFindManager.find_basic_account_info(session.get('email'), 'first name')
    last_name = UserFindManager.find_basic_account_info(session.get('email'), 'last name')
    registry_date = UserFindManager.find_basic_account_info(session.get('email'), 'registry date')

    account_info = {'first_name': first_name,
                    'last_name': last_name,
                    'registry_date': registry_date}

    return account_info


def retrieve_allergy_info_from_db():
    """ Returns user's allergy info. """

    gender = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'gender')
    family_history = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'family history')
    allergic_rhinitis = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergic rhinitis')
    allergic_asthma = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergic asthma')
    allergic_conjunctivitis = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergic conjunctivitis')
    allergy_frequency = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergy frequency')
    allergy_affection = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergy affection')
    immunotherapy = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'immunotherapy')
    immunotherapy_start_date = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'immunotherapy start date')
    medicine_days = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'medicine days')
    medicine_weeks = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'medicine weeks')

    symptoms = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Symptoms', 'symptoms')

    allergens = UserFindManager.find_allergy_info(session.get('email'), 'Allergens', 'allergens')

    allergic_rhinitis_nose = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - nose')
    allergic_rhinitis_mouth = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - mouth')
    allergic_rhinitis_injection = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - injection')
    allergic_asthma_mouth = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic asthma - mouth')
    allergic_conjunctivitis_drops = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic conjunctivitis - drops')


    allergy_info = {'allergy_data': { 'gender': gender,
                                      'family_history': family_history,
                                      'allergic_rhinitis': allergic_rhinitis,
                                      'allergic_asthma': allergic_asthma, 
                                      'allergic_conjunctivitis': allergic_conjunctivitis,
                                      'allergy_frequency': allergy_frequency,
                                      'allergy_affection': allergy_affection,
                                      'immunotherapy': immunotherapy,
                                      'immunotherapy_start_date': immunotherapy_start_date,
                                      'medicine_days': medicine_days,
                                      'medicine_weeks': medicine_weeks},

                    'allergy_symptoms': {'symptoms': symptoms},
                    
                    'allergens': {'allergens': allergens},
                    
                    'medicines': {'allergic_rhinitis_nose': allergic_rhinitis_nose,
                                  'allergic_rhinitis_mouth': allergic_rhinitis_mouth,
                                  'allergic_rhinitis_injection': allergic_rhinitis_injection,
                                  'allergic_asthma_mouth': allergic_asthma_mouth,
                                  'allergic_conjunctivitis_drops': allergic_conjunctivitis_drops}}

    return allergy_info


def change_password(form_change_password, LOGGER):
    """ Implements change password process. """

    if form_change_password.new_password.data == form_change_password.confirm_new_password.data: 
        user = UserFindManager.find_user('email', session.get('email'))

        # check if hashed password from mongodb is equal with plain text input password
        if bcrypt.check_password_hash(user['password'], form_change_password.current_password.data):
            hashed_new_password = bcrypt.generate_password_hash(form_change_password.new_password.data).decode('utf-8')
            UserUpdateManager.update_authentication_info(session.get('email'), 'password', hashed_new_password)
            flash('Password has successfully changed', 'success')
        else:
            flash('\'Current Password\' field is incorrect', 'warning')

    else:
        flash('New password\'s fields must be equal', 'danger')


def update_username(form, LOGGER):
    """ Updates user's username. """


    if form.username.data == session.get('username'):
        flash('No change for update', 'warning')

    else:

        if UserFindManager.find_user('username', form.username.data):
            flash('That username is taken. Please choose a different one.', 'warning')

        else:
            
            if (len(form.username.data) >= 2) and (len(form.username.data) <= 20):
                UserUpdateManager.update_authentication_info(session.get('email'), 'username', form.username.data)
                session['username'] = form.username.data
                LOGGER.info(f'Username updated for user \'{form.username.data}\'')
                flash('Username updated', 'success')

            else:
                flash('Field must be between 2 and 20 characters long.', 'danger')


def delete_account(LOGGER):
    """ Deletes permanently user's account. """

    UserDeleteManager.delete_user(session.get('email'))
    LOGGER.debug('Account has been deleted')
    flash('Your account has been deleted', 'danger')




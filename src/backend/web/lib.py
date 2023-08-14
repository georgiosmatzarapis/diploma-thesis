""" Module with general helper functions for 'web' directory. """
from backend.web.database_api import UserInsertManager, UserFindManager
from flask import session


def check_if_all_settings_exist():
    """ Check if user has filled out all settings from the first logged-in time. """
    
    if (UserFindManager.check_for_existing_allergy_info(session.get('email'), 'Allergy Data') and
        UserFindManager.check_for_existing_allergy_info(session.get('email'), 'Allergy Symptoms') and
        UserFindManager.check_for_existing_allergy_info(session.get('email'), 'Allergens') and
        UserFindManager.check_for_existing_allergy_info(session.get('email'), 'Medicines') and
        UserFindManager.check_for_existing_vas_info(session.get('email'))):

        return True

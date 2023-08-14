""" Routes about allergy settings functionality. """
from flask import render_template, url_for, flash, redirect, request, session, Blueprint
from backend import bcrypt, lg
from backend.web.database_api import UserInsertManager
from backend.web.web_app.allergy_settings import forms
from backend.web.web_app.main.forms import VasToolForm
from backend.web.web_app.allergy_settings import lib
from backend.web.lib import check_if_all_settings_exist

LOGGER = lg.get_logger(__name__)
allergy_settings = Blueprint('allergy_settings', __name__)



@allergy_settings.route("/allergy_data", methods=['GET', 'POST'])
def allergy_data():

    if session.get('logged_in'):


        if session.get('first_login'):
            form = forms.AllergyDataForm()
            immunotherapy_form = forms.AllergyDataImmunotherapyForm()

            if form.validate_on_submit() and immunotherapy_form.is_submitted():
                lib.FirstLogin.insert_allergy_data_to_db(form, immunotherapy_form, LOGGER)
                return redirect(url_for('allergy_settings.allergy_symptoms'))

            form.immunotherapy.data = 'Select from above'
            return render_template('allergy_settings/allergy_data.html', title='Allergy', form=form, immunotherapy_form=immunotherapy_form)

        else:
            form = forms.AllergyDataForm()
            immunotherapy_form = forms.AllergyDataImmunotherapyForm()

            if request.method == 'GET':
                LOGGER.debug('GET Request')
                return render_template('allergy_settings/allergy_data.html', title='Allergy', form=form, immunotherapy_form=immunotherapy_form)

            elif request.method == 'POST':
                LOGGER.debug('POST Request')
                if form.is_submitted() and immunotherapy_form.is_submitted():
                    lib.UpdateSettings.insert_allergy_data_to_db(form, immunotherapy_form, LOGGER)
                    return redirect(url_for('allergy_settings.allergy_data'))

    else:
        LOGGER.warning('No authorized user tried to access the allergy settings page!')
        flash('Please log in to access this page.', 'dark')
        return redirect(url_for('users.login'))


@allergy_settings.route("/allergy_symptoms", methods=['GET', 'POST'])
def allergy_symptoms():

    if session.get('logged_in'):


        if session.get('first_login'):
            form = forms.AllergySymptomsForm()

            if form.validate_on_submit():
                lib.FirstLogin.insert_allergy_symptoms_to_db(form, LOGGER)
                return redirect(url_for('allergy_settings.allergens'))

            return render_template('allergy_settings/allergy_symptoms.html', title='Allergy', form=form)

        else:
            form = forms.AllergySymptomsForm()

            if request.method == 'GET':
                LOGGER.debug('GET Request')
                return render_template('allergy_settings/allergy_symptoms.html', title='Allergy', form=form)

            elif request.method == 'POST':
                LOGGER.debug('POST Request')
                if form.is_submitted():
                    lib.UpdateSettings.insert_allergy_symptoms_to_db(form, LOGGER)
                    return redirect(url_for('allergy_settings.allergy_symptoms'))
            

    else:
        LOGGER.warning('No authorized user tried to access the allergy symptoms page!')
        flash('Please log in to access this page.', 'dark')
        return redirect(url_for('users.login'))


data_required = {'error': 'This field is required.'}
@allergy_settings.route("/allergens", methods=['GET', 'POST'])
def allergens():

    if session.get('logged_in'):


        if session.get('first_login'):
            form = forms.AllergensForm()
            if form.is_submitted() and (form.allergens1.data or form.allergens2.data or form.allergens3.data):
                lib.FirstLogin.insert_allergens_to_db(form, LOGGER)
                return redirect(url_for('allergy_settings.medicines'))
            return render_template('allergy_settings/allergens.html', title='Allergy', form=form, data_required=data_required)

        else:

            form = forms.AllergensForm()

            if request.method == 'GET':
                LOGGER.debug('GET Request')
                return render_template('allergy_settings/allergens.html', title='Allergy', form=form)

            elif request.method == 'POST':
                LOGGER.debug('POST Request')
                if form.is_submitted():
                    lib.UpdateSettings.insert_allergens_to_db(form, LOGGER)
                    return redirect(url_for('allergy_settings.allergens'))
            

    else:
        LOGGER.warning('No authorized user tried to access the allergens page!')
        flash('Please log in to access this page.', 'dark')
        return redirect(url_for('users.login'))


@allergy_settings.route("/medicines", methods=['GET', 'POST'])
def medicines():

    if session.get('logged_in'):


        if session.get('first_login'):
            form_0 = forms.MedicinesForm()

            if form_0.validate_on_submit():
                lib.FirstLogin.insert_medicines_to_db(form_0, LOGGER)
                return redirect(url_for('allergy_settings.vas_tool'))
            return render_template('allergy_settings/medicines.html', title='Allergy', form_0=form_0)

        else:
            form_0 = forms.MedicinesForm()
            form_1 = forms.ClearMedicinesForm1()
            form_2 = forms.ClearMedicinesForm2()
            form_3 = forms.ClearMedicinesForm3()
            form_4 = forms.ClearMedicinesForm4()
            form_5 = forms.ClearMedicinesForm5()


            if request.method == 'GET':
                LOGGER.debug('GET Request')
                return render_template('allergy_settings/medicines.html', title='Allergy', form_0=form_0, form_1=form_1, form_2=form_2, form_3=form_3, form_4=form_4, form_5=form_5)

            elif request.method == 'POST':
                LOGGER.debug('POST Request')

                if form_1.clear_allergic_rhinitis_nose.data:
                    lib.UpdateSettings.delete_medicines_from_db(form_1.clear_allergic_rhinitis_nose, 'allergic rhinitis - nose', LOGGER)
                    return redirect(url_for('allergy_settings.medicines'))
                elif form_2.clear_allergic_rhinitis_mouth.data:
                    lib.UpdateSettings.delete_medicines_from_db(form_2.clear_allergic_rhinitis_mouth, 'allergic rhinitis - mouth', LOGGER)
                    return redirect(url_for('allergy_settings.medicines'))
                elif form_3.clear_allergic_rhinitis_injection.data:
                    lib.UpdateSettings.delete_medicines_from_db(form_3.clear_allergic_rhinitis_injection, 'allergic rhinitis - injection', LOGGER)
                    return redirect(url_for('allergy_settings.medicines'))
                elif form_4.clear_allergic_asthma_mouth.data:
                    lib.UpdateSettings.delete_medicines_from_db(form_4.clear_allergic_asthma_mouth, 'allergic asthma - mouth', LOGGER)
                    return redirect(url_for('allergy_settings.medicines'))
                elif form_5.clear_allergic_conjunctivitis_drops.data:
                    lib.UpdateSettings.delete_medicines_from_db(form_5.clear_allergic_conjunctivitis_drops, 'allergic conjunctivitis - drops', LOGGER)
                    return redirect(url_for('allergy_settings.medicines'))

                if form_0.is_submitted():
                    lib.UpdateSettings.insert_medicines_to_db(form_0, LOGGER)
                    return redirect(url_for('allergy_settings.medicines'))

    else:
        LOGGER.warning('No authorized user tried to access the medicines page!')
        flash('Please log in to access this page.', 'dark')
        return redirect(url_for('users.login'))


@allergy_settings.route("/vas_tool", methods=['GET', 'POST'])
def vas_tool():
         
    if session.get('logged_in'):


        if session.get('first_login'):
                form = VasToolForm()

                if form.is_submitted():
                    lib.FirstLogin.insert_vas_info_to_db(form, LOGGER)

                    if check_if_all_settings_exist():
                        session['first_login'] = False
                        return redirect(url_for('users.profile'))
                    else:
                        flash('Please re-login, but first complete all the allergy forms!', 'danger')
                        return redirect(url_for('users.logout'))
                        
                return render_template('allergy_settings/vas_tool.html', title='Vas Tool', form=form)

        else:
            requested_page = '404'
            return render_template('errors/404.html', requested_page=requested_page)


    else:
        requested_page = '404'
        return render_template('errors/404.html', requested_page=requested_page)
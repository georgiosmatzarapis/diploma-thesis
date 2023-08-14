from flask import render_template, url_for, flash, redirect, request, session, Blueprint
from backend.web.database_api import UserInsertManager, UserUpdateManager, UserFindManager
from backend.web.lib import check_if_all_settings_exist
from datetime import datetime, timedelta

class FirstLogin:
    """
    Class which contains functions about the insertion of user's allergy & vas info, while first log-in.
    """


    def insert_allergy_data_to_db(form, immunotherapy_form, LOGGER):
        LOGGER.debug(f'ALLERGY DATA INFO: {form.gender.data}, {form.family_history.data}, {form.allergic_rhinitis.data}, {form.allergic_asthma.data}, \
                                          {form.allergic_conjunctivitis.data}, {form.allergy_frequency.data}, {form.allergy_affection.data}, \
                                          {form.immunotherapy.data}, {immunotherapy_form.immunotherapy_start_date.data},{form.medicine_days.data}, {form.medicine_weeks.data}')
        
        immunotherapy_message1 = 'No given date'
        immunotherapy_message2 = 'Not receiving immunotherapy'

        if ((immunotherapy_form.immunotherapy_start_date.data == None and form.immunotherapy.data == 'Sublingual (drops, tablets, nebulisation)') or 
           (immunotherapy_form.immunotherapy_start_date.data == None and form.immunotherapy.data == 'Injection') or 
           (immunotherapy_form.immunotherapy_start_date.data == None and form.immunotherapy.data == 'Other')):
            UserInsertManager.insert_allergy_data_without_immunotherapy_date(session.get('email'), form.gender.data, form.family_history.data, form.allergic_rhinitis.data, form.allergic_asthma.data, 
                                        form.allergic_conjunctivitis.data, form.allergy_frequency.data, form.allergy_affection.data, form.immunotherapy.data, 
                                        immunotherapy_message1, form.medicine_days.data, form.medicine_weeks.data)

        elif (immunotherapy_form.immunotherapy_start_date.data == None and form.immunotherapy.data == 'Not receiving immunotherapy'):
            UserInsertManager.insert_allergy_data_without_immunotherapy_date(session.get('email'), form.gender.data, form.family_history.data, form.allergic_rhinitis.data, form.allergic_asthma.data, 
                                        form.allergic_conjunctivitis.data, form.allergy_frequency.data, form.allergy_affection.data, form.immunotherapy.data, 
                                        immunotherapy_message2, form.medicine_days.data, form.medicine_weeks.data)

        else:
            UserInsertManager.insert_allergy_data(session.get('email'), form.gender.data, form.family_history.data, form.allergic_rhinitis.data, form.allergic_asthma.data, 
                                        form.allergic_conjunctivitis.data, form.allergy_frequency.data, form.allergy_affection.data, form.immunotherapy.data, 
                                        immunotherapy_form.immunotherapy_start_date.data, form.medicine_days.data, form.medicine_weeks.data)

    def insert_allergy_symptoms_to_db(form, LOGGER):
        LOGGER.debug(f'ALLERGY SYMPTOMS INFO: {form.allergy_symptoms.data}')
        UserInsertManager.insert_allergy_symptoms(session.get('email'), form.allergy_symptoms.data)

    def insert_allergens_to_db(form, LOGGER):
        LOGGER.debug(f'ALLERGY SYMPTOMS INFO: {form.allergens1.data}, {form.allergens2.data}, {form.allergens3.data}')

        submitted_allergens = []
        for data in form.allergens1.data:
            submitted_allergens.append(data)

        for data in form.allergens2.data:
            submitted_allergens.append(data)

        for data in form.allergens3.data:
            submitted_allergens.append(data)

        UserInsertManager.insert_allergens(session.get('email'), submitted_allergens)

    def insert_medicines_to_db(form_0, LOGGER):
        LOGGER.debug(f'{form_0.allergic_rhinitis_nose.data}, {form_0.allergic_rhinitis_mouth.data}, {form_0.allergic_rhinitis_injection.data}, \
                    {form_0.allergic_asthma_mouth.data}, {form_0.allergic_conjunctivitis_drops.data}')

        UserInsertManager.insert_medicines(session.get('email'), form_0.allergic_rhinitis_nose.data, form_0.allergic_rhinitis_mouth.data,
                            form_0.allergic_rhinitis_injection.data, form_0.allergic_asthma_mouth.data, form_0.allergic_conjunctivitis_drops.data)
    
    def insert_vas_info_to_db(form, LOGGER):
        LOGGER.debug(f'{form.today_symptoms.data}, {form.rhinitis_symptoms_today.data}, {form.asthma_symptoms_today.data}, \
                       {form.conjunctivitis_symptoms_today.data}, {form.work_school_today.data}, {form.work_affection.data}, {datetime.utcnow()}')

        user_time = datetime.utcnow()
        work_school_state = 'No work/school today'
        location_state = 'No location given'

        if form.work_school_today.data == 'Yes':
            UserInsertManager.insert_vas_without_geolocation(session.get('email'), form.today_symptoms.data, form.rhinitis_symptoms_today.data, form.asthma_symptoms_today.data,
                                   form.conjunctivitis_symptoms_today.data, form.work_school_today.data, form.work_affection.data, location_state, user_time)

        elif form.work_school_today.data == 'No':
            UserInsertManager.insert_vas_without_geolocation(session.get('email'), form.today_symptoms.data, form.rhinitis_symptoms_today.data, form.asthma_symptoms_today.data,
                                   form.conjunctivitis_symptoms_today.data, form.work_school_today.data, work_school_state, location_state, user_time)

        if check_if_all_settings_exist():
            flash('Settings successfully completed!', 'success')



class UpdateSettings:
    """
    Class which contains functions about the update/delete of user's allergy infos.
    """

    def insert_allergy_data_to_db(form, immunotherapy_form, LOGGER):
        LOGGER.debug(f'ALLERGY DATA INFO: {form.gender.data}, {form.family_history.data}, {form.allergic_rhinitis.data}, {form.allergic_asthma.data}, \
                                          {form.allergic_conjunctivitis.data}, {form.allergy_frequency.data}, {form.allergy_affection.data}, \
                                          {form.immunotherapy.data}, {immunotherapy_form.immunotherapy_start_date.data},{form.medicine_days.data}, {form.medicine_weeks.data}')

        # VALUES BEFORE UPDATE
        current_gender = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'gender')
        current_family_history = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'family history')
        current_allergic_rhinitis = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergic rhinitis')
        current_allergic_asthma = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergic asthma')
        current_allergic_conjunctivitis = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergic conjunctivitis')
        current_allergy_frequency = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergy frequency')
        current_allergy_affection = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'allergy affection')
        current_immunotherapy = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'immunotherapy')
        current_immunotherapy_start_date = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'immunotherapy start date')
        current_medicine_days = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'medicine days')
        current_medicine_weeks = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Data', 'medicine weeks')
        LOGGER.debug(f'{current_gender}, {current_family_history}, {current_allergic_rhinitis}, {current_allergic_conjunctivitis}, {current_allergy_frequency}, {current_allergy_affection}, {current_immunotherapy}, {current_immunotherapy_start_date}, {current_medicine_days}, {current_medicine_weeks}')

        if form.gender.data != 'None':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'gender', form.gender.data)

        if form.family_history.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'family history', form.family_history.data)

        if form.allergic_rhinitis.data != 'None':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'allergic rhinitis', form.allergic_rhinitis.data)

        if form.allergic_asthma.data != 'None':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'allergic asthma', form.allergic_asthma.data)

        if form.allergic_conjunctivitis.data != 'None':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'allergic conjunctivitis', form.allergic_conjunctivitis.data)

        if form.allergy_frequency.data != 'None':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'allergy frequency', form.allergy_frequency.data)

        if form.allergy_affection.data != []:
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'allergy affection', form.allergy_affection.data)

        if form.immunotherapy.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'immunotherapy', form.immunotherapy.data)

        if (immunotherapy_form.immunotherapy_start_date.data != None) and (form.immunotherapy.data != 'Not receiving immunotherapy'):
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'immunotherapy start date', immunotherapy_form.immunotherapy_start_date.data)
        else:
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'immunotherapy start date', 'No given date')

        if form.medicine_days.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'medicine days', form.medicine_days.data)

        if form.medicine_weeks.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Data', 'medicine weeks', form.medicine_weeks.data)

        if ((((form.gender.data != 'None') and (current_gender != form.gender.data)) or 
           ((form.family_history.data != '0') and (current_family_history != form.family_history.data)) or 
           ((form.allergic_rhinitis.data != 'None') and (current_allergic_rhinitis != form.allergic_rhinitis.data)) or
           ((form.allergic_asthma.data != 'None') and (current_allergic_asthma != form.allergic_asthma.data)) or
           ((form.allergic_conjunctivitis.data != 'None') and (current_allergic_conjunctivitis != form.allergic_conjunctivitis.data)) or
           ((form.allergy_frequency.data != 'None') and (current_allergy_frequency != form.allergy_frequency.data)) or 
           ((form.allergy_affection.data != []) and (current_allergy_affection != form.allergy_affection.data)) or
           ((form.immunotherapy.data != '0') and (current_immunotherapy != form.immunotherapy.data)) or 
           ((immunotherapy_form.immunotherapy_start_date.data != None) and (current_immunotherapy_start_date != immunotherapy_form.immunotherapy_start_date.data)) or
           ((form.medicine_days.data != '0') and (current_medicine_days != form.medicine_days.data)) or 
           ((form.medicine_weeks.data != '0') and (current_medicine_weeks != form.medicine_weeks.data)))):
        
            flash('Allergy data have changed', 'info')


    def insert_allergy_symptoms_to_db(form, LOGGER):
        LOGGER.debug(f'ALLERGY SYMPTOMS INFO: {form.allergy_symptoms.data}')
        current_symptoms = UserFindManager.find_allergy_info(session.get('email'), 'Allergy Symptoms', 'symptoms')

        if (form.allergy_symptoms.data != []) and (current_symptoms != form.allergy_symptoms.data):
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergy Symptoms', 'symptoms', form.allergy_symptoms.data)
            flash('Allergy symptoms have changed', 'info')


    def insert_allergens_to_db(form, LOGGER):

        submitted_allergens = []
        for data in form.allergens1.data:
            submitted_allergens.append(data)

        for data in form.allergens2.data:
            submitted_allergens.append(data)

        for data in form.allergens3.data:
            submitted_allergens.append(data)

        LOGGER.debug(f'ALLERGENS INFO: {submitted_allergens}')
        current_allergens = UserFindManager.find_allergy_info(session.get('email'), 'Allergens', 'allergens')
        # LOGGER.debug(f'{current_allergens}')
        

        if (submitted_allergens != []) and (current_allergens != submitted_allergens):
            UserUpdateManager.update_allergy_info(session.get('email'), 'Allergens', 'allergens', submitted_allergens)
            flash('Allergens have changed', 'info')
            

    def insert_medicines_to_db(form_0, LOGGER):
        LOGGER.debug(f'UP {form_0.allergic_rhinitis_nose.data}, {form_0.allergic_rhinitis_mouth.data}, {form_0.allergic_rhinitis_injection.data}, {form_0.allergic_asthma_mouth.data}, {form_0.allergic_conjunctivitis_drops.data}')

        current_allergic_rhinitis_nose = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - nose')
        current_allergic_rhinitis_mouth = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - mouth')
        current_allergic_rhinitis_injection = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - injection')
        current_allergic_asthma_mouth = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic asthma - mouth')
        current_allergic_conjunctivitis_drops = UserFindManager.find_allergy_info(session.get('email'), 'Medicines', 'allergic conjunctivitis - drops')
        LOGGER.debug(f'UP {current_allergic_rhinitis_nose}, {current_allergic_rhinitis_mouth}, {current_allergic_rhinitis_injection}, {current_allergic_asthma_mouth}, {current_allergic_conjunctivitis_drops}')


        if form_0.allergic_rhinitis_nose.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - nose', form_0.allergic_rhinitis_nose.data)
        
        if form_0.allergic_rhinitis_mouth.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - mouth', form_0.allergic_rhinitis_mouth.data)

        if form_0.allergic_rhinitis_injection.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Medicines', 'allergic rhinitis - injection', form_0.allergic_rhinitis_injection.data)

        if form_0.allergic_asthma_mouth.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Medicines', 'allergic asthma - mouth', form_0.allergic_asthma_mouth.data)

        if form_0.allergic_conjunctivitis_drops.data != '0':
            UserUpdateManager.update_allergy_info(session.get('email'), 'Medicines', 'allergic conjunctivitis - drops', form_0.allergic_conjunctivitis_drops.data)


        if ((((form_0.allergic_rhinitis_nose.data != '0') and (current_allergic_rhinitis_nose != form_0.allergic_rhinitis_nose.data)) or 
           ((form_0.allergic_rhinitis_mouth.data != '0') and (current_allergic_rhinitis_mouth != form_0.allergic_rhinitis_mouth.data)) or 
           ((form_0.allergic_rhinitis_injection.data != '0') and (current_allergic_rhinitis_injection != form_0.allergic_rhinitis_injection.data)) or 
           ((form_0.allergic_asthma_mouth.data != '0') and (current_allergic_asthma_mouth != form_0.allergic_asthma_mouth.data)) or
           ((form_0.allergic_conjunctivitis_drops.data != '0') and (current_allergic_conjunctivitis_drops != form_0.allergic_conjunctivitis_drops.data)))):

           flash('Medicines have changed', 'info')


    def delete_medicines_from_db(complete_form_name, db_update_key, LOGGER):
        form_label = complete_form_name.label
        LOGGER.debug(f'{form_label}, {complete_form_name.data}')
        
        if UserFindManager.find_allergy_info(session.get('email'), 'Medicines', db_update_key) == 'No medicine':
            flash('No data to delete', 'warning')
        else:
            UserUpdateManager.delete_medicine_info(session.get('email'), 'Medicines', db_update_key)
            flash('Medicine deleted', 'success')
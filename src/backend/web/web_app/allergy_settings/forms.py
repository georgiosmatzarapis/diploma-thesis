""" Forms related with allergy settings. """
from flask_wtf import FlaskForm
from wtforms import (SubmitField, RadioField, SelectMultipleField, SelectField, widgets)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, StopValidation
from wtforms.fields.html5 import DateField
from backend.configs.forms_choices_config import AllergyDataFormChoices, AllergySymptomsFormChoices, AllergensFormChoices, MedicinesFormChoices


class MultiCheckboxField(SelectMultipleField):
    
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AllergyDataForm(FlaskForm):
    """
    Class which initializes forms related with allergy data. 
    """

    gender = RadioField('Gender:', validators=[DataRequired()],
                        choices=AllergyDataFormChoices.GENDER)

    family_history = SelectField('Anyone in family has a history of allergy?', default=0, validators=[DataRequired()],
                                 choices=AllergyDataFormChoices.FAMILY_HISTORY)

    allergic_rhinitis = RadioField('Do you have Allergic Rhinitis?', validators=[DataRequired()],
                                   choices=AllergyDataFormChoices.ALLERGIC_RHINITIS)

    allergic_asthma = RadioField('Do you have Allergic Asthma?', validators=[DataRequired()],
                                   choices=AllergyDataFormChoices.ALLERGIC_ASTHMA)

    allergic_conjunctivitis = RadioField('Do you have Allergic Conjunctivitis?', validators=[DataRequired()],
                                         choices=AllergyDataFormChoices.ALLERGIC_CONJUNCTIVITIS)

    allergy_frequency = RadioField('How often my Allergy affects me:', validators=[DataRequired()],
                                   choices=AllergyDataFormChoices.ALLERGY_FREQUENCY)

    allergy_affection = MultiCheckboxField('How my Allergy affects me:', validators=[DataRequired()],
                                            choices=AllergyDataFormChoices.ALLERGY_AFFECTION)

    immunotherapy = SelectField('In which way do you receive Immunotherapy?', default=0, validators=[DataRequired()],
                                choices=AllergyDataFormChoices.IMMUNOTHERAPY)

    medicine_days = SelectField('How many days a week you use medicines when needed?', default=0, validators=[DataRequired()],
                                choices=AllergyDataFormChoices.MEDICINE_DAYS)

    medicine_weeks = SelectField('How many weeks you use medicines when needed?', default=0, validators=[DataRequired()],
                                 choices=AllergyDataFormChoices.MEDICINE_WEEKS)

    submit = SubmitField('Update Allergy Data')


class AllergyDataImmunotherapyForm(FlaskForm):
    """
    Class which initializes form related with start date of immunotherapy. 
    """

    immunotherapy_start_date = DateField('Since when do you receive Immunotherapy?', format='%Y-%m-%d')
    

class AllergySymptomsForm(FlaskForm):
    """
    Class which initializes forms related with allergy symptoms. 
    """

    allergy_symptoms = MultiCheckboxField('Check your personal Allergy Symptoms:', validators=[DataRequired()],
                                           choices=AllergySymptomsFormChoices.ALLERGY_SYMPTOMS_POLLEN_COM)

    submit = SubmitField('Update Allergy Symptoms')


class AllergensForm(FlaskForm):   
    """
    Class which initializes forms related with allergens. 
    """

    allergens1 = MultiCheckboxField('Check your personal Allergen:', 
                                    choices=AllergensFormChoices.ALLERGENS_SUBLIST_1)    

    allergens2 = MultiCheckboxField(choices=AllergensFormChoices.ALLERGENS_SUBLIST_2) 

    allergens3 = MultiCheckboxField(choices=AllergensFormChoices.ALLERGENS_SUBLIST_3)  

    submit = SubmitField('Update Allergens')


class MedicinesForm(FlaskForm):   
    """
    Class which initializes forms related with medicines. 
    """

    allergic_rhinitis_nose = SelectField('Nose:', default=0, validators=[DataRequired()],
                                choices=MedicinesFormChoices.ALLERGIC_RHINITIS_NOSE)

    allergic_rhinitis_mouth = SelectField('Mouth:', default=0, validators=[DataRequired()],
                                choices=MedicinesFormChoices.ALLERGIC_RHINITIS_MOUTH)

    allergic_rhinitis_injection = SelectField('Injection:', default=0, validators=[DataRequired()],
                                choices=MedicinesFormChoices.ALLERGIC_RHINITIS_INJECTION)

    allergic_asthma_mouth = SelectField('Mouth:', default=0, validators=[DataRequired()],
                                choices=MedicinesFormChoices.ALLERGIC_ASTHMA_MOUTH)

    allergic_conjunctivitis_drops = SelectField('Drops:', default=0, validators=[DataRequired()],
                                choices=MedicinesFormChoices.ALLERGIC_CONJUNCTIVITIS_DROPS)

    submit = SubmitField('Update Medicines')


class ClearMedicinesForm1(FlaskForm):   
    """
    Class which initializes form related with medicine deletion. 
    """

    clear_allergic_rhinitis_nose = SubmitField('Yes')


class ClearMedicinesForm2(FlaskForm):
    """
    Class which initializes form related with medicine deletion. 
    """

    clear_allergic_rhinitis_mouth = SubmitField('Yes')


class ClearMedicinesForm3(FlaskForm):
    """
    Class which initializes form related with medicine deletion. 
    """

    clear_allergic_rhinitis_injection = SubmitField('Yes')


class ClearMedicinesForm4(FlaskForm):
    """
    Class which initializes form related with medicine deletion. 
    """

    clear_allergic_asthma_mouth = SubmitField('Yes')


class ClearMedicinesForm5(FlaskForm):
    """
    Class which initializes form related with medicine deletion. 
    """

    clear_allergic_conjunctivitis_drops = SubmitField('Yes')
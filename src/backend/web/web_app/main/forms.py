from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from wtforms.fields.html5 import IntegerRangeField

from backend.configs.forms_choices_config import VasToolFormChoices, AllergensFormChoices, HomeAllergensFormChoices


class MultiCheckboxField(SelectMultipleField):
    
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SensorMapForm(FlaskForm):
    """
    Class which initializes forms about user's choise for sensor allergy maps at home page.
    """

    selected_time = SelectField('Time Interval:', default=0, choices=HomeAllergensFormChoices.TIME_INTERVAL)

    allergens_1 = MultiCheckboxField('Allergens:', choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_1)    

    allergens_2 = MultiCheckboxField(choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_2) 

    allergens_3 = MultiCheckboxField(choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_3)  


class VASMapForm(FlaskForm):
    """
    Class which initializes forms about user's choise for mcs allergy maps at home page.
    """

    selected_time = SelectField('Time Interval:', default=0, choices=HomeAllergensFormChoices.TIME_INTERVAL)

    allergens_1 = MultiCheckboxField('Allergens:', choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_1)    

    allergens_2 = MultiCheckboxField(choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_2) 

    allergens_3 = MultiCheckboxField(choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_3) 


class TwitterMapForm(FlaskForm):
    """
    Class which initializes time interval form about user's choise for twitter map at home page.
    """

    selected_time = SelectField('Time Interval:', default=0, choices=HomeAllergensFormChoices.TIME_INTERVAL_TWITTER)


class HybridMCSMapForm(FlaskForm):
    """
    Class which initializes forms about user's choise for mcs allergy maps at home page.
    """

    selected_time = SelectField('Time Interval:', default=0, choices=HomeAllergensFormChoices.TIME_INTERVAL)

    allergens_1 = MultiCheckboxField('Allergens:', choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_1)    

    allergens_2 = MultiCheckboxField(choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_2) 

    allergens_3 = MultiCheckboxField(choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_3)


class HybridMapForm(FlaskForm):
    """
    Class which initializes forms about user's choise for mcs allergy maps at home page.
    """

    selected_time = SelectField('Time Interval:', default=0, choices=HomeAllergensFormChoices.TIME_INTERVAL)

    allergens_1 = MultiCheckboxField('Allergens:', choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_1)    

    allergens_2 = MultiCheckboxField(choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_2) 

    allergens_3 = MultiCheckboxField(choices=HomeAllergensFormChoices.ALLERGENS_SUBLIST_3)


class HumidityMapForm(FlaskForm):
    """
    Class which initializes time interval form about user's choise for humidity map at home page.
    """

    selected_time = SelectField('Time Interval:', default=0, choices=HomeAllergensFormChoices.TIME_INTERVAL)


class VasToolForm(FlaskForm):
    """
    Class which initializes forms related with vas tool. 
    """

    today_symptoms = IntegerRangeField('Symptoms today?', default=6)

    rhinitis_symptoms_today = IntegerRangeField('Rhinitis symptoms today?', default=6)
    
    asthma_symptoms_today = IntegerRangeField('Asthma symptoms today?', default=6)

    conjunctivitis_symptoms_today = IntegerRangeField('Conjunctivitis (eyes) symptoms today?', default=6)

    work_school_today = SelectField('Work/School today?', default='Yes', choices=VasToolFormChoices.WORK_SCHOOL_TODAY)

    work_affection = IntegerRangeField('Allergy symptoms affect your work today?', default=6)

    submit = SubmitField('Submit Symptoms', default=False)


class MyAllergyMapForm(FlaskForm):
    """
    Class which initializes forms related with MyAllergyMap. 
    """
    
    time_interval = SelectField('Time Interval:', default=0, choices=VasToolFormChoices.TIME_INTERVAL)
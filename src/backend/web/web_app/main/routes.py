""" Routes about main functionality of the page. """
from flask import render_template, request, redirect, url_for, session, flash, Blueprint, make_response, jsonify
from datetime import datetime, timedelta

from backend.helpers.main_config import CONFIGURATION
from backend.web.web_app.main import forms
from backend import lg


LOGGER = lg.get_logger(__name__)
main = Blueprint('main', __name__)
google_maps_api_key = CONFIGURATION.gmaps_api_key
leaflet_map_tile = CONFIGURATION.leaflet_map_tile

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():

    if session.get('logged_in'):
        

        if session.get('first_login'):
            LOGGER.debug(f'session state: {session}')
            return render_template('allergy_settings/warning.html', title='Warning')

        else:
            vas_form = forms.VasToolForm()
            sensor_map_form = forms.SensorMapForm()
            vas_map_form = forms.VASMapForm()
            twitter_map_form = forms.TwitterMapForm()
            hybrid_mcs_map_form = forms.HybridMCSMapForm()
            hybrid_map_form = forms.HybridMapForm()
            humidity_map_form = forms.HumidityMapForm()
            LOGGER.debug(f'session state: {session}')
            requested_page = 'home'
            return render_template('main/home.html', title='Home', requested_page=requested_page, vas_form=vas_form,  
                                                    sensor_map_form=sensor_map_form, vas_map_form=vas_map_form,
                                                    twitter_map_form=twitter_map_form, hybrid_mcs_map_form=hybrid_mcs_map_form,
                                                    hybrid_map_form=hybrid_map_form, humidity_map_form=humidity_map_form, 
                                                    google_maps_api_key=google_maps_api_key, leaflet_map_tile=leaflet_map_tile)

    else:
        sensor_map_form = forms.SensorMapForm()
        vas_map_form = forms.VASMapForm()
        twitter_map_form = forms.TwitterMapForm()
        hybrid_mcs_map_form = forms.HybridMCSMapForm()
        hybrid_map_form = forms.HybridMapForm()
        humidity_map_form = forms.HumidityMapForm()
        LOGGER.debug(f'session state: {session}')
        requested_page = 'home'
        return render_template('main/home.html', title='Home', requested_page=requested_page, sensor_map_form=sensor_map_form, 
                                                vas_map_form=vas_map_form, twitter_map_form=twitter_map_form, 
                                                hybrid_mcs_map_form=hybrid_mcs_map_form, hybrid_map_form=hybrid_map_form, 
                                                humidity_map_form=humidity_map_form, google_maps_api_key=google_maps_api_key, 
                                                leaflet_map_tile=leaflet_map_tile)
    

@main.route("/allergy")
def allergy():

    if session.get('logged_in'):

        if session.get('first_login'):
            return render_template('allergy_settings/warning.html', title='Warning')

        else:
            requested_page = 'allergy'
            return render_template('main/allergy.html', title='Allergy', requested_page=requested_page)

    else:
        requested_page = 'allergy'
        return render_template('main/allergy.html', title='Allergy', requested_page=requested_page)


@main.route("/about")
def about():

    if session.get('logged_in'):

        if session.get('first_login'):
            return render_template('allergy_settings/warning.html', title='Warning')

        else:
            requested_page = 'about'
            return render_template('main/about.html', title='About', requested_page=requested_page)

    else:
        requested_page = 'about'
        return render_template('main/about.html', title='About', requested_page=requested_page)
    

@main.route("/myhealth")
def myhealth():

    if session.get('logged_in'):

        if session.get('first_login'):
            return render_template('allergy_settings/warning.html', title='Warning')

        else:
            form = forms.MyAllergyMapForm()
            requested_page = 'myhealth'
            return render_template('main/myHealth.html', title='myHealth', form=form, google_maps_api_key=google_maps_api_key, requested_page=requested_page)
    
    else:
        LOGGER.warning('No authorized user tried to access the allergens page!')
        flash('Please log in to access this page.', 'dark')
        return redirect(url_for('users.login'))

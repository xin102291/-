from flask import Flask
import sys
import os
from App.route import *

def create_app(app):
    # app = Flask(__name__,static_folder="static", static_url_path="/")
    app.add_url_rule('/', 'login', login)
    app.add_url_rule('/login', 'login', login)
    app.add_url_rule('/home', 'home', home)
    app.add_url_rule('/patient_personal_info', 'patient_personal_info', patient_personal_info)
    app.add_url_rule('/patient_test_results', 'patient_test_results', patient_test_results)
    app.add_url_rule('/patient_medical_records', 'patient_medical_records', patient_medical_records)
    app.add_url_rule('/patient_medications', 'patient_medications', patient_medications)
    app.add_url_rule('/patient_medical_documents', 'patient_medical_documents', patient_medical_documents)
    app.add_url_rule('/dashboard', 'dashboard', patient_dashboard)
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/signup', 'signup', signup)
    app.add_url_rule('/realtime_encryption','realtime_encryption',realtime_encryption)
    return app


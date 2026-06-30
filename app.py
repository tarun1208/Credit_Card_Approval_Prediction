# ==========================================================
# CREDIT CARD APPROVAL PREDICTION SYSTEM
# Flask Backend
# ==========================================================

# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

import time

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

import pandas as pd
import numpy as np
import joblib

# ==========================================================
# CREATE FLASK APPLICATION
# ==========================================================

app = Flask(__name__)

app.secret_key = "credit_card_prediction"

# ==========================================================
# LOAD TRAINED MODEL
# ==========================================================

print("=" * 60)
print("Loading Machine Learning Models...")
print("=" * 60)

model = joblib.load("models/best_model.pkl")

print("Best Model Loaded")

scaler = joblib.load("models/scaler.pkl")

print("Scaler Loaded")

label_encoders = joblib.load("models/label_encoders.pkl")
print("=" * 60)

for col, le in label_encoders.items():
    print(col)
    print(le.classes_)
    print()

print("=" * 60)
print("Label Encoders Loaded")

feature_columns = joblib.load("models/feature_columns.pkl")

print("Feature Columns Loaded")

print("=" * 60)
print("Application Started Successfully")
print("=" * 60)

# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def home():

    return render_template("home.html")


# ==========================================================
# ABOUT PAGE
# ==========================================================

@app.route("/about")
def about():

    return render_template("about.html")


# ==========================================================
# PREDICTION PAGE (GET)
# ==========================================================

@app.route("/predict", methods=["GET"])
def predict():

    return render_template("predict.html")


# ==========================================================
# RESULT PAGE (POST)
# ==========================================================

@app.route("/result", methods=["POST"])
def result():

    try:

        print("=" * 60)
        print("Receiving Customer Details...")
        print("=" * 60)

        # ---------------------------------------------
        # Personal Information
        # ---------------------------------------------

        gender = request.form["CODE_GENDER"]

        age = int(request.form["AGE"])

        family_members = float(request.form["CNT_FAM_MEMBERS"])

        children = int(request.form["CNT_CHILDREN"])

        family_status = request.form["NAME_FAMILY_STATUS"]

        housing_type = request.form["NAME_HOUSING_TYPE"]


        # ---------------------------------------------
        # Employment Information
        # ---------------------------------------------

        income_type = request.form["NAME_INCOME_TYPE"]

        education = request.form["NAME_EDUCATION_TYPE"]

        occupation = request.form["OCCUPATION_TYPE"]

        employed_years = int(request.form["EMPLOYED_YEARS"])

        annual_income = float(request.form["AMT_INCOME_TOTAL"])

        income_per_person = float(request.form["INCOME_PER_PERSON"])


        # ---------------------------------------------
        # Financial Information
        # ---------------------------------------------

        own_house = request.form["FLAG_OWN_REALTY"]

        own_car = request.form["FLAG_OWN_CAR"]

        child_ratio = float(request.form["CHILD_RATIO"])


        # ---------------------------------------------
        # Contact Information
        # ---------------------------------------------

        mobile = int(request.form["FLAG_MOBIL"])

        work_phone = int(request.form["FLAG_WORK_PHONE"])

        phone = int(request.form["FLAG_PHONE"])

        email = int(request.form["FLAG_EMAIL"])

        print("Customer Details Received Successfully")

                # ==========================================================
        # FEATURE ENGINEERING
        # ==========================================================

        # Convert Age back to DAYS_BIRTH
        days_birth = -(age * 365)

        # Convert Employment Years back to DAYS_EMPLOYED
        days_employed = -(employed_years * 365)

        # ==========================================================
        # CREATE INPUT DATAFRAME
        # ==========================================================

        input_data = pd.DataFrame({

            "CODE_GENDER": [gender],

            "FLAG_OWN_CAR": [own_car],

            "FLAG_OWN_REALTY": [own_house],

            "CNT_CHILDREN": [children],

            "AMT_INCOME_TOTAL": [annual_income],

            "NAME_INCOME_TYPE": [income_type],

            "NAME_EDUCATION_TYPE": [education],

            "NAME_FAMILY_STATUS": [family_status],

            "NAME_HOUSING_TYPE": [housing_type],

            "DAYS_BIRTH": [days_birth],

            "DAYS_EMPLOYED": [days_employed],

            "FLAG_MOBIL": [mobile],

            "FLAG_WORK_PHONE": [work_phone],

            "FLAG_PHONE": [phone],

            "FLAG_EMAIL": [email],

            "OCCUPATION_TYPE": [occupation],

            "CNT_FAM_MEMBERS": [family_members],

            "AGE": [age],

            "EMPLOYED_YEARS": [employed_years],

            "INCOME_PER_PERSON": [income_per_person],

            "CHILD_RATIO": [child_ratio]

        })

        print("=" * 60)
        print("Input Data Created")
        print(input_data)
        print("=" * 60)

        # ==========================================================
        # LABEL ENCODING
        # ==========================================================

        categorical_columns = [

            "CODE_GENDER",

            "FLAG_OWN_CAR",

            "FLAG_OWN_REALTY",

            "NAME_INCOME_TYPE",

            "NAME_EDUCATION_TYPE",

            "NAME_FAMILY_STATUS",

            "NAME_HOUSING_TYPE",

            "OCCUPATION_TYPE"

        ]

        for column in categorical_columns:

            input_data[column] = label_encoders[column].transform(
                input_data[column]
            )

        print("Categorical Encoding Completed")

        # ==========================================================
        # ARRANGE FEATURES IN TRAINING ORDER
        # ==========================================================

        input_data = input_data[feature_columns]

        print("Feature Order Verified")

                # ==========================================================
        # SCALE NUMERICAL FEATURES
        # ==========================================================

        numerical_columns = [

            "AMT_INCOME_TOTAL",

            "CNT_FAM_MEMBERS",

            "AGE",

            "EMPLOYED_YEARS",

            "INCOME_PER_PERSON",

            "CHILD_RATIO"

        ]

        input_data[numerical_columns] = scaler.transform(
            input_data[numerical_columns]
        )

        print("=" * 60)
        print("Feature Scaling Completed")
        print("=" * 60)

        # ==========================================================
        # MODEL PREDICTION
        # ==========================================================

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(input_data)

        approval_probability = round(
            probability[0][1] * 100,
            2
        )

        rejection_probability = round(
            probability[0][0] * 100,
            2
        )

        print("=" * 60)
        print("Prediction Completed")
        print("=" * 60)

        print("Prediction :", prediction)
        print("Approval Probability :", approval_probability)
        print("Rejection Probability :", rejection_probability)

        # ==========================================================
        # RISK LEVEL
        # ==========================================================

        if approval_probability >= 80:

            risk_level = "LOW"

            risk_color = "success"

        elif approval_probability >= 50:

            risk_level = "MEDIUM"

            risk_color = "warning"

        else:

            risk_level = "HIGH"

            risk_color = "danger"

        print("=" * 60)
        print("Risk Level :", risk_level)
        print("=" * 60)

                # ==========================================================
        # CUSTOMER SUMMARY
        # ==========================================================

        customer_summary = {

            "Gender": gender,

            "Age": age,

            "Annual Income": annual_income,

            "Income Type": income_type,

            "Education": education,

            "Occupation": occupation,

            "Employment Years": employed_years,

            "Family Members": family_members,

            "Children": children,

            "Housing": housing_type

        }

        print("=" * 60)
        print("Customer Summary Created")
        print(customer_summary)
        print("=" * 60)

        # ==========================================================
        # DISPLAY PREDICTION MESSAGE
        # ==========================================================

        if prediction == 1:

            prediction_text = "Approved"

        else:

            prediction_text = "Rejected"

        print("Prediction Result :", prediction_text)

        # ==========================================================
        # RETURN RESULT PAGE
        # ==========================================================
        import time

        time.sleep(60)
        return render_template(

    "result.html",

    prediction=prediction,

    prediction_text=prediction_text,

    probability=approval_probability,

    rejection_probability=rejection_probability,

    risk_level=risk_level,

    risk_color=risk_color,

    customer=customer_summary

)
        # ==========================================================
    # ERROR HANDLING
    # ==========================================================

    except Exception as e:
        print("=" * 80)
        print("APPLICATION ERROR")
        print(e)
        print("=" * 80)

        return f"<h2>Error</h2><pre>{e}</pre>"


# ==========================================================
# PAGE NOT FOUND (404)
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html"

    ), 404


# ==========================================================
# INTERNAL SERVER ERROR (500)
# ==========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return render_template(

        "500.html"

    ), 500


# ==========================================================
# RUN FLASK APPLICATION
# ==========================================================

import os

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    print("=" * 60)
    print(" CREDIT CARD APPROVAL PREDICTION SYSTEM ")
    print("=" * 60)

    print(" Flask Server Started")
    print(f" Running on Port : {port}")
    print(" Waiting for Requests...")
    print("=" * 60)

    app.run(

        host="0.0.0.0",

        port=port,

        debug=False

    )
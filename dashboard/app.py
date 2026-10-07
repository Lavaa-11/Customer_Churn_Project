import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from io import BytesIO


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Customer Retention Analytics System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOGIN CREDENTIALS
# ============================================================

USER_CREDENTIALS = {
    "user": "user123"
}

ADMIN_CREDENTIALS = {
    "admin": "admin123"
}


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "prediction_history" not in st.session_state:
    st.session_state["prediction_history"] = []

if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

# Registered users
if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = USER_CREDENTIALS.copy()


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state["logged_in"]:

    st.title("📊 Intelligent Customer Retention Analytics System")

    st.markdown(
        "### Customer Churn Prediction & Retention Decision Support"
    )

    st.markdown("---")

    login_type = st.radio(
        "Select an Option",
        [
            "👤 User Login",
            "📝 New User Registration",
            "🛡️ Admin Login"
        ],
        horizontal=True
    )

    st.markdown("")

    # ========================================================
    # USER LOGIN
    # ========================================================

    if login_type == "👤 User Login":

        st.subheader("👤 User Login")

        username = st.text_input(
            "Username",
            key="user_login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="user_login_password"
        )

        if st.button(
            "🔐 Login as User",
            use_container_width=True
        ):

            registered_users = st.session_state["registered_users"]

            if (
                username in registered_users
                and registered_users[username] == password
            ):

                st.session_state["logged_in"] = True
                st.session_state["user_role"] = "User"
                st.session_state["username"] = username

                st.success("Login successful!")
                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    # ========================================================
    # NEW USER REGISTRATION
    # ========================================================

    elif login_type == "📝 New User Registration":

        st.subheader("📝 New User Registration")

        st.info(
            "Create a new user account to access the "
            "customer churn prediction dashboard."
        )

        new_username = st.text_input(
            "Create Username",
            key="register_username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password"
        )

        if st.button(
            "📝 Register New User",
            use_container_width=True,
            type="primary"
        ):

            registered_users = st.session_state["registered_users"]

            if (
                not new_username.strip()
                or not new_password
                or not confirm_password
            ):

                st.error(
                    "Please fill in all registration fields."
                )

            elif len(new_username.strip()) < 3:

                st.error(
                    "Username must contain at least 3 characters."
                )

            elif len(new_password) < 4:

                st.error(
                    "Password must contain at least 4 characters."
                )

            elif new_password != confirm_password:

                st.error(
                    "Password and Confirm Password do not match."
                )

            elif new_username.strip() in registered_users:

                st.error(
                    "Username already exists. "
                    "Please choose another username."
                )

            elif new_username.strip() in ADMIN_CREDENTIALS:

                st.error(
                    "This username is reserved. "
                    "Please choose another username."
                )

            else:

                registered_users[new_username.strip()] = new_password

                st.success(
                    "Registration successful! "
                    "You can now select User Login and log in "
                    "with your new account."
                )

    # ========================================================
    # ADMIN LOGIN
    # ========================================================

    else:

        st.subheader("🛡️ Admin Login")

        username = st.text_input(
            "Admin Username",
            key="admin_login_username"
        )

        password = st.text_input(
            "Admin Password",
            type="password",
            key="admin_login_password"
        )

        if st.button(
            "🔐 Login as Admin",
            use_container_width=True
        ):

            if (
                username in ADMIN_CREDENTIALS
                and ADMIN_CREDENTIALS[username] == password
            ):

                st.session_state["logged_in"] = True
                st.session_state["user_role"] = "Admin"
                st.session_state["username"] = username

                st.success("Admin login successful!")
                st.rerun()

            else:

                st.error(
                    "Invalid admin username or password."
                )

    st.markdown("---")

    st.info(
        "Use User Login for customer churn prediction, "
        "New User Registration to create a new account, "
        "or Admin Login to access administrative analytics."
    )

    st.stop()


# ============================================================
# CURRENT USER INFORMATION
# ============================================================

current_role = st.session_state["user_role"]
current_username = st.session_state["username"]


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        text-align: center;
    }

    .factor-card {
        background-color: #fff8e1;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin-bottom: 10px;
    }

    .alert-box {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }

    .low-risk {
        background-color: #e8f5e9;
        border-left: 6px solid #4caf50;
    }

    .medium-risk {
        background-color: #fff8e1;
        border-left: 6px solid #ffc107;
    }

    .high-risk {
        background-color: #ffebee;
        border-left: 6px solid #f44336;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📊 Retention Analytics")

    st.markdown("---")

    st.subheader("👤 Current User")

    st.write(f"**Username:** {current_username}")
    st.write(f"**Role:** {current_role}")

    st.markdown("---")

    st.subheader("🔐 Permissions")

    if current_role == "Admin":

        st.success("✓ Customer Prediction")
        st.success("✓ Risk Analysis")
        st.success("✓ Retention Strategy")
        st.success("✓ What-If Simulation")
        st.success("✓ Prediction History")
        st.success("✓ Analytics")
        st.success("✓ Reports")

    else:

        st.success("✓ Customer Prediction")
        st.success("✓ Risk Analysis")
        st.success("✓ Retention Strategy")
        st.success("✓ What-If Simulation")

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["username"] = None
        st.session_state["last_result"] = None

        st.rerun()

    st.markdown("---")

    st.subheader("🤖 AI Model")

    st.write("**Model:** Logistic Regression")

    st.write("**Risk Thresholds:**")

    st.write("🟢 Low Risk: < 40%")
    st.write("🟡 Medium Risk: 40% – 70%")
    st.write("🔴 High Risk: > 70%")

    st.markdown("---")

    st.subheader("📌 Available Features")

    st.write("• Customer Profile")
    st.write("• Service Information")
    st.write("• Contract & Billing")
    st.write("• Churn Probability")
    st.write("• Risk Factors")
    st.write("• Retention Strategy")
    st.write("• Revenue at Risk")
    st.write("• What-If Simulation")

    if current_role == "Admin":

        st.write("• Prediction History")
        st.write("• Analytics")
        st.write("• CSV / Excel Reports")


# ============================================================
# MAIN HEADER
# ============================================================

st.title("📊 Intelligent Customer Retention Analytics System")

st.markdown(
    "### AI-Powered Customer Churn Prediction & Retention Decision Support"
)

if current_role == "Admin":

    st.success(
        f"🛡️ Admin Dashboard | Logged in as **{current_username}**"
    )

else:

    st.info(
        f"👤 User Dashboard | Logged in as **{current_username}**"
    )


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "logistic_regression_model.joblib"
)

PREPROCESSING_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "preprocessing.joblib"
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model_and_preprocessing():

    model = joblib.load(MODEL_PATH)
    preprocessing_data = joblib.load(PREPROCESSING_PATH)

    return model, preprocessing_data


try:

    model, preprocessing_data = load_model_and_preprocessing()

except Exception as e:

    st.error(
        "Unable to load the trained model or preprocessing file."
    )

    st.code(str(e))

    st.info(
        "Please check that the following files exist:\n"
        "models/logistic_regression_model.joblib\n"
        "models/preprocessing.joblib"
    )

    st.stop()


# ============================================================
# CREATE INPUT DATAFRAME
# ============================================================

def create_input_dataframe(
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract,
    paperless_billing,
    payment_method,
    monthly_charges,
    total_charges
):

    input_data = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    return pd.DataFrame([input_data])


# ============================================================
# PREPROCESS INPUT
# ============================================================

def preprocess_input(input_df):

    processed_input = pd.get_dummies(
        input_df,
        drop_first=True,
        dtype=int
    )

    feature_columns = preprocessing_data["feature_columns"]

    processed_input = processed_input.reindex(
        columns=feature_columns,
        fill_value=0
    )

    imputer = preprocessing_data["imputer"]

    processed_input = imputer.transform(
        processed_input
    )

    return processed_input


# ============================================================
# GENERATE RISK FACTORS
# ============================================================

def generate_risk_factors(
    contract,
    payment_method,
    tenure,
    monthly_charges,
    internet_service,
    online_security,
    tech_support,
    partner,
    dependents
):

    factors = []

    if contract == "Month-to-month":
        factors.append(
            "Month-to-month contract indicates lower customer commitment."
        )

    if payment_method == "Electronic check":
        factors.append(
            "Electronic check payment method is associated with higher churn risk."
        )

    if tenure < 12:
        factors.append(
            "Customer has relatively short tenure."
        )

    if monthly_charges >= 80:
        factors.append(
            "Higher monthly charges may increase churn sensitivity."
        )

    if internet_service == "Fiber optic":
        factors.append(
            "Fiber optic service customers may require closer retention monitoring."
        )

    if online_security == "No":
        factors.append(
            "Customer does not have online security service."
        )

    if tech_support == "No":
        factors.append(
            "Customer does not have technical support service."
        )

    if partner == "No" and dependents == "No":
        factors.append(
            "Customer has no partner or dependents in the account."
        )

    if len(factors) == 0:

        factors.append(
            "No major rule-based risk factors were identified."
        )

    return factors


# ============================================================
# GENERATE RETENTION RECOMMENDATION
# ============================================================

def generate_recommendation(
    risk_level,
    contract,
    payment_method,
    tenure,
    monthly_charges,
    internet_service,
    online_security,
    tech_support
):

    recommendations = []

    if risk_level == "High Risk":

        recommendations.append(
            "Offer a personalized retention discount or loyalty incentive."
        )

        recommendations.append(
            "Encourage migration from a month-to-month contract to a longer-term contract."
        )

        recommendations.append(
            "Provide proactive customer support to address possible service concerns."
        )

        recommendations.append(
            "Consider technical support or security service bundles where relevant."
        )

        recommendations.append(
            "Review billing and payment experience with the customer."
        )

    elif risk_level == "Medium Risk":

        recommendations.append(
            "Provide a personalized customer engagement offer."
        )

        recommendations.append(
            "Offer loyalty benefits to strengthen customer relationship."
        )

        recommendations.append(
            "Encourage a longer-term contract through suitable incentives."
        )

        recommendations.append(
            "Consider security and technical support add-ons."
        )

    else:

        recommendations.append(
            "Maintain regular customer engagement."
        )

        recommendations.append(
            "Provide loyalty rewards to encourage continued retention."
        )

        recommendations.append(
            "Continue monitoring customer satisfaction and service usage."
        )

        recommendations.append(
            "Maintain proactive communication with the customer."
        )

    return recommendations


# ============================================================
# CUSTOMER INFORMATION
# ============================================================

st.markdown("---")
st.header("👤 Customer Information")

col1, col2, col3 = st.columns(3)

with col1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        [0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes"
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

with col2:

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        max_value=100,
        value=12,
        step=1
    )

with col3:

    monthly_charges = st.number_input(
        "Monthly Charges ($)",
        min_value=0.0,
        max_value=500.0,
        value=70.0,
        step=1.0
    )

    total_charges = st.number_input(
        "Total Charges ($)",
        min_value=0.0,
        max_value=100000.0,
        value=float(monthly_charges * tenure),
        step=10.0
    )


# ============================================================
# CUSTOMER FINANCIAL SUMMARY
# ============================================================

financial_col1, financial_col2, financial_col3 = st.columns(3)

estimated_annual_revenue = monthly_charges * 12

estimated_customer_lifetime_revenue = (
    monthly_charges * max(tenure, 1)
)

with financial_col1:

    st.metric(
        "Estimated Annual Revenue",
        f"${estimated_annual_revenue:,.2f}"
    )

with financial_col2:

    st.metric(
        "Customer Lifetime Revenue",
        f"${estimated_customer_lifetime_revenue:,.2f}"
    )

with financial_col3:

    st.metric(
        "Tenure",
        f"{tenure} months"
    )


# ============================================================
# SERVICE INFORMATION
# ============================================================

st.markdown("---")
st.header("📡 Service Information")

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# PHONE SERVICE
# ------------------------------------------------------------

with col1:

    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"],
        key="phone_service"
    )

    if phone_service == "Yes":

        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["Yes", "No"],
            key="multiple_lines_yes"
        )

    else:

        multiple_lines = "No phone service"

        st.selectbox(
            "Multiple Lines",
            ["No phone service"],
            index=0,
            disabled=True,
            key="multiple_lines_no"
        )


# ------------------------------------------------------------
# INTERNET SERVICE
# ------------------------------------------------------------

    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"],
        key="internet_service"
    )


# ------------------------------------------------------------
# ONLINE SECURITY
# ------------------------------------------------------------

    if internet_service == "No":

        online_security = "No internet service"

        st.selectbox(
            "Online Security",
            ["No internet service"],
            index=0,
            disabled=True,
            key="online_security_no"
        )

    else:

        online_security = st.selectbox(
            "Online Security",
            ["Yes", "No"],
            key="online_security_yes"
        )


# ============================================================
# INTERNET-RELATED SERVICES
# ============================================================

with col2:

    if internet_service == "No":

        online_backup = "No internet service"

        st.selectbox(
            "Online Backup",
            ["No internet service"],
            index=0,
            disabled=True,
            key="online_backup_no"
        )

    else:

        online_backup = st.selectbox(
            "Online Backup",
            ["Yes", "No"],
            key="online_backup_yes"
        )


    if internet_service == "No":

        device_protection = "No internet service"

        st.selectbox(
            "Device Protection",
            ["No internet service"],
            index=0,
            disabled=True,
            key="device_protection_no"
        )

    else:

        device_protection = st.selectbox(
            "Device Protection",
            ["Yes", "No"],
            key="device_protection_yes"
        )


    if internet_service == "No":

        tech_support = "No internet service"

        st.selectbox(
            "Tech Support",
            ["No internet service"],
            index=0,
            disabled=True,
            key="tech_support_no"
        )

    else:

        tech_support = st.selectbox(
            "Tech Support",
            ["Yes", "No"],
            key="tech_support_yes"
        )


# ============================================================
# STREAMING SERVICES
# ============================================================

with col3:

    if internet_service == "No":

        streaming_tv = "No internet service"

        st.selectbox(
            "Streaming TV",
            ["No internet service"],
            index=0,
            disabled=True,
            key="streaming_tv_no"
        )

    else:

        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No"],
            key="streaming_tv_yes"
        )


    if internet_service == "No":

        streaming_movies = "No internet service"

        st.selectbox(
            "Streaming Movies",
            ["No internet service"],
            index=0,
            disabled=True,
            key="streaming_movies_no"
        )

    else:

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No"],
            key="streaming_movies_yes"
        )


# ============================================================
# CONTRACT AND BILLING
# ============================================================

st.markdown("---")
st.header("💳 Contract & Billing")

col1, col2, col3 = st.columns(3)

with col1:

    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

with col2:

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

with col3:

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )


# ============================================================
# PREDICTION BUTTON
# ============================================================

st.markdown("---")

predict_button = st.button(
    "🔮 Predict Customer Churn Risk",
    use_container_width=True,
    type="primary"
)


# ============================================================
# PREDICTION PROCESS
# ============================================================

if predict_button:

    try:

        input_df = create_input_dataframe(
            gender=gender,
            senior_citizen=senior_citizen,
            partner=partner,
            dependents=dependents,
            tenure=tenure,
            phone_service=phone_service,
            multiple_lines=multiple_lines,
            internet_service=internet_service,
            online_security=online_security,
            online_backup=online_backup,
            device_protection=device_protection,
            tech_support=tech_support,
            streaming_tv=streaming_tv,
            streaming_movies=streaming_movies,
            contract=contract,
            paperless_billing=paperless_billing,
            payment_method=payment_method,
            monthly_charges=monthly_charges,
            total_charges=total_charges
        )

        processed_input = preprocess_input(
            input_df
        )

        prediction = model.predict(
            processed_input
        )[0]

        churn_probability = model.predict_proba(
            processed_input
        )[0][1]

        risk_percentage = churn_probability * 100


        # ----------------------------------------------------
        # RISK CLASSIFICATION
        # ----------------------------------------------------

        if risk_percentage < 40:

            risk_level = "Low Risk"

        elif risk_percentage <= 70:

            risk_level = "Medium Risk"

        else:

            risk_level = "High Risk"


        # ----------------------------------------------------
        # REVENUE AT RISK
        # ----------------------------------------------------

        monthly_revenue_at_risk = (
            monthly_charges * churn_probability
        )

        annual_revenue_at_risk = (
            monthly_charges * 12 * churn_probability
        )


        # ----------------------------------------------------
        # PREDICTION CERTAINTY
        # ----------------------------------------------------

        prediction_certainty = (
            max(
                churn_probability,
                1 - churn_probability
            ) * 100
        )


        # ----------------------------------------------------
        # RISK FACTORS
        # ----------------------------------------------------

        risk_factors = generate_risk_factors(
            contract=contract,
            payment_method=payment_method,
            tenure=tenure,
            monthly_charges=monthly_charges,
            internet_service=internet_service,
            online_security=online_security,
            tech_support=tech_support,
            partner=partner,
            dependents=dependents
        )


        # ----------------------------------------------------
        # RETENTION RECOMMENDATIONS
        # ----------------------------------------------------

        recommendations = generate_recommendation(
            risk_level=risk_level,
            contract=contract,
            payment_method=payment_method,
            tenure=tenure,
            monthly_charges=monthly_charges,
            internet_service=internet_service,
            online_security=online_security,
            tech_support=tech_support
        )


        # ----------------------------------------------------
        # RESULT OBJECT
        # ----------------------------------------------------

        result = {
            "Timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Username": current_username,
            "Role": current_role,
            "Prediction": (
                "Churn"
                if prediction == 1
                else "Stay"
            ),
            "Churn Probability": churn_probability,
            "Risk Percentage": risk_percentage,
            "Risk Level": risk_level,
            "Prediction Certainty": prediction_certainty,
            "Monthly Charges": monthly_charges,
            "Annual Revenue at Risk": annual_revenue_at_risk,
            "Contract": contract,
            "Payment Method": payment_method,
            "Tenure": tenure
        }


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        st.session_state["last_result"] = {
            "prediction": prediction,
            "churn_probability": churn_probability,
            "risk_percentage": risk_percentage,
            "risk_level": risk_level,
            "prediction_certainty": prediction_certainty,
            "monthly_revenue_at_risk": monthly_revenue_at_risk,
            "annual_revenue_at_risk": annual_revenue_at_risk,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "input_df": input_df,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }


        # ----------------------------------------------------
        # ADD TO HISTORY
        # ----------------------------------------------------

        st.session_state["prediction_history"].append(
            result
        )

        st.success(
            "Customer churn prediction completed successfully."
        )

    except Exception as e:

        st.error(
            "An error occurred while generating the prediction."
        )

        st.code(str(e))


# ============================================================
# DISPLAY LAST PREDICTION
# ============================================================

if st.session_state["last_result"] is not None:

    result = st.session_state["last_result"]

    prediction = result["prediction"]

    churn_probability = result["churn_probability"]

    risk_percentage = result["risk_percentage"]

    risk_level = result["risk_level"]

    prediction_certainty = result["prediction_certainty"]

    monthly_revenue_at_risk = result[
        "monthly_revenue_at_risk"
    ]

    annual_revenue_at_risk = result[
        "annual_revenue_at_risk"
    ]

    risk_factors = result["risk_factors"]

    recommendations = result["recommendations"]


    # ========================================================
    # PREDICTION RESULT
    # ========================================================

    st.markdown("---")
    st.header("🎯 Prediction Result")


    if prediction == 1:

        st.markdown(
            """
            <div class="alert-box high-risk">
                🔴 Customer Likely to Churn
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="alert-box low-risk">
                🟢 Customer Likely to Stay
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Churn Probability",
            f"{risk_percentage:.2f}%"
        )

    with col2:

        st.metric(
            "Risk Level",
            risk_level
        )

    with col3:

        st.metric(
            "Prediction Certainty",
            f"{prediction_certainty:.2f}%"
        )

    with col4:

        st.metric(
            "Annual Revenue at Risk",
            f"${annual_revenue_at_risk:,.2f}"
        )


    # ========================================================
    # PROBABILITY BAR
    # ========================================================

    st.subheader("📈 Churn Probability")

    st.progress(
        min(
            max(churn_probability, 0.0),
            1.0
        )
    )

    st.write(
        f"Estimated probability of churn: "
        f"**{risk_percentage:.2f}%**"
    )


    # ========================================================
    # CUSTOMER PROFILE
    # ========================================================

    st.markdown("---")
    st.subheader("👤 Customer Profile")

    profile_col1, profile_col2, profile_col3 = st.columns(3)

    with profile_col1:

        st.write(f"**Gender:** {gender}")

        st.write(
            f"**Senior Citizen:** "
            f"{'Yes' if senior_citizen == 1 else 'No'}"
        )

        st.write(f"**Partner:** {partner}")

        st.write(f"**Dependents:** {dependents}")

    with profile_col2:

        st.write(f"**Tenure:** {tenure} months")

        st.write(
            f"**Phone Service:** {phone_service}"
        )

        st.write(
            f"**Multiple Lines:** {multiple_lines}"
        )

        st.write(
            f"**Internet Service:** {internet_service}"
        )

    with profile_col3:

        st.write(f"**Contract:** {contract}")

        st.write(
            f"**Monthly Charges:** ${monthly_charges:,.2f}"
        )

        st.write(
            f"**Total Charges:** ${total_charges:,.2f}"
        )

        st.write(
            f"**Payment Method:** {payment_method}"
        )


    # ========================================================
    # REVENUE ANALYTICS
    # ========================================================

    st.markdown("---")
    st.subheader("💰 Revenue Risk Analytics")

    revenue_col1, revenue_col2, revenue_col3 = st.columns(3)

    with revenue_col1:

        st.metric(
            "Monthly Revenue at Risk",
            f"${monthly_revenue_at_risk:,.2f}"
        )

    with revenue_col2:

        st.metric(
            "Annual Revenue at Risk",
            f"${annual_revenue_at_risk:,.2f}"
        )

    with revenue_col3:

        st.metric(
            "Monthly Customer Value",
            f"${monthly_charges:,.2f}"
        )


    # ========================================================
    # RISK FACTORS
    # ========================================================

    st.markdown("---")
    st.subheader("⚠️ Explainable Risk Factors")

    for factor in risk_factors:

        st.markdown(
            f"""
            <div class="factor-card">
                ⚠️ {factor}
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # RETENTION STRATEGY
    # ========================================================

    st.markdown("---")
    st.subheader("🎯 Recommended Retention Strategy")

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        st.write(
            f"**{index}.** {recommendation}"
        )


# ============================================================
# WHAT-IF SIMULATOR
# ============================================================

if st.session_state["last_result"] is not None:

    st.markdown("---")
    st.header("🔄 What-If Retention Simulator")

    st.write(
        "Change the contract or payment method to estimate "
        "how the churn probability could change."
    )

    whatif_col1, whatif_col2 = st.columns(2)

    with whatif_col1:

        whatif_contract = st.selectbox(
            "What-If Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ],
            index=[
                "Month-to-month",
                "One year",
                "Two year"
            ].index(contract),
            key="whatif_contract"
        )

    with whatif_col2:

        payment_options = [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]

        whatif_payment = st.selectbox(
            "What-If Payment Method",
            payment_options,
            index=payment_options.index(
                payment_method
            ),
            key="whatif_payment"
        )


    if st.button(
        "🔄 Run What-If Analysis",
        use_container_width=True
    ):

        try:

            whatif_df = create_input_dataframe(
                gender=gender,
                senior_citizen=senior_citizen,
                partner=partner,
                dependents=dependents,
                tenure=tenure,
                phone_service=phone_service,
                multiple_lines=multiple_lines,
                internet_service=internet_service,
                online_security=online_security,
                online_backup=online_backup,
                device_protection=device_protection,
                tech_support=tech_support,
                streaming_tv=streaming_tv,
                streaming_movies=streaming_movies,
                contract=whatif_contract,
                paperless_billing=paperless_billing,
                payment_method=whatif_payment,
                monthly_charges=monthly_charges,
                total_charges=total_charges
            )

            whatif_processed = preprocess_input(
                whatif_df
            )

            whatif_probability = model.predict_proba(
                whatif_processed
            )[0][1]

            whatif_percentage = (
                whatif_probability * 100
            )

            original_percentage = risk_percentage

            probability_difference = (
                whatif_percentage
                - original_percentage
            )


            st.markdown("---")
            st.subheader("📊 What-If Result")

            wcol1, wcol2, wcol3 = st.columns(3)

            with wcol1:

                st.metric(
                    "Original Churn Probability",
                    f"{original_percentage:.2f}%"
                )

            with wcol2:

                st.metric(
                    "What-If Churn Probability",
                    f"{whatif_percentage:.2f}%"
                )

            with wcol3:

                st.metric(
                    "Probability Difference",
                    f"{probability_difference:+.2f}%"
                )


            if probability_difference < 0:

                st.success(
                    "The selected What-If scenario shows a lower "
                    "estimated churn probability."
                )

            elif probability_difference > 0:

                st.warning(
                    "The selected What-If scenario shows a higher "
                    "estimated churn probability."
                )

            else:

                st.info(
                    "The selected What-If scenario produces the "
                    "same estimated churn probability."
                )


        except Exception as e:

            st.error(
                "Unable to run the What-If analysis."
            )

            st.code(str(e))


# ============================================================
# ADMIN PREDICTION HISTORY
# ============================================================

st.markdown("---")

if current_role == "Admin":

    st.header("🛡️ Admin Analytics & Prediction History")

    history = st.session_state["prediction_history"]

    if len(history) == 0:

        st.info(
            "No prediction history is available yet."
        )

    else:

        history_df = pd.DataFrame(history)

        st.subheader("📋 Prediction History")

        display_df = history_df.copy()

        if "Churn Probability" in display_df.columns:

            display_df["Churn Probability"] = (
                display_df["Churn Probability"] * 100
            ).round(2)

        if "Risk Percentage" in display_df.columns:

            display_df["Risk Percentage"] = (
                display_df["Risk Percentage"]
            ).round(2)

        if "Prediction Certainty" in display_df.columns:

            display_df["Prediction Certainty"] = (
                display_df["Prediction Certainty"]
            ).round(2)

        st.dataframe(
            display_df,
            use_container_width=True
        )


        # ====================================================
        # ADMIN ANALYTICS
        # ====================================================

        st.markdown("---")
        st.subheader("📊 Analytics")

        analytics_col1, analytics_col2, analytics_col3, analytics_col4 = (
            st.columns(4)
        )

        total_predictions = len(history_df)

        churn_count = (
            history_df["Prediction"]
            .eq("Churn")
            .sum()
        )

        stay_count = (
            history_df["Prediction"]
            .eq("Stay")
            .sum()
        )

        average_probability = (
            history_df["Churn Probability"]
            .mean() * 100
        )


        with analytics_col1:

            st.metric(
                "Total Predictions",
                total_predictions
            )

        with analytics_col2:

            st.metric(
                "Predicted Churn",
                churn_count
            )

        with analytics_col3:

            st.metric(
                "Predicted Stay",
                stay_count
            )

        with analytics_col4:

            st.metric(
                "Average Churn Probability",
                f"{average_probability:.2f}%"
            )


        # ====================================================
        # RISK LEVEL DISTRIBUTION
        # ====================================================

        st.markdown("---")
        st.subheader("⚠️ Risk Level Distribution")

        risk_distribution = (
            history_df["Risk Level"]
            .value_counts()
            .reset_index()
        )

        risk_distribution.columns = [
            "Risk Level",
            "Customers"
        ]

        st.dataframe(
            risk_distribution,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # REPORT DOWNLOADS
        # ====================================================

        st.markdown("---")
        st.subheader("📥 Download Reports")


        # ----------------------------------------------------
        # CSV REPORT
        # ----------------------------------------------------

        csv_data = history_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Download CSV Report",
            data=csv_data,
            file_name="customer_churn_prediction_report.csv",
            mime="text/csv",
            use_container_width=True
        )


        # ----------------------------------------------------
        # EXCEL REPORT
        # ----------------------------------------------------

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            history_df.to_excel(
                writer,
                index=False,
                sheet_name="Prediction History"
            )

            risk_distribution.to_excel(
                writer,
                index=False,
                sheet_name="Risk Distribution"
            )

        excel_buffer.seek(0)

        st.download_button(
            label="📊 Download Excel Report",
            data=excel_buffer,
            file_name="customer_churn_prediction_report.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True
        )


        # ====================================================
        # CLEAR HISTORY
        # ====================================================

        st.markdown("---")

        if st.button(
            "🗑️ Clear Prediction History",
            use_container_width=True
        ):

            st.session_state["prediction_history"] = []

            st.success(
                "Prediction history cleared successfully."
            )

            st.rerun()


else:

    st.info(
        "🔒 Prediction history and administrative analytics "
        "are available only to Admin users."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "📊 Intelligent Customer Retention Analytics System | "
    "AI-powered churn prediction and retention decision support"
)

st.caption(
    "⚠️ Predictions are estimates intended to support "
    "customer retention decisions and should not be treated "
    "as guaranteed outcomes."
)
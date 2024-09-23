import streamlit as st
from datetime import datetime
from chatbot import get_response, symptom_checker
from utils import (
    add_user, add_symptom, add_appointment, add_medication,
    get_user, get_symptoms, get_appointments, get_medications, check_user_exists
)
from database import initialize_database
import matplotlib.pyplot as plt
import plotly.express as px

# Initialize database
initialize_database()

# Function to handle responses and update context
def handle_request(context, question):
    try:
        response = get_response(context, question)
        return response
    except Exception as e:
        return f"Error processing request: {e}"

# Streamlit app layout
st.set_page_config(page_title="Healthcare Chatbot 🤖", layout="wide")

# Title and description
st.title("Healthcare Chatbot 🤖")
st.write("Welcome to our advanced healthcare chatbot. Ask me anything related to healthcare, symptoms, appointments, and more! 💬")

# Initialize session state for conversation history and context
if 'context' not in st.session_state:
    st.session_state.context = ""
if 'history' not in st.session_state:
    st.session_state.history = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Sidebar navigation
st.sidebar.header("Navigation 📋")
option = st.sidebar.radio(
    "Select a section:",
    ("Chat with Bot", "Manage User", "Log Symptom", "Schedule Appointment", "Manage Medication", "Symptom Checker", "Health Monitoring", "EHR Integration", "History")
)

# Main content area
if option == "Chat with Bot":
    st.header("Chat with Bot 💬")
    user_question = st.text_input("Ask your question 🤔:")
    ask_button = st.button("Ask")

    if ask_button and user_question:
        response = handle_request(st.session_state.context, user_question)
        st.write(f"**You asked:** 🤔 {user_question}")
        st.write(f"**Chatbot says:** 🤖 {response}")

        # Update context and history with the new interaction
        st.session_state.context += f"\nUser: {user_question}\nChatbot: {response}"
        st.session_state.history.append({
            "section": "Chat with Bot",
            "question": user_question,
            "response": response
        })

    # Display the chat history for the current session
    st.subheader("Chat History 📜")
    for entry in st.session_state.history:
        if entry["section"] == "Chat with Bot":
            st.write(f"**You asked:** 🤔 {entry['question']}")
            st.write(f"**Chatbot says:** 🤖 {entry['response']}")

elif option == "Manage User":
    st.header("Manage User Details 🏥")

    with st.form(key='user_form'):
        st.write("### User Details 📝")
        user_name = st.text_input("Name 👤")
        user_email = st.text_input("Email ✉️")
        user_phone = st.text_input("Phone Number 📞")
        submit_user = st.form_submit_button("Save User Details 💾")
        if submit_user:
            try:
                existing_user_id = check_user_exists(user_email)
                if existing_user_id:
                    st.session_state.user_id = existing_user_id
                    st.write("User already registered! ✅")
                else:
                    st.session_state.user_id = add_user(user_name, user_email, user_phone)
                    st.write("User details saved successfully! ✅")
                st.session_state.history.append({
                    "section": "Manage User",
                    "question": "Saved User Details",
                    "response": f"Name: {user_name}, Email: {user_email}, Phone: {user_phone}"
                })
            except Exception as e:
                st.write(f"Error saving user details: {e}")

elif option == "Log Symptom":
    if st.session_state.user_id:
        st.header("Log Symptom 📝")

        with st.form(key='symptom_form'):
            symptom_description = st.text_input("Symptom Description 🩺")
            symptom_assessment = st.text_area("Assessment Result 🧪")
            submit_symptom = st.form_submit_button("Save Symptom 💾")
            if submit_symptom:
                try:
                    add_symptom(st.session_state.user_id, symptom_description, symptom_assessment)
                    st.write("Symptom logged successfully! ✅")
                    st.session_state.history.append({
                        "section": "Log Symptom",
                        "question": "Logged Symptom",
                        "response": f"Description: {symptom_description}, Assessment: {symptom_assessment}"
                    })
                except Exception as e:
                    st.write(f"Error logging symptom: {e}")
    else:
        st.write("Please register or select a user first.")

elif option == "Schedule Appointment":
    if st.session_state.user_id:
        st.header("Schedule Appointment 📅")

        with st.form(key='appointment_form'):
            doctor_name = st.text_input("Doctor's Name 👨‍⚕️")
            appointment_date = st.date_input("Appointment Date 🗓️", min_value=datetime.today())
            appointment_time = st.time_input("Appointment Time ⏰", value=datetime.now().time())
            appointment_status = st.selectbox("Appointment Status 🏷️", ["Scheduled", "Completed", "Cancelled"])
            submit_appointment = st.form_submit_button("Save Appointment 💾")
            if submit_appointment:
                try:
                    appointment_datetime = datetime.combine(appointment_date, appointment_time).isoformat()
                    add_appointment(st.session_state.user_id, doctor_name, appointment_datetime, appointment_status)
                    st.write("Appointment scheduled successfully! ✅")
                    st.session_state.history.append({
                        "section": "Schedule Appointment",
                        "question": "Scheduled Appointment",
                        "response": f"Doctor: {doctor_name}, Date: {appointment_datetime}, Status: {appointment_status}"
                    })
                except Exception as e:
                    st.write(f"Error scheduling appointment: {e}")
    else:
        st.write("Please register or select a user first.")

elif option == "Manage Medication":
    if st.session_state.user_id:
        st.header("Manage Medications 💊")

        with st.form(key='medication_form'):
            medication_name = st.text_input("Medication Name 💊")
            dosage = st.text_input("Dosage 💉")
            reminder_time = st.time_input("Reminder Time ⏰", value=datetime.now().time())
            submit_medication = st.form_submit_button("Save Medication 💾")
            if submit_medication:
                try:
                    reminder_time_str = reminder_time.strftime("%H:%M:%S")
                    add_medication(st.session_state.user_id, medication_name, dosage, reminder_time_str)
                    st.write("Medication saved successfully! ✅")
                    st.session_state.history.append({
                        "section": "Manage Medication",
                        "question": "Saved Medication",
                        "response": f"Medication: {medication_name}, Dosage: {dosage}, Reminder: {reminder_time_str}"
                    })
                except Exception as e:
                    st.write(f"Error saving medication: {e}")
    else:
        st.write("Please register or select a user first.")

elif option == "Symptom Checker":
    st.header("Symptom Checker and Triage 🩺")

    with st.form(key='symptom_checker_form'):
        symptom_description = st.text_input("Describe your symptoms:")
        submit_checker = st.form_submit_button("Check Symptoms")
        if submit_checker and symptom_description:
            try:
                result = symptom_checker(symptom_description)
                st.write("### Triage Results")
                st.write(result)
            except Exception as e:
                st.write(f"Error checking symptoms: {e}")

elif option == "Health Monitoring":
    st.header("Health Monitoring and Reminders 📊")

    # Dummy data for health monitoring
    st.write("### Real-Time Health Metrics")
    st.line_chart({
        'Heart Rate': [72, 75, 74, 78, 76, 79, 80],
        'Blood Pressure': [120, 122, 119, 121, 123, 118, 120]
    })

    st.write("### Health Data Visualization")
    fig = plt.figure()
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
    st.pyplot(fig)

elif option == "EHR Integration":
    st.header("EHR Data Integration 📋")

    # Dummy EHR data
    st.write("### EHR Data")
    ehr_data = {
        'Date': ['2023-01-01', '2023-02-01', '2023-03-01'],
        'Appointment': ['Check-up', 'Blood Test', 'X-Ray']
    }
    fig = px.bar(ehr_data, x='Date', y='Appointment', title="EHR Data")
    st.plotly_chart(fig)

elif option == "History":
    st.header("Interaction History 📜")
    st.write("### Full Interaction History 📜")
    for entry in st.session_state.history:
        st.write(f"**Section:** {entry['section']}")
        st.write(f"**Question:** {entry['question']}")
        st.write(f"**Response:** {entry['response']}")
        st.write("---")

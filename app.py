import streamlit as st
from nlp_pipeline import extract_medical_details, perform_sentiment_intent_analysis
from soap_note_generator import generate_soap_note

# Configure the page layout & title
st.set_page_config(page_title="Physician Notetaker AI", layout="centered")

# Inject custom CSS to remove white background and style the chat bubbles
st.markdown(
    """
    <style>
    /* Make the entire page background dark */
    body, .main, .block-container {
        background-color: #1e1e1e !important;
    }
    
    /* Chat bubbles: no background color, white text */
    .chat-bubble-left {
        margin: 10px 0;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
        background-color: transparent;
        color: #ffffff;
    }
    .chat-bubble-right {
        margin: 10px 0;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
        float: right;
        background-color: transparent;
        color: #ffffff;
        text-align: right;
    }
    /* Ensure subsequent elements don't get stuck around the float */
    .clearfix {
        clear: both;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Physician Notetaker AI – Two-Role Chat Interface")

# Initialize session state for chat history if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_message(role: str, text: str):
    """Adds a message (Doctor or Patient) to the session state chat history."""
    st.session_state.chat_history.append({"role": role, "text": text})

# --- Display Chat History ---
for message in st.session_state.chat_history:
    if message["role"] == "Doctor":
        # Doctor bubble: left-aligned
        st.markdown(
            f"""
            <div class="chat-bubble-left">
                <strong>Doctor:</strong> {message['text']}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Patient bubble: right-aligned
        st.markdown(
            f"""
            <div class="chat-bubble-right">
                <strong>Patient:</strong> {message['text']}
            </div>
            <div class="clearfix"></div>
            """,
            unsafe_allow_html=True
        )

# --- User Input Section ---
st.subheader("Enter Your Message")

role = st.radio("Role:", ["Doctor", "Patient"], horizontal=True)
user_input = st.text_input("Type your message here:")

if st.button("Send") and user_input.strip():
    add_message(role, user_input)
    # No need for st.experimental_rerun(); Streamlit re-runs automatically on button click

# --- Buttons for NLP tasks ---
st.write("---")
st.subheader("NLP Processing")

col1, col2 = st.columns(2)

with col1:
    if st.button("Extract Medical Details (From Patient Messages)"):
        # Combine all patient messages into a single 'transcript'
        patient_transcript = "\n".join(
            msg["text"] for msg in st.session_state.chat_history if msg["role"] == "Patient"
        )
        if patient_transcript:
            details = extract_medical_details(patient_transcript)
            st.markdown("**Extracted Medical Details:**")
            st.json(details)
        else:
            st.warning("No patient messages found.")

with col2:
    if st.button("Analyze Sentiment & Intent (Patient)"):
        # Combine all patient messages
        patient_text = "\n".join(
            msg["text"] for msg in st.session_state.chat_history if msg["role"] == "Patient"
        )
        if patient_text:
            sentiment_intent = perform_sentiment_intent_analysis(patient_text)
            st.markdown("**Sentiment & Intent Analysis (Patient):**")
            st.json(sentiment_intent)
        else:
            st.warning("No patient messages found.")

st.write("---")
st.subheader("Generate SOAP Note")

if st.button("Generate SOAP Note (From Patient Transcript)"):
    patient_transcript = "\n".join(
        msg["text"] for msg in st.session_state.chat_history if msg["role"] == "Patient"
    )
    if patient_transcript:
        soap_note = generate_soap_note(patient_transcript)
        st.json(soap_note)
    else:
        st.warning("No patient messages found for SOAP note generation.")

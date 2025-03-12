# nlp_pipeline.py
import spacy
from transformers import pipeline

# Load spaCy model (you can substitute a medical-specific model if available)
nlp = spacy.load("en_core_web_sm")

# Load a sentiment analysis pipeline from Hugging Face
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def extract_medical_details(transcript: str) -> dict:
    """
    Extracts key medical details from the transcript.
    """
    patient_name = "Unknown"
    for token in transcript.split():
        if token.startswith("Ms.") or token.startswith("Mr."):
            patient_name = token.strip(",.")
            break

    symptoms = []
    diagnosis = ""
    treatment = []
    current_status = ""
    prognosis = ""

    # Extracting symptoms based on simple keyword matching
    if "neck" in transcript.lower():
        symptoms.append("Neck pain")
    if "back" in transcript.lower():
        symptoms.append("Back pain")
    if "head" in transcript.lower():
        symptoms.append("Head impact")

    # Diagnosis detection
    if "whiplash" in transcript.lower():
        diagnosis = "Whiplash injury"

    # Treatment detection
    if "physiotherapy" in transcript.lower():
        treatment.append("Physiotherapy sessions")
    if "painkillers" in transcript.lower():
        treatment.append("Painkillers")

    # Status and prognosis
    if "occasional" in transcript.lower():
        current_status = "Occasional pain"
    if "full recovery" in transcript.lower():
        prognosis = "Full recovery expected within six months"
    else:
        prognosis = "Recovery expected"

    return {
        "Patient_Name": patient_name,
        "Symptoms": symptoms,
        "Diagnosis": diagnosis,
        "Treatment": treatment,
        "Current_Status": current_status,
        "Prognosis": prognosis
    }

def perform_sentiment_intent_analysis(patient_text: str) -> dict:
    """
    Performs sentiment and intent analysis on the patient’s text.
    """
    sentiment_result = sentiment_analyzer(patient_text)[0]
    sentiment = "Neutral"
    if sentiment_result["label"] == "NEGATIVE":
        sentiment = "Anxious"
    elif sentiment_result["label"] == "POSITIVE":
        sentiment = "Reassured"

    # Simple rules for intent detection
    intent = "General conversation"
    if "worried" in patient_text.lower() or "concern" in patient_text.lower():
        intent = "Seeking reassurance"
    elif "pain" in patient_text.lower() or "hurt" in patient_text.lower():
        intent = "Reporting symptoms"

    return {
        "Sentiment": sentiment,
        "Intent": intent
    }

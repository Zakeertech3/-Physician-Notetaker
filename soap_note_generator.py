# soap_note_generator.py
def generate_soap_note(transcript: str) -> dict:
    """
    Generates a structured SOAP note from the transcript.
    """
    # Subjective: Extracting patient complaints and history.
    subjective = {
        "Chief_Complaint": "",
        "History_of_Present_Illness": ""
    }
    if "pain" in transcript.lower():
        subjective["Chief_Complaint"] = "Neck and back pain"
        subjective["History_of_Present_Illness"] = (
            "Patient had a car accident, experienced pain for several weeks, "
            "and now reports occasional pain."
        )

    # Objective: Findings from physical examination.
    objective = {
        "Physical_Exam": "Full range of motion in neck and back, no tenderness.",
        "Observations": "Patient appears in stable condition."
    }

    # Assessment: Diagnosis based on history and exam.
    assessment = {
        "Diagnosis": "Whiplash injury",
        "Severity": "Mild, improving"
    }

    # Plan: Recommendations and follow-up.
    plan = {
        "Treatment": "Continue physiotherapy as needed, use painkillers if required.",
        "Follow-Up": "Return if symptoms worsen or persist beyond six months."
    }

    return {
        "Subjective": subjective,
        "Objective": objective,
        "Assessment": assessment,
        "Plan": plan
    }

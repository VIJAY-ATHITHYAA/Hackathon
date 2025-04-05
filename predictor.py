import google.generativeai as genai

# Initialize Gemini with your API key
genai.configure(api_key="AIzaSyA2byhZ6SP-ychVIeye29Qsc8iH6q9hIwo")  # Replace with your actual key

# Load the generative model
model = genai.GenerativeModel("gemini-pro")


def predict_risk(age, weight, medical_history):
    risk = {
        "diabetes": "Low",
        "hypertension": "Low",
        "heart_disease": "Low"
    }

    if int(age) > 45 or "family_diabetes" in medical_history:
        risk["diabetes"] = "High"
    if int(weight) > 90 or "smoking" in medical_history:
        risk["heart_disease"] = "Moderate"
    if "stress" in medical_history or int(age) > 50:
        risk["hypertension"] = "Moderate"

    return risk


def check_symptoms(symptoms_list):
    symptoms_text = ', '.join(symptoms_list)

    prompt = (
        f"A patient reports the following symptoms: {symptoms_text}. "
        f"Suggest the 3 most likely health conditions based on general medical knowledge. "
        f"Keep the explanation simple and beginner-friendly."
    )

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
        return reply.split('\n') if '\n' in reply else [reply]

    except Exception as e:
        return [f"Error fetching suggestions: {str(e)}"]

from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# ✅ Configure Gemini API key
genai.configure(api_key="AIzaSyA2byhZ6SP-ychVIeye29Qsc8iH6q9hIwo")

# ✅ Create the Gemini model (make sure the model name is valid)
model = genai.GenerativeModel("gemini-1.5-flash")  # Replace with latest valid model if needed

@app.route("/", methods=["GET", "POST"])
def chat():
    # ✅ Use session or hidden state if you want persistent messages
    messages = []

    if request.method == "POST":
        user_input = request.form["message"]
        messages.append(("You", user_input))

        try:
            # Start a new chat (if you want persistence, create chat object globally)
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_input)

            bot_reply = response.text.strip()
        except Exception as e:
            bot_reply = f"❌ HealthMate AI Error: {str(e)}"

        messages.append(("HealthMate AI", bot_reply))

    return render_template("chat.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)

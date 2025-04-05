from flask import Flask, render_template, request, redirect, flash, url_for
from scheduler import schedule_medication, reminders  # ✅ importing reminders

app = Flask(__name__)
app.secret_key = 'rsp_health_secret'

@app.route('/', methods=['GET', 'POST'])
def manage_meds():
    if request.method == 'POST':
        med_name = request.form.get('medName')
        med_time = request.form.get('medTime')
        email = request.form.get('email')

        if med_name and med_time and email:
            try:
                schedule_medication(med_name, med_time, email)
                flash(f"✅ Reminder for '{med_name}' scheduled at {med_time} to {email}", "success")
            except Exception as e:
                flash(f"❌ Error scheduling medication: {str(e)}", "error")
        else:
            flash("⚠️ Please fill in all fields!", "warning")

        return redirect(url_for('manage_meds'))

    return render_template('design.html', reminders=reminders)

if __name__ == '__main__':
    app.run(debug=True)

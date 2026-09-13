from flask import Flask, render_template

app = Flask(__name__)

# डमी जॉब्सची यादी (पुढे जाऊन आपण हे डेटाबेसवरून घेऊ शकतो)
jobs_list = [
    {
        "id": 1,
        "title": "ITI Railway Apprentice Recruitment 2026",
        "department": "Indian Railways",
        "qualification": "ITI Pass (Fitter / Electrician / Welder)",
        "last_date": "30 Sept 2026",
        "link": "#"
    },
    {
        "id": 2,
        "title": "Mahagenco Technician-3 Vacancy",
        "department": "Mahagenco (महानिर्मिती)",
        "qualification": "ITI Electrical / Wireman",
        "last_date": "15 Oct 2026",
        "link": "#"
    },
    {
        "id": 3,
        "title": "Konkan Railway S&T Maintenance Posts",
        "department": "Konkan Railway",
        "qualification": "ITI Electronics / Electrical",
        "last_date": "25 Sept 2026",
        "link": "#"
    }
]

@app.route('/')
def home():
    return render_template('index.html', jobs=jobs_list)

if __name__ == '__main__':
    app.run(debug=True)

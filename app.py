from flask import Flask, render_template

app = Flask(__name__)

# डमी जॉब लिस्ट (पुढे आपण हे डेटाबेसवरून घेऊ शकतो)
JOBS = [
    {
        "id": 1,
        "title": "ITI Railway Apprentice Recruitment 2026",
        "department": "Indian Railways (Konkan / Central Railway)",
        "qualification": "ITI Passed (Tractor Mechanic, Fitter, Electrician, Welder)",
        "last_date": "30 Sept 2026",
        "link": "#"
    },
    {
        "id": 2,
        "title": "Mahagenco Technician-3 Vacancy",
        "department": "Maharashtra State Power Generation Co. Ltd.",
        "qualification": "ITI Electrical / Mechanical",
        "last_date": "15 Oct 2026",
        "link": "#"
    },
    {
        "id": 3,
        "title": "John Deere & CNH Assembly Shop Trainee",
        "department": "Private / Multinational Sector",
        "qualification": "ITI Tractor Mechanic / Diesel Mechanic",
        "last_date": "Running",
        "link": "#"
    }
]

@app.route('/')
def home():
    return render_template('index.html', jobs=JOBS)

if __name__ == '__main__':
    app.run(debug=True)

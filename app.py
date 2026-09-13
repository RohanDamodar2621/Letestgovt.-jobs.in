import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'rohan_secret_key_secure'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class JobPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    organization = db.Column(db.String(200))
    advt_no = db.Column(db.String(100))
    total_vacancies = db.Column(db.String(50))
    advt_date = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    last_date = db.Column(db.String(100))
    notification_link = db.Column(db.String(500))
    apply_link = db.Column(db.String(500))
    category = db.Column(db.String(50), default="Notice")

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    jobs = JobPost.query.order_by(JobPost.id.desc()).all()
    return render_template('index.html', jobs=jobs)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('logged_in'):
        if request.method == 'POST':
            new_job = JobPost(
                title=request.form.get('title'),
                organization=request.form.get('organization'),
                advt_no=request.form.get('advt_no'),
                total_vacancies=request.form.get('total_vacancies'),
                advt_date=request.form.get('advt_date'),
                start_date=request.form.get('start_date'),
                last_date=request.form.get('last_date'),
                notification_link=request.form.get('notification_link'),
                apply_link=request.form.get('apply_link'),
                category=request.form.get('category')
            )
            db.session.add(new_job)
            db.session.commit()
            return redirect(url_for('admin'))
        
        jobs = JobPost.query.order_by(JobPost.id.desc()).all()
        return render_template('admin.html', jobs=jobs, logged_in=True)

    error = None
    if request.method == 'POST':
        if request.form.get('username') == 'Rohan2621' and request.form.get('password') == 'Tejas3108!!':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'चुकीचा युजरनेम किंवा पासवर्ड!'

    return render_template('admin.html', logged_in=False, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete_job(id):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    job = JobPost.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)

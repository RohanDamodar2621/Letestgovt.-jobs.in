import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'rohan_secret_key_secure' # सेशन सांभाळण्यासाठी सिक्रेट क्रीट

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default="Notice")

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    notices = Notice.query.order_by(Notice.id.desc()).all()
    return render_template('index.html', notices=notices)

# लॉगिन पेज (Admin Login)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # जर आधीच लॉगिन असेल तर डॅशबोर्ड दाखवा
    if session.get('logged_in'):
        if request.method == 'POST':
            title = request.form.get('title')
            category = request.form.get('category')
            if title:
                new_notice = Notice(title=title, category=category)
                db.session.add(new_notice)
                db.session.commit()
                return redirect(url_for('admin'))
        
        notices = Notice.query.order_by(Notice.id.desc()).all()
        return render_template('admin.html', notices=notices, logged_in=True)

    # लॉगिन नसलेस फॉर्म तपासा
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'Rohan2621' and password == 'Tejas3108!!':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'चुकीचा युजरनेम किंवा पासवर्ड!'

    return render_template('admin.html', logged_in=False, error=error)

# लॉगआउट करण्यासाठी
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete_notice(id):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)

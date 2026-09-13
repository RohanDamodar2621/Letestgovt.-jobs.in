import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Render किंवा लोकलसाठी SQLite डेटाबेस कॉन्फिगरेशन
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# डेटाबेस टेबल रचना (Notice Board वरील अपडेट्ससाठी)
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default="Notice") # Notice किंवा Recruitment

with app.app_context():
    db.create_all()

# मुख्य होमपेज (जिथे सर्व नोटीस आणि अपडेट्स दिसतील)
@app.route('/')
def home():
    notices = Notice.query.order_by(Notice.id.desc()).all()
    return render_template('index.html', notices=notices)

# ॲडमिन पॅनल (नवीन जॉब टाकण्यासाठी पेज)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        if title:
            new_notice = Notice(title=title, category=category)
            db.session.add(new_notice)
            db.session.commit()
            return redirect(url_for('admin'))
    
    notices = Notice.query.order_by(Notice.id.desc()).all()
    return render_template('admin.html', notices=notices)

# नोटीस डिलीट करण्यासाठी
@app.route('/delete/<int:id>')
def delete_notice(id):
    notice = Notice.query.get_or_404(id)
    db.session.delete(notice)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)

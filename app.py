import os
import time
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
DEFAULT_DB = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', DEFAULT_DB)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Active')

    def __repr__(self):
        return f"<Item {self.title}>"

# 1. READ: Display items
@app.route('/')
def home():
    items = Item.query.all()
    return render_template('dashboard.html', items=items)

# 2. CREATE: Add item
@app.route('/add', methods=['POST'])
def add_item():
    title = request.form.get('title')
    if title:
        new_item = Item(title=title)
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('home'))

# 3. DELETE: Remove item
@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))

# 4. UPDATE: Edit item route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.title = request.form.get('title')
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', item=item)

if __name__ == '__main__':
    with app.app_context():
        time.sleep(2)
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
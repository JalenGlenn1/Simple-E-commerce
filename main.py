from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import util
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# create an application instance
# all requests it receives from clients to this object for handling
# we are instantiating a Flask object by passing __name__ argument to the Flask constructor. 
# The Flask constructor has one required argument which is the name of the application package. 
# Most of the time __name__ is the correct value. The name of the application package is used 
# by Flask to find static assets, templates and so on.
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ecommerce.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class accounts(db.Model):
    __tablename__ = "accounts"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    gift_card_funds = db.Column(db.Float, default = 0.0)
    quantity_a = db.Column(db.Integer, default = 0)
    quantity_b = db.Column(db.Integer, default = 0)
    quantity_c = db.Column(db.Integer, default = 0)
    quantity_d = db.Column(db.Integer, default = 0)
    quantity_e = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return ("Username: " + self.username + "\nPassword: " + self.password + "\nGift card funds: " + str(self.gift_card_funds) + 
            "\nQuantity A: " + str(self.quantity_a) + "\nQuantity B: " + str(self.quantity_b) + "\nQuantity C: " + str(self.quantity_c) +
            "\nQuantity D: " + str(self.quantity_d) + "\nQuantity E: " + str(self.quantity_e) + "\n")

db.drop_all()
db.create_all()
guest_user = accounts(username='Guest', password='Guest')
test_user_a = accounts(username='john', password='junk', gift_card_funds=2.95, quantity_a=1, quantity_b=2, quantity_c=3, quantity_d=4, quantity_e=5)
test_user_b = accounts(username='barnaby234', password='wahse', gift_card_funds=10.96, quantity_b=3, quantity_d=7)

db.session.add_all([guest_user, test_user_a, test_user_b])
db.session.commit()

active_user = 'Guest'

# route is used to map a URL with a Python function
# complete address: ip:port/
# 127.0.0.1:5000/
@app.route('/', methods=['GET', 'POST'])
def login_page():
    return render_template('Login.html')

@app.route('/Available_Items', methods=['GET', 'POST'])
def items_page():
    global active_user

    if request.method == 'GET':
       active_user = 'Guest'

    active = active_user
    user = accounts.query.filter(accounts.username==active).first()

    items_a = user.quantity_a
    items_b = user.quantity_b
    items_c = user.quantity_c
    items_d = user.quantity_d
    items_e = user.quantity_e
    money = round(user.gift_card_funds, 2)

    return render_template('Available_Items.html', log_html = user.username, items_a_html = str(items_a), items_b_html = str(items_b), items_c_html = str(items_c), items_d_html = str(items_d), items_e_html = str(items_e), money_html = str(money))

@app.route('/Account_Creation', methods=['GET', 'POST'])
def account_page():
    return render_template('Account_Creation.html')

@app.route('/verify_new_username', methods=['POST'])
def receive_data():
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    found_username = accounts.query.filter(accounts.username==new_username).first()

    if new_username == '' or new_password == '':
        return "Blank, not added"
    elif found_username is None:
        db.session.add(accounts(username=new_username, password=new_password))
        db.session.commit()
        return "Not found, added"
    else:
        return "Found, not added"

@app.route('/verify_login', methods=['POST'])
def receive_data2():
    global active_user

    enter_username = request.form['enter_username']
    enter_password = request.form['enter_password']
    found_username = accounts.query.filter(accounts.username==enter_username, accounts.password==enter_password).first()

    if found_username is None:
        return "Login failed"
    else:
        active_user = enter_username
        return "Login succeeded"

@app.route('/increment_quantity_a', methods=['GET'])
def increment_quantity_a():
    global active_user
    user = accounts.query.filter(accounts.username==active_user).first()
    user.quantity_a = user.quantity_a + 1
    db.session.commit()
    return "Increment success" + str(user.quantity_a)

@app.route('/increment_quantity_b', methods=['GET'])
def increment_quantity_b():
    global active_user
    user = accounts.query.filter(accounts.username==active_user).first()
    user.quantity_b = user.quantity_b + 1
    db.session.commit()
    return "Increment success" + str(user.quantity_b)

@app.route('/increment_quantity_c', methods=['GET'])
def increment_quantity_c():
    global active_user
    user = accounts.query.filter(accounts.username==active_user).first()
    user.quantity_c = user.quantity_c + 1
    db.session.commit()
    return "Increment success" + str(user.quantity_c)

@app.route('/increment_quantity_d', methods=['GET'])
def increment_quantity_d():
    global active_user
    user = accounts.query.filter(accounts.username==active_user).first()
    user.quantity_d = user.quantity_d + 1
    db.session.commit()
    return "Increment success" + str(user.quantity_d)

@app.route('/increment_quantity_e', methods=['GET'])
def increment_quantity_e():
    global active_user
    user = accounts.query.filter(accounts.username==active_user).first()
    user.quantity_e = user.quantity_e + 1
    db.session.commit()
    return "Increment success" + str(user.quantity_e)

@app.route('/update_quantities', methods=['POST'])
def update_quantities():
    global active_user

    user = accounts.query.filter(accounts.username==active_user).first()
    user.quantity_a = request.form['new_quantity_a']
    user.quantity_b = request.form['new_quantity_b']
    user.quantity_c = request.form['new_quantity_c']
    user.quantity_d = request.form['new_quantity_d']
    user.quantity_e = request.form['new_quantity_e']
    db.session.commit()
    return "Increment success"

@app.route('/update_funds', methods=['POST'])
def update_funds():
    global active_user

    user = accounts.query.filter(accounts.username==active_user).first()
    user.gift_card_funds = round(user.gift_card_funds + float(request.form['new_funds']), 2)
    db.session.commit()
    return "Increment success"

@app.route('/gift_payment', methods=['GET'])
def gift_payment():
    global active_user

    user = accounts.query.filter(accounts.username==active_user).first()
    cost = round(user.quantity_a * 14.99 + user.quantity_b * 15.99 + user.quantity_c * 3.99 + user.quantity_d * 2899.99 + user.quantity_e * 499.99, 2)

    if cost > user.gift_card_funds:
        return "Payment failed"
    else:
        user.gift_card_funds = user.gift_card_funds - cost
        user.quantity_a = 0
        user.quantity_b = 0
        user.quantity_c = 0
        user.quantity_d = 0
        user.quantity_e = 0
        db.session.commit()
        return "Payment succeeded"

@app.route('/debit_credit_payment', methods=['GET'])
def debit_credit_payment():
    global active_user

    user = accounts.query.filter(accounts.username==active_user).first()

    user.quantity_a = 0
    user.quantity_b = 0
    user.quantity_c = 0
    user.quantity_d = 0
    user.quantity_e = 0
    db.session.commit()
    return "Payment succeeded"

@app.route('/logout', methods=['GET'])
def logout():
    global active_user
    active_user = "Guest"
    return "Logout successful"

@app.route('/Checkout', methods=['GET'])
def checkout_page():
    global active_user
    user = accounts.query.filter(accounts.username==active_user).first()

    cost = round(user.quantity_a * 14.99 + user.quantity_b * 15.99 + user.quantity_c * 3.99 + user.quantity_d * 2899.99 + user.quantity_e * 499.99, 2)
    return render_template('Checkout.html', money_html = str(cost))

@app.route('/Edit_Cart', methods=['GET'])
def cart_page():
    return render_template('Edit_Cart.html')

@app.route('/Add_Funds', methods=['GET'])
def funds_page():
    return render_template('Add_Funds.html')

if __name__ == '__main__':
	# set debug mode
    app.debug = True
    # your local machine ip
    ip = '127.0.0.1'
    db.create_all()
    app.run(host=ip)


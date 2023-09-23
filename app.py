from flask import Flask,render_template, request, url_for, redirect, session,jsonify
import mysql.connector

#Database connection 
mydb = mysql.connector.connect(host="localhost", user="root",password="",database="inventorymanagementsystem")
mycursor = mydb.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NTP'

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/home",methods=['GET','POST'])
def home():
    return render_template('home.html',username=session['username'][0])

@app.route("/dashboard",methods=['POST'])
def dashboard():
    
    return render_template('dashboard.html')

@app.route("/register",methods=['POST'])
def register():
    return render_template('register.html')

@app.route("/login",methods=['POST'])
def login():
    return render_template('login.html')

@app.route("/about",methods=['POST'])
def about():
    return render_template('about.html')

@app.route('/validate_login', methods =['GET', 'POST'])
def validate_login():
    msg=''
    if request.method == 'POST':

        username = request.form['email']
        password = request.form['pwd']

        mycursor.execute('SELECT * FROM Users WHERE email = %s AND password = %s', (username, password, ))
        account = mycursor.fetchall()

        if account:
            session['loggedin'] = True
            session['username'] = account[0]
            msg='success'
        else:
            msg='error'
        return render_template('index.html', msg = msg)
    
@app.route("/validate_register",methods=['GET','POSt'])
def validate_register():
    msg = ''
    if request.method == 'POST':
        
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['pwd'] 
        phone = request.form['phone']
        cname = request.form['cname']
        address = request.form['address']

        mycursor.execute('SELECT * FROM users WHERE email = %s  AND cname= %s', (email, cname))
        account = mycursor.fetchall()

        if account:
            msg = 'exists'
        else:
            mycursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s)', (fname, lname, email, password, phone, cname, address))
            mydb.commit()
            msg = 'Registered successfully'
    else:
        msg="Error while Registering"
    
    return render_template('index.html',msg=msg)

@app.route("/profile",methods=['POST'])
def profile():
    if request.method == 'POST':
        print(session['username'])
        data={
            'fname' : session['username'][0],
            'lname' : session['username'][1],
            'email' : session['username'][2],
            'phone' : session['username'][4],
            'cname' : session['username'][5],
            'address':session['username'][6]
        }
    return render_template('profile.html',data=data)

@app.route('/users',methods=['GET','POST'])
def users():
    if request.method == 'POST':
        
        mycursor.execute('SELECT * FROM users')
        users = mycursor.fetchall()

    return render_template('users.html',users=users)

@app.route('/items',methods=['GET','POST'])
def items():  
    if request.method == 'POST':
        
        mycursor.execute('SELECT * FROM items')
        items = mycursor.fetchall()
        
    return render_template('items.html',items=items)

@app.route('/add_item',methods=['GET','POST'])
def add_item():
    return render_template('add_items.html')

@app.route('/add_user',methods=['GET','POST'])
def add_user():
    return render_template('add_user.html')

@app.route('/display_item',methods=['POST'])
def display_item():
    if request.method == 'POST':

        mycursor.execute('SELECT * FROM items where product_id=%s',request.values)
        values = mycursor.fetchall()
        data={
            'pid' : values['product_id'],
            'pname' : values['product_name'],
            'category' : values['category'],
            'mdate' : values['manf_date'],
            'edate' : values['exp_date'],
            'price':values['price'],
            'quantity':values['quantity'],
            'desc':values['description']
        }
        return render_template('/display_item.html',data=data)

@app.route('/validate_item',methods=['POST'])
def validate_item():
    if request.method == 'POST':

        pid = request.form['pid']
        pname = request.form['pname']
        category = request.form['category']
        mdate = request.form['mdate']
        edate = request.form['edate']
        price = request.form['price']
        quantity = request.form['qty']
        desc = request.form['desc']

        mycursor.execute('INSERT into items VALUES(%s, %s, %s, %s, %s, %s, %s, %s)',(pid,pname,category,mdate,edate,price,quantity,desc))
       
    return redirect('/items')

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__=="_main_":
    app.run(debug=True)
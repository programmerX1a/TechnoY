from flask import render_template,redirect,Flask,request,session,flash,url_for,render_template_string
from zxcvbn import zxcvbn
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from datetime import datetime,timedelta
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user


app=Flask(__name__)
app.permanent_session_lifetime = timedelta(days=30)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

with sqlite3.connect("database.db") as x:
    db=x.cursor()
    db.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,   
    cash REAL NOT NULL

    
    )
'''
)
    db.execute('''
    CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL
    
)'''
)  
    db.execute('''
    CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
    UNIQUE(user_id, course_id)
)'''
)
 

def connect():    #Turns tuple rows into dictionaries and auto saves
    y=sqlite3.connect("database.db",isolation_level=None)
    y.row_factory=sqlite3.Row
    return y


@app.route("/alert")
def alert(): 
    return render_template_string("""
        <script>
            alert("You're already enrolled in this course.");
            window.location.href = "{{ url_for('index') }}";
        </script>
        """)

    return redirect(url_for('index'))




@app.route("/")
def index():
    logged=session.get("Logged")
    name=session.get("name")
    return render_template("index.html",logged=logged,name=name)

@app.route("/logout")
def logout():
    session["Logged"]=False
    return redirect("/signin")


@app.route("/sw",methods=["POST","GET"])
def sw():
    if request.method=="POST":
        session["course_name"]="Solid Works"
        with connect() as x:
            db=x.cursor()
            row=db.execute("SELECT * FROM courses WHERE name=?",(session.get("course_name"),)).fetchone()
            session["course_price"]=row["price"]
            row2=db.execute("SELECT * FROM enrollments WHERE user_id=? and course_id=(SELECT id FROM courses WHERE name=?)",(session.get("user_id"),session.get("course_name"),)).fetchone()
            if row2 is not None:
                return redirect("/alert")
            else:
                return redirect("/payment")    

    else:
        logged=session.get("Logged")
        name=session.get("name")
        return render_template("SW.html",logged=logged,name=name)
 
@app.route("/ai",methods=["POST","GET"])
def ai():
    if request.method=="POST":
        session["course_name"]="Artificial Intelligence"
        with connect() as x:
            db=x.cursor()
            row=db.execute("SELECT * FROM courses WHERE name=?",(session.get("course_name"),)).fetchone()
            session["course_price"]=row["price"]
            row2=db.execute("SELECT * FROM enrollments WHERE user_id=? and course_id=(SELECT id FROM courses WHERE name=?)",(session.get("user_id"),session.get("course_name"),)).fetchone()
            if row2 is not None:
                return redirect("/alert")
            else:
                return redirect("/payment")    

    else:
        logged=session.get("Logged")
        name=session.get("name")
        return render_template("ai.html",logged=logged,name=name)

@app.route("/signin",methods=["POST","GET"])
def signin():
    session.clear()
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")


        with connect() as x:
            db=x.cursor()
            row=db.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone()
            if row is None:
                return render_template("Sign IN.html",error="User doesnt exist")
            elif not check_password_hash(row["password"],password):
                   return render_template("Sign IN.html",error="Incorrect Password")
        session["user_id"] = row["id"]
        session["email"]=email
        session.permanent=bool(request.form.get("remember"))  
        session["Logged"]=True 
        session["name"]=session["email"].split("@")[0]
       




        return redirect("/")       
                    




    
    return render_template("Sign IN.html")
 
@app.route("/cpp",methods=["POST","GET"])
def cpp():
    if request.method=="POST":
        session["course_name"]="C++"
        with connect() as x:
            db=x.cursor()
            row=db.execute("SELECT * FROM courses WHERE name=?",(session.get("course_name"),)).fetchone()
            session["course_price"]=row["price"]
            row2=db.execute("SELECT * FROM enrollments WHERE user_id=? and course_id=(SELECT id FROM courses WHERE name=?)",(session.get("user_id"),session.get("course_name"),)).fetchone()
            if row2 is not None:
                return redirect("/alert")
            else:
                return redirect("/payment")    

    else:
        logged=session.get("Logged")
        name=session.get("name")
        return render_template("C++.html",logged=logged,name=name)


@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        email=request.form.get("Email")
        password=request.form.get("Password")
        cpassword=request.form.get("CPassword")
        strength=zxcvbn(password)
        if not email:
            return render_template("Sign UP.html",error="Please Enter a valid Email")
        elif password!=cpassword:
            return render_template("Sign UP.html",error="Both passwords must be identical")    
        elif len(password)<8:
             return render_template("Sign UP.html",error="Password needs to have atleast 8 Characters")    
        elif strength["score"]<2:
             return render_template("Sign UP.html",error="Make sure your Password includes Lowercase/Uppercase Characters with numbers")
        with connect() as x:
            db=x.cursor()
            row=db.execute("SELECT * FROM users WHERE email=?",(email,)).fetchone()  
            if row is not None:
                return render_template("Sign UP.html",error="User Already exists")    
            hashed_password=generate_password_hash(password)
            db.execute("INSERT INTO users(email,password,cash) VALUES(?,?,100)",(email,hashed_password))
            return redirect("/signin")            
           

                






    else:    
        return render_template("Sign UP.html")
 
@app.route("/python",methods=["POST","GET"])
def python():
    if request.method=="POST":
        session["course_name"]="Python"
        with connect() as x:
            db=x.cursor()
            row=db.execute("SELECT * FROM courses WHERE name=?",(session.get("course_name"),)).fetchone()
            session["course_price"]=row["price"]
            row2=db.execute("SELECT * FROM enrollments WHERE user_id=? and course_id=(SELECT id FROM courses WHERE name=?)",(session.get("user_id"),session.get("course_name"),)).fetchone()
            if row2 is not None:
                return redirect("/alert")
            else:
                return redirect("/payment")    

    else:
        logged=session.get("Logged")
        name=session.get("name")
        return render_template("python.html",logged=logged,name=name)

@app.route("/web",methods=["POST","GET"])
def web():
    if request.method=="POST":
        session["course_name"]="Web Development"
        with connect() as x:
            db=x.cursor()
            row=db.execute("SELECT * FROM courses WHERE name=?",(session.get("course_name"),)).fetchone()
            session["course_price"]=row["price"]
            row2=db.execute("SELECT * FROM enrollments WHERE user_id=? and course_id=(SELECT id FROM courses WHERE name=?)",(session.get("user_id"),session.get("course_name"),)).fetchone()
            if row2 is not None:
                return redirect("/alert")
            else:
                return redirect("/payment")    

    else:
        logged=session.get("Logged")
        name=session.get("name")
        return render_template("wb.html",logged=logged,name=name)

@app.route("/payment",methods=["POST","GET"])
def payment():
    print(request.method)
    if request.method=="POST":
        course=session.get("course_name")
        price=session.get("course_price")
        name=str(request.form.get("pname"))
        expiry=request.form.get("expiry")
        card=request.form.get("card")
        

        if any(i.isdigit() for i in name):
            return render_template("payment.html",error="Enter a Valid Name",course=course,price=price)


        try:
            cvc=int(request.form.get("cvc"))
        except ValueError:
            return render_template("payment.html",error="Enter a Valid CVC (3 digits)",course=course,price=price)    


        year=int(expiry.split('/')[1])
        month=int(expiry.split('/')[0])
        current_year=int(datetime.now().year)-2000
        current_month=int(datetime.now().month)
        card=card.replace(" ","")
        valid=[34,37,40,51,52,53,54,55,22,23,24,25,26,27,40,41,42,43,44,45,46,47,48,49]
        sum1=0
        sum2=0
        digits2=int(card[0:2]) 

        if digits2 not in valid:
            return render_template("payment.html",error="Invalid Credit Card (ONLY AMEX, VISA AND MASTERCARD)",course=course,price=price)


        digits=[int(i) for i in card]
        for i in range(len(digits) - 1, -1, -2):
            sum1 += digits[i]
        for i in range(len(digits) - 2, -1, -2):
            doubled = digits[i] * 2
            if doubled >= 10:
                sum2 += (doubled % 10) + (doubled // 10)
            else:
                sum2 += doubled

        total = sum1 + sum2
        if total % 10 != 0:
            return render_template("payment.html",error="Invalid Credit Card",course=course,price=price)  


        if year<current_year:
            return render_template("payment.html",error="Expired Credit Card",course=course,price=price)
        elif year==current_year and month<=current_month:
            return render_template("payment.html",error="Expired Credit Card",course=course,price=price)
        with connect() as x:
            db=x.cursor()
            cash=db.execute("SELECT cash FROM users WHERE id=?",(session.get("user_id"),)).fetchone()[0]
            if cash<price:
                return render_template("payment.html",error="Credit Card Declined",course=course,price=price)
            print(cash)
                
        return redirect("/success")    


            






    else:
        course=session.get("course_name")
        price=session.get("course_price")
        return render_template("payment.html",course=course,price=price)
@app.route("/success")
def success():
    course=session.get("course_name")
    date=datetime.now()
    with connect() as x:
        db=x.cursor()
        price=db.execute("SELECT price FROM courses WHERE name=?",(course,)).fetchone()
        db.execute("INSERT INTO enrollments (user_id,course_id,enrollment_date)   VALUES (?,(SELECT id FROM courses WHERE name=?),?)",(session.get("user_id"),course,date))
        db.execute("UPDATE users SET cash=cash-? WHERE id=?",(price[0],session.get("user_id")))





    return render_template("join.html",course=course)


@app.route("/history",methods=["POST","GET"])
def history():
    if request.method=="POST":
        name=request.form.get("courses")
        with connect() as x:
            db=x.cursor()
            price=db.execute("SELECT price FROM courses WHERE name=?",(name,)).fetchone()
            id=db.execute("SELECT id FROM courses WHERE name=?",(name,)).fetchone()

            print(name,price,id)
            if price and id:
                db.execute("UPDATE users SET cash=cash+? WHERE id=?",(price[0],session.get("user_id")))
                db.execute("DELETE FROM enrollments WHERE user_id=? AND course_id=?",(session.get("user_id"),id[0]))
        return redirect("/history")        


    else:
        logged=session.get("Logged")
        name=session.get("name")
        with connect() as x:
            db=x.cursor()
            rows = db.execute("""
            SELECT users.email AS user_email, courses.name AS course_name, courses.price AS course_price,enrollment_date,users.cash as cash
            FROM enrollments
            JOIN users ON enrollments.user_id = users.id
            JOIN courses ON enrollments.course_id = courses.id
            WHERE user_id=?
        """,(session.get("user_id"),)).fetchall()
            cash=db.execute("SELECT cash FROM users WHERE id=?",(session.get("user_id"),)).fetchone()   
            if not rows:
                disabled=True
            else:
                disabled=False    
     
        return render_template("history.html",name=name,logged=logged,rows=rows,cash=cash,disabled=disabled)    
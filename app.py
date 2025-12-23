from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
app=Flask(__name__)
app.secret_key="gizli_anahtar"
# SQLite ile bağlantı kurma 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# DB oluşturma
db = SQLAlchemy(app )
class Account(db.Model):
    name=db.Column(db.String(20),nullable=False,unique=True)
    password=db.Column(db.String(100),nullable=False)
    id=db.Column(db.Integer,primary_key=True)
    def __repr__(self):
        return f"<Account {self.id}"
@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name=request.form["name"]
        password=request.form["password"]
        user=Account.query.filter_by(name=name).first()
        if user and check_password_hash(user.password,password):
            session["user_id"]=user.id
            return redirect("/home")
        else:
            return "Hatalı giriş❌"
    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        try:
            name=request.form["name"]
            password=request.form["password"]

            hashed_pw=generate_password_hash(password)
            new_user=Account(name=name,password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
        except:
            return "Bu kullanıcı adı zaten var"
        return redirect("/")
    return render_template("register.html")
@app.route("/welcome",methods=["POST"])
def welcome():
    name=request.form["name"]
    password=request.form["password"]
    return render_template("welcome.html",name=name,password=password)
@app.route("/home")
def home_shop():
    if "user_id" not in session:
        return redirect("/")
    return render_template("home.html")
@app.route("/sepete_ekle",methods=["POST"])
def sepete_ekle():
    if "user_id" not in session:
        return redirect("/")
    urun={
        "ad": request.form["ad"],
        "fiyat": request.form["fiyat"],
        "resim":request.form["resim"]
    }
    if "sepet" not in session:
        session["sepet"]=[]
    sepet=session["sepet"]
    sepet.append(urun)
    session["sepet"]=sepet
    return redirect("/home")
@app.route("/sepet")
def sepet():
    if "user_id" not in session:
        return redirect("/")
    return render_template("sepet.html",sepet=session.get("sepet"))
@app.route("/buy")
def buy():
    if "user_id" not in session:
        return redirect("/")
    return render_template("buy.html")
@app.route("/buy_success",methods=["POST"])
def buy_success():
    if "user_id" not in session:
        return redirect("/")
    return render_template("buy_success.html")
@app.route("/sepet_sil", methods=["POST"])
def sepet_sil():
    if "user_id" not in session:
        return redirect("/")
    index = int(request.form["index"])

    sepet = session.get("sepet", [])

    if 0 <= index < len(sepet):
        sepet.pop(index)
        session["sepet"] = sepet

    return redirect("/sepet")
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
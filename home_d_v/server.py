from flask import Flask,render_template, request ,redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField
from flask_wtf.file import FileField , FileAllowed
import datetime


app=Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

configure_uploads(app, photos)

db = SQLAlchemy(app)


#  ************les tables ************


class Repas(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    categorie=db.Column(db.String(100))
    price = db.Column(db.Integer) 
    store = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))

class AddRepas(FlaskForm):
    title= StringField('title')
    categorie = StringField('categorie')   
    price = IntegerField('price')
    store = IntegerField('store')
    description = TextAreaField('description')
    image = FileField('image', validators=[FileAllowed(IMAGES, ' Seules les images sont acceptées. ')])

class Message(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100),nullable=False) 
    phone = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(200),nullable=False)
    message= db.Column(db.String(30),nullable=False)

class AddMessage(FlaskForm):
    name = StringField('name')
    email = StringField('email')
    phone = IntegerField('phone')
    address = TextAreaField('address')
    message = TextAreaField('message')


# ************Clients************
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return  render_template("about.html")

@app.route("/contact", methods=['GET','POST'])
def contact(): 
    form = AddMessage()
    if form.validate_on_submit():        
        new_message=Message(name=form.name.data,email=form.email.data,phone=form.phone.data,address=form.address.data,message=form.message.data)
        db.session.add(new_message)
        db.session.commit()
        print(new_message)
        return redirect(url_for('home'))

    return render_template("contact.html",form=form)

@app.route("/onemeal/<id>")
def onemeal(id):
    repas =Repas.query.filter_by(id=id).first()
    return render_template("onemeal.html",repas=repas)

@app.route("/meals")
def meals():
    repas=Repas.query.all()
    return render_template("meals.html", repas=repas)

@app.route("/login_client")
def login_client():
    return render_template("login_client.html")

# ************Admin************
@app.route("/admin")
def admin():
    repas=Repas.query.all()
    m=repas.reverse()
    return render_template("admin/admin.html",repas=repas)

@app.route("/admin/inbox")
def inbox():
    messages=Message.query.all()
    m=messages.reverse()
    return render_template('admin/inbox.html', admin=True,messages=messages)


@app.route("/admin/add",methods=['POST','GET'])
def add():
    form = AddRepas()
    if form.validate_on_submit(): 
        image_url=photos.url(photos.save(form.image.data))
        a=Repas(title=form.title.data,categorie=form.categorie.data,price=form.price.data,store=form.store.data,image=image_url)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('admin/add_meals.html', admin=True,form=form)

@app.route("/admin/delete/<int:id>",methods=['POST','GET'])
def delete(id):
    deleteMeals = Repas.query.filter_by(id = id).first()
    db.session.delete(deleteMeals)
    db.session.commit()
    return redirect(url_for('admin'))



@app.route("/login_admin")
def login_admin():
    return render_template("login_admin.html")


if __name__ == '__main__':
    app.run()




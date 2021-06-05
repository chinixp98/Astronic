from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import os
from session import login_required

UPLOAD_FOLDER = "./static/profile/"
UPLOAD_POST = "./static/post/"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_POST'] = UPLOAD_POST

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///astronic.db")


@app.route("/")
def index():

    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("login.html", error="Debe introducir su usuario")

        if not password:
            return render_template("login.html", error="Debe introducir su contraseña")

        if not username and password:
            return render_template("login.html", error="Debe introducir lo requerido")

        rows = db.execute("SELECT *FROM users WHERE username = :username", username=username)

        if len(rows) != 1:
            return render_template("login.html", error="Usuario no registrado")

        if not check_password_hash(rows[0]["password"], password):
            return render_template("login.html", error="Contraseña incorrecta")

        else:
            session["user_id"] = rows[0]["user_id"]

        return redirect("/home")

    else:
        return render_template("login.html")




@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":

        first_name = request.form.get("name")
        last_name = request.form.get("lastname")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not first_name:
            return render_template("register.html", error="Introduzca su primer nombre")

        if not last_name:
            return render_template("register.html", error="Introduzca su primer apellido")

        if not email:
            return render_template("register.html", error="Introduzca su correo electrónico")

        if not username:
            return render_template("register.html", error="Introduzca un usuario")

        if not password:
            return render_template("register.html", error="Introduzca una contraseña")

        if not confirmation:
            return render_template("register.html", error="Introduzca su contraseña de nuevo")

        if password != confirmation:
            return render_template("register.html", error="Las contraseñas deben ser iguales")

        correo = db.execute("SELECT *FROM users WHERE email = :email", email=email)

        if len(correo) == 1:
            return render_template("register.html", error="Este correo ya está en uso")

        rows = db.execute("SELECT *FROM users WHERE username = :username", username=username)

        if len(rows) == 1:
            return render_template("register.html", error="Usuario en uso")

        elif len(rows) == 0:
            nuevo_usuario = db.execute("INSERT INTO users (first_name, last_name, email, username, password) VALUES (:first_name, \
                                       :last_name, :email, :username, :password)", first_name=first_name, last_name=last_name,
                                       email=email, username=username, password=generate_password_hash(password))


        session["user_id"] = nuevo_usuario

        return redirect("/profile2")

    else:
        return render_template("register.html")



@app.route("/home", methods=["GET"])
@login_required
def home():

    return render_template("home.html")




@app.route("/profile1", methods=["GET", "POST"])
@login_required
def profile1():
    if request.method == "POST":

        archivo = request.files['archivo']
        about = request.form.get("about")

        if archivo:
            nombreArchivo = archivo.filename
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo))

            perfil = db.execute("SELECT profile_id FROM profile WHERE user_id = :user_id", user_id=session["user_id"])

            if perfil:
                db.execute("UPDATE profile SET foto = :foto WHERE user_id = :user_id", foto=nombreArchivo, user_id=session["user_id"])

            else:
                db.execute("INSERT INTO profile (foto, user_id) VALUES (:foto, :user_id)", foto=nombreArchivo, user_id=session["user_id"])

            return redirect ("/profile")

        if about:
            perfil = db.execute("SELECT profile_id FROM profile WHERE user_id = :user_id", user_id=session["user_id"])

            if perfil:
                db.execute("UPDATE profile SET about = :about WHERE user_id = :user_id", about=about, user_id=session["user_id"])

            else:
                db.execute("INSERT INTO profile (about, user_id) VALUES (:about, :user_id)", about=about, user_id=session["user_id"])

            return redirect ("/profile")



    else:
        return render_template("profile1.html")



@app.route("/profile2", methods=["GET", "POST"])
@login_required
def profile2():
    if request.method == "POST":

        archivo = request.files['archivo']

        if "archivo" not in request.files:
            return render_template("profile2.html", error="Debe introducir una imagen")

        if archivo.filename == "":
            return render_template("profile2.html", error="Debe introducir una imagen")

        if archivo:
            nombreArchivo = archivo.filename
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivo))

            perfil = db.execute("SELECT profile_id FROM profile WHERE user_id = :user_id", user_id=session["user_id"])

            if perfil:
                db.execute("UPDATE profile SET foto = :foto WHERE user_id = :user_id", foto=nombreArchivo, user_id=session["user_id"])

            else:
                db.execute("INSERT INTO profile (foto, user_id) VALUES (:foto, :user_id)", foto=nombreArchivo, user_id=session["user_id"])

            return redirect ("/profile")

    else:
        return render_template("profile2.html")




@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    nombreusuario = db.execute("SELECT username FROM users WHERE user_id = :user_id", user_id=session["user_id"])
    fotoperfil = db.execute("SELECT foto FROM profile WHERE user_id = :user_id", user_id=session["user_id"])
    about = db.execute("SELECT about FROM profile WHERE user_id = :user_id", user_id=session["user_id"])
    print(fotoperfil)

    return render_template("profile.html", fotoperfil = fotoperfil, nombreusuario=nombreusuario, about=about)




@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":
        title = request.form.get("titulo")
        imageurl = request.files['archivo']
        content = request.form.get("contenido")

        if not title:
            return render_template("create.html", error="Debe introducir un titulo")

        if not content:
            return render_template("create.html", error="Debe introducir contenido")

        if "archivo" not in request.files:
            return render_template("create.html", error="Debe introducir una imagen")

        if imageurl.filename == "":
            return render_template("create.html", error="Debe introducir una imagen")

        if imageurl:
            nombreArchivo = imageurl.filename
            imageurl.save(os.path.join(app.config["UPLOAD_POST"], nombreArchivo))
            db.execute("INSERT INTO posts (title, imageurl, content, user_id) VALUES (:title, :imageurl, :content, :user_id)",
                       title=title, imageurl=nombreArchivo, content=content, user_id=session["user_id"])

        return redirect ("/blog")

    else:
        return render_template("create.html")




@app.route("/comentario", methods=["GET", "POST"])
@login_required
def comentario():

    if request.method == "POST":
        comentario = request.form.get("comentario")
        post_id = request.form.get("pi")

        if not comentario:
            return render_template("comentario.html", error="Debe agregar un comentario")

        if comentario:
            db.execute("INSERT INTO comentarios (post_id, user_id, comment) VALUES (:post_id, :user_id, :comment)",
                       post_id=post_id, user_id=session["user_id"], comment=comentario)

        return redirect("/blog")

    else:
        post_id = request.args.get("pi")
        pi = int(post_id)
        print(pi)
        return render_template("comentario.html", pi=pi)



@app.route("/blog", methods=["GET"])
@login_required
def blog():

    posts = db.execute("SELECT title, imageurl, content, user_id, post_id FROM posts")
    usuario = db.execute("SELECT username, user_id FROM users")
    comentarios = db.execute("SELECT comment_id, post_id, user_id, comment FROM comentarios")

    print(usuario)
    print(posts)
    print(comentarios)
    return render_template("blog.html", posts=posts, usuario=usuario, comentarios=comentarios)






@app.route("/logout")
@login_required
def logout():

    session.clear()

    return redirect("/login")



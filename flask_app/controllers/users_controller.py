from flask import render_template, request, redirect, session, flash #importamos flash para mensajes

from flask_app import app 

from flask_app.models.users import User 
from flask_app.models.recipes import Recipe

#importacion de BCrypt para encriptar contraseña

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    #validamos la información que redcibimos
    if not User.valida_usuario(request.form):
        return redirect('/')

    #si todo se valida correctamente 

    #usuario entrega un request.form con los datos del formulario

    #rescatamos contraseña del usario y la guardamos en pwd para encriptarla

    pwd = bcrypt.generate_password_hash(request.form['password']) 

    #dado que request.form no se puede modificar, para reemplazar password se crea un nuevo diccioario con los datos del formulario request.form

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    #recibimos el id del nuevo usuario 

    id = User.save(formulario)

    #usamos session para guardarlo en sesión el id del usuario 

    session['user_id'] = id

    #redireccionamos a dashboard

    return redirect('/dashboard')




@app.route('/login' , methods=['POST'])
def login():
    #Verificamos que el email existe en la base de datos usando función de User para get mail
    user = User.get_by_email(request.form) #recibimos FALSO si no existe o una instancia de usuario si existe el mail

    if not user: #si USER es igual a False
        flash('Correo electrónico no encontrado', 'login')
        return redirect('/')

    #user es una instancia con todos los datos de mi usuario
    if not bcrypt.check_password_hash(user.password, request.form['password']):  #funcion para saber si la contraseña encriptada coincide con la ingresada
        flash('Password incorrecto', 'login')
        return redirect('/')

    #usamos session para guardarlo en sesión el id del usuario cuando esté validado

    session['user_id'] = user.id

    return redirect('/dashboard')





@app.route('/dashboard')
def dashboard():
    # VALIDAR QUE SE HAYA INICIADO SESIÓN
    if 'user_id' not in session:
        return redirect('/')

        ##en session tengo el id del usuario session['user_id]
        #queremos una función que con ese id devuelva una instancia de usuario para enviarla al html

    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario)

    #lista con todas las recetas

    todas_recetas = Recipe.get_all()


    return render_template('dashboard.html', user=user, todas_recetas = todas_recetas)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

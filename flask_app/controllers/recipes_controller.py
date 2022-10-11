from flask import render_template, request, redirect, session, flash #importamos flash para mensajes

from flask_app import app 

from flask_app.models.recipes import Recipe 
from flask_app.models.users import User

#importacion de BCrypt para encriptar contraseña

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')        
        ##en session tengo el id del usuario session['user_id]
        #queremos una función que con ese id devuelva una instancia de usuario para enviarla al html
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario)
    return render_template('new_recipe.html', user=user)

@app.route('/create/recipe', methods = ['POST'])
def create_recipe():
    if 'user_id' not in session: #comprobamos que haya iniciado sesión
        return redirect('/')     

    #validación de receta con la función valida
    
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe') 

    #si se valida se guarda la receta con la función save

    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')        
        ##en session tengo el id del usuario session['user_id]
        #queremos una función que con ese id devuelva una instancia de usuario para enviarla al html
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario) #recibo la instsnacia de usuario que inició sesión

    #La instancia de la receta que se debe desplegar en editar, en base al ID de la receta
    #creamos un diccionrio para pasar funciuon get_by_id
    formulario_receta = {"id": id}

    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods = ['POST'])
def update_recipe():
    #verificar que haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')   

    #verificar que los datos estén correctos 

    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id']) #edit/recipe/1 

    #guardar los cambios

    Recipe.update(request.form) #enviamos el formulario completo para actualizar
    
    #redireccionar a dashboard

    return redirect('/dashboard')


@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    #validar que haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')   

    #borramos con función de modelo Recipe, primero creando un diccionario para agregar la id del form
    formulario = {"id" : id}
    Recipe.delete(formulario)


    #redirigimos a dashboard
    return redirect('/dashboard')


@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    #verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect('/')   

    #saber cual es el nombre del usuario que inició sesión
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario) #guardamos datos de usuario que inició sesión

    #mostrar la receta como instancia 
    #creamos un formulario receta para capturar el id
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta) #esta recipe

    #renderizar show_recipe.html
    return render_template('show_recipe.html', user=user, recipe = recipe) #es esta recipe


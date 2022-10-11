from flask_app.config.mysqlconnection import connectToMySQL

#importaciones para validaciones
from flask import flash 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #Función estática para validaciones
    @staticmethod
    def valida_usuario(formulario):
        #formulario = DICCIONARIO con todos los names y valores que el usuario ingresa
        es_valido = True
    
    #Validamos que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash('Nombre debe tener al menos 3 caracteres', 'registro')
            es_valido = False
        
        #Validamos que el apellido tenga al menos 3 caracteres
        if len(formulario['last_name']) < 3:
            flash('Apellido debe tener al menos 3 caracteres', 'registro')
            es_valido = False
        
            #Verificar que password tenga al menos 6 caracteres
        if len(formulario['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False

        #Verificamos que las contraseñas coincidan
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas NO coinciden', 'registro')
            es_valido = False

        #Revisamos que email tenga el formato correcto -> Expresiones Regulares
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail inválido', 'registro')
            es_valido = False

        #Consultamos si existe el correo electrónico
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('recetas').query_db(query, formulario)
        if len(results) >= 1:
            flash('E-mail registrado previamente', 'registro')
            es_valido = False
        
        return es_valido

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('recetas').query_db(query, formulario)

        return result #devuelve el id del nuevo registro que se realizó

    @classmethod
    def get_by_email(cls, formulario):
        #recibimos formulario = {email: elena@coding.com, password: 123}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        #siempre que es SELECT devuelve una lista
        if len(result) < 1: #significa que la lista está vacía y no existe ese mail
            return False
        else: 
            #Me regresa una lista con UN registro, correspondiente al usuario de ese email
            #result = [
            #    {id: 1, first_name: elena, last_name:de troya.....} -> POSICION 0
            #]
            user = cls(result[0]) #User( {id: 1, first_name: elena, last_name:de troya.....})
            return user 

    @classmethod
    def get_by_id(cls, formulario):
        #recibimos formulario = {id: 1}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        #result = [
            #    {id: 1, first_name: elena, last_name:de troya.....} -> POSICION 0
            #]
        user = cls(result[0]) #creamos una instnacia d User
        return user





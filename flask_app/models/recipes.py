from msvcrt import kbhit
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        #LEFT JOIN
        self.first_name = data['first_name']

    
    @staticmethod
    def valida_receta(formulario):
        es_valido = True 

        if len(formulario['name']) < 3:
            flash('El nombre de la receta debe tener al menos 3 caracteres', 'receta')
            es_valido = False
        
        if len(formulario['description']) < 3:
            flash('La descripción debe tener al menos tres caracteres', 'receta')
            es_valido = False 

        if len(formulario['instructions']) < 3:
            flash('Las instrucciones deben tener al menos tres caracteres', 'receta')
            es_valido = False
        
        if formulario['date_made'] == '':
            flash('Ingrese una fecha de creación', 'receta')
            es_valido = False
        
        return es_valido

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s)"
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result 

    @classmethod
    def get_all(cls):
        query = "SELECT recipes.*, users.first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('recetas').query_db(query)

        recipes = []
        #recipe = diccionario
        for recipe in results:
            recipes.append(cls(recipe)) #creamos instancia de Recipe y la agreamos a la lista
        
        return recipes


    @classmethod
    def get_by_id(cls, formulario):
        #formulario = {id : 1}
        query = "SELECT recipes.*, users.first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"       
        result = connectToMySQL('recetas').query_db(query, formulario) #selec siempre devuelve una lista
        recipe = cls(result[0]) #al ser un diccionario, necesitamos la posición 0 
        return recipe 

    @classmethod
    def update(cls, formulario): 
        #formulario = {"name:arroz, "descripcion": blabla}    
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s"
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario):    
        #formulario = {"id": 1}
        query = "DELETE FROM recipes WHERE id = %(id)s"  
        result = connectToMySQL('recetas').query_db(query, formulario)
        return result








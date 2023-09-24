from api import api
from flask import jsonify, make_response
from flask_restful import Resource, request
from .models import Pizza, Restaurant, RestaurantPizza, db

class Pizzas(Resource):
    def get(self):
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]    
        response =make_response(jsonify(pizzas), 200)
        return response

class Restaurants(Resource):
    def get(self):
        restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
        return make_response(jsonify(restaurants), 200)
    
class RestaurantsById(Resource):
    def get(self, id):
        
        restaurant = Restaurant.query.get(int(id))
        
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        
        pizzas = Pizza.query.join(RestaurantPizza).filter(RestaurantPizza.restaurant_id == id).all()
        pizza_dict = [pizza.to_dict() for pizza in pizzas]
        
        restaurant_dict = {
            "id":restaurant.id,
            "name":restaurant.restaurant_name,
            "address":restaurant.address,
            "pizzas":pizza_dict
        }
        
        response = make_response(jsonify(restaurant_dict), 200)
        return response

    def delete(self, id):
        restaurant = Restaurant.query.get(int(id))
        
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        
        pizzas = Pizza.query.join(RestaurantPizza).filter(RestaurantPizza.restaurant_id == id).all()
        
        for pizza in pizzas:
           db.session.delete(pizza)
        
        db.session.delete(restaurant)
        db.session.commit()
        
        response_body = {"message": "records successfully deleted"}
        response = make_response(jsonify(response_body), 200)
        return response
        
class RestaurantPizzas(Resource):
    def get(self):
        res_pizzas = [res_pizza.to_dict() for res_pizza in RestaurantPizza.query.all()]
        response = make_response(jsonify(res_pizzas), 200)
        return response
    
    def post(self):
        new_restaurant_pizza = RestaurantPizza(
            price = int(request.form["price"]),
            pizza_id = int(request.form["pizza_id"]),
            restaurant_id = int(request.form["restaurant_id"]),
        )
        
        try:
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            id = request.form["pizza_id"]
            pizza = Pizza.query.get(int(id))
            pizza_dict = pizza.to_dict()
                
            response = make_response(jsonify(pizza_dict), 200)
            return response  
        except:  
            return {"errors": ["validation errors"]} , 404   
        
        
    
api.add_resource(Pizzas, "/pizzas")    
api.add_resource(Restaurants, "/restaurants")
api.add_resource(RestaurantsById, "/restaurants/<int:id>")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")

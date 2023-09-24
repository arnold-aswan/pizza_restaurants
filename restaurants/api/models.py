# from api import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    serialize_rules = ('-pizzas.restaurant')

    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')
    
    def to_dict(self):
        return {
            "id":self.id,
            "restaurant_name":self.restaurant_name,
            "address":self.address,
            # "pizzas": self.pizzas #comment out and restaurant loads
        }
    
    def __repr__(self) -> str:
        return f'{self.restaurant_name}, {self.address}'
    
    @validates('name')
    def validate_name(self, key, name):
        words = name.split(" ")
        if key in name:
            raise ValueError("Name already exists")
        elif len(words) > 50:
            raise ValueError("Name must be less than 50 words") 
        
    
    
    
class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    serialize_rules = ('-restaurants.pizza')
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingridient = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())  
    
    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingridient': self.ingridient,
            # 'created_at': self.created_at,
            # 'updated_at': self.updated_at,
            # "restaurants":self.restaurants #comment out and pizza loads
        }
    
    def __repr__(self) -> str:
        return f'{self.name} {self.ingridient} {self.created_at} {self.updated_at}'



class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    serialize_rules = ('-pizza.restaurants', '-restaurant.pizzas')
    
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurants')
    
    def to_dict(self):
        return {
            "id":self.id,
            "pizza_id":self.pizza_id,
            "restaurant_id":self.restaurant_id,
            "price": self.price,
            # "restaurant":self.restaurant,
            # "pizza":self.pizza
        }
    
    def __repr__(self) -> str:
        return f'{self.pizza_id}, {self.restaurant_id} {self.price}'
    
    @validates('price')
    def validate_price(self, key, price):
        if price < 1 and price > 30:
            raise ValueError("Price must be between 1 and 30")
        return price
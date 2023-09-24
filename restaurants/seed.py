from random import randint, choice as rc
from faker import Faker
from api import app
from api.models import db, Pizza, Restaurant, RestaurantPizza

pizza_names = [
    "Cheese Pizza", 
    "Veggie Pizza", 
    "Pepperoni Pizza", 
    "Meat Pizza", 
    "Margherita Pizza", 
    "BBQ Chicken Pizza",
    "Hawaiian Pizza",
    "Buffalo Pizza",
]

pizza_ingridient = [
    "Pepperoni",
    "Mushroom",
    "Extra cheese",
    "Sausage",
    "Onion",
    "Black olives",
    "Green pepper",
    "Fresh garlic"
]

fake = Faker()

with app.app_context():
    Pizza.query.delete()
    Restaurant.query.delete()
    RestaurantPizza.query.delete()
    
    pizzas = []
    for i in range(10):
        pizza = Pizza(
            name=rc(pizza_names),
            ingridient = rc(pizza_ingridient),
        )
        pizzas.append(pizza)
    db.session.add_all(pizzas) 
    
    restaurants = []
    for i in range(10):
        rest_name = fake.company()
        address = fake.address()
        
        if rest_name and address:  
            restaurant = Restaurant(
            restaurant_name=rest_name,
            address=address,
            )  
            restaurants.append(restaurant)
    db.session.add_all(restaurants)   
    
    restaurantpizzas = [] 
    for p in pizzas:
        for i in range(randint(1,4)):
            rp = RestaurantPizza(
                price = randint(1, 30),
                pizza = p,
                restaurant = rc(restaurants),
            )
            restaurantpizzas.append(rp)
    db.session.add_all(restaurantpizzas)
    
        
    db.session.commit()         
    print(restaurants)
        
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId to handle MongoDB _id fields

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB Configuration
MONGO_URI = "mongodb+srv://adivasinilambariherbalhairoil:Omkar123@cluster0.cwjj9.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['test']
orders_collection = db['orders']

# Check DB connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Helper function to get order count
def get_order_count():
    return orders_collection.count_documents({})

# Routes
@app.route('/')
def index():
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    try:
        orders = list(orders_collection.find())
        order_count = get_order_count()
        return render_template('orders.html', orders=orders, order_count=order_count)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/order/<string:order_id>')
def order_details(order_id):
    try:
        # Convert order_id to ObjectId for querying
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
        if order:
            order_count = get_order_count()
            return render_template('order_details.html', order=order, order_count=order_count)
        else:
            return f"Order with ID {order_id} not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/order/update/<string:order_id>', methods=['POST'])
def update_order_status(order_id):
    try:
        new_status = request.form.get('status')
        result = orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"orderStatus": new_status}}
        )
        if result.matched_count:
            return redirect(url_for('order_details', order_id=order_id))
        else:
            return f"Failed to update order with ID {order_id}.", 400
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)

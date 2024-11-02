from flask import Flask, render_template,  request, jsonify

from flask_mail import Mail, Message

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/about')
def about():


    return render_template('about.html')


@app.route('/feedback')
def feedback():

    return render_template('feedback.html')


@app.route('/payment')
def payment():

    return render_template('payment.html')

import os
import random
@app.route('/books')
def books():
    products_folder = 'static/img/products'
    products = []
    for filename in os.listdir(products_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # Extract product name from the filename (without extension)
            product_name = os.path.splitext(filename)[0]

            # Generate a random price between 15 and 25
            price = round(random.uniform(15, 25), 2)

            category = get_category_for_product(product_name)

            # Append product details to the products list
            products.append({'name': product_name, 'image': filename, 'price': price, 'category': category})

            # Append product details to the products list
    categorized_products = categorize_products(products)

    # Render the HTML template with the categorized products data
    return render_template('books.html', categorized_products=categorized_products)

def get_category_for_product(product_name):
    # Simple logic to determine the category based on the product name
    if 'marketing' in product_name.lower():
        return 'Marketing'
    elif 'accounting' in product_name.lower():
        return 'Accounting'
    elif 'hr' in product_name.lower():
        return 'HR'
    elif 'logistics' in product_name.lower():
        return 'Logistics'
    else:
        return 'Other'

def categorize_products(products):
    # Organize products into categories
    categorized_products = {'Marketing': [], 'Accounting': [], 'HR': [], 'Logistics': []}

    for product in products:
        category = product['category']
        categorized_products[category].append(product)

    return categorized_products


@app.route('/booking', methods=['GET','POST'])
def booking():


    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']

        if not (name and email and date and time):
            return 'All fields are required', 500


        # Create message
        email_message = f"Confirmed looking forward to see soon {name} This is a friendly reminder about your appointment on {date} at {time} "

        try:

             # Configure your email settings
            sender_email = get.env("email")
            sender_password = get.env("password")
            receiver_email = str(email)
            app.config['MAIL_SERVER']= 'smtp.gmail.com'
            app.config['MAIL_PORT']= 465
            app.config['MAIL_USERNAME']= sender_email
            app.config['MAIL_PASSWORD']= sender_password
            app.config['MAIL_USE_TLS']= False
            app.config['MAIL_USE_SSL']= True

            mail = Mail(app)

            msg = Message(subject= "Confirmation", sender= email, recipients= [receiver_email])

            msg.body = email_message
            mail.send(msg)


            success_message = ' Your Parking is Confirmed successfully!'
            return render_template('booking.html', success_message=success_message)
        except Exception as e:
            error_message = "some thing goning wroing :",str(e)
            return render_template('booking.html', error_message=error_message)


    return render_template('booking.html')




if __name__ == '__main__':
    app.run(debug=True)



import os
from flask import Flask, render_template, request
import stripe

stripe_keys = {
  'secret_key': 'sk_test_868yYR6rMBn6ZwOhQvZuHQRj',
  'publishable_key': 'pk_test_g4HiFOzaY8OGqRmhmTKxmckM'
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='aud',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    app.run(debug=True)
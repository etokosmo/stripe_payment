# Stripe Payment Service

## About

Service for creating a payment form for products.

## Website example

You can see this project [here](https://etokosmo.ru/api/items/).

Items Example

![image](https://github.com/etokosmo/stripe_payment/blob/main/images_for_readme/Buy%20items.gif)

Item Example

![image](https://github.com/etokosmo/stripe_payment/blob/main/images_for_readme/Buy%20item.gif)


## API

You can send GET request to `http://<YOUR_DOMEN>/api/buy/<int:item_id>`.

You will get Stripe SessionID to payment for item.

<details>
  <summary>Example</summary>

#### Request
`http://127.0.0.1:8000/api/buy/<int:item_id>`

#### Response
```json
{"sessionId": "cs_test_a1eqvWY7lQpQ7TjbRIt5TY6nAj4X5VE1cdEvKARktYr1nQuZrSw2Iiqzu3"}
```
</details>

You can send POST request to `http://<YOUR_DOMEN>/api/buy/`.

You will get Stripe SessionID to payment for cart items.

<details>
  <summary>Example</summary>

#### Request
`http://127.0.0.1:8000/api/buy/`

Headers:
```
'Content-type': 'application/json; charset=UTF-8',
'X-CSRFToken': '{{csrf_token}}'
```

Body:
```json
{
    "id": 2,
    "img": "/media/Mentos-Mint.jpg",
    "name": "Ментос",
    "price": "50",
    "quantity": 1
}

# Also can include
    "customer_firstname": "User",
    "customer_lastname": "Customer",
    "customer_address": "Somewhere",
    "customer_promocode": "Undefined",
```

#### Response
```json
{"sessionId": "cs_test_a1eqvWY7lQpQ7TjbRIt5TY6nAj4X5VE1cdEvKARktYr1nQuZrSw2Iiqzu3"}
```
</details>

## Configurations

* Python version: 3.10
* Libraries: [requirements.txt](https://github.com/etokosmo/foodplan/blob/main/requirements.txt)

## Launch

### Local server

- Download code
- Through the console in the directory with the code, install the virtual environment with the command:
```bash
python3 -m venv env
```

- Activate the virtual environment with the command:
```bash
source env/bin/activate
```

- Install the libraries with the command:
```bash
pip install -r requirements.txt
```

- Write the environment variables in the `.env` file in the format KEY=VALUE

`SECRET_KEY` - A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.

`ALLOWED_HOSTS` - A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations.

`DEBUG` - A boolean that turns on/off debug mode. If your app raises an exception when DEBUG is True, Django will display a detailed traceback, including a lot of metadata about your environment, such as all the currently defined Django settings (from settings.py).

`DATABASE_URL` - URL to db. For more information check [this](https://github.com/jazzband/dj-database-url).

`STRIPE_PUBLIC_KEY` - Stripe public API key. For more information check [this](https://stripe.com/docs/keys).

`STRIPE_SECRET_KEY` - Stripe secret API key. For more information check [this](https://stripe.com/docs/keys).

- Create your database with the command:
```bash
python manage.py makemigrations
python manage.py migrate
```

- Run local server with the command (it will be available at http://127.0.0.1:8000/):
```bash
python manage.py runserver
```

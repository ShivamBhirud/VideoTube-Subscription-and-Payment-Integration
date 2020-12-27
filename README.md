Installations Required-
1. Set up your Virtual Environment
2. Install all of the required packages from requirement.txt file.
	$ pip install -r /path/to/requirements.txt


How to run the code?

1. Open an account on Stripe developer's for testing: https://dashboard.stripe.com/
2. You need your Public and Private/Secret keys from the stripe. Find it at: https://dashboard.stripe.com/test/apikeys
3. cd to the folder where Django's manage.py file is present.
4. Open settings.py file and update the Public and Private Keys that you got from stripe.
5. Make migrations so that the SQlite DB would be created in your local: 
	$ python manage.py makemigrations
	$ python manage.py migrate
6. Run the project: $ python manage.py runserver
7. Signup as suggested on the signup page of the project and Login with your creds.
7. For making dummy payment use card number as 4242 4242 4242 4242, Expiry date can be any one from the future, and CVV should be any three digit number.
8. You will see the payment on your stripe dashboard once done.

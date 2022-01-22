# hotel-reservations
A simple Flask webservice for making and managing ones reservations.

## Requirements 
- Python => 3.7

## Installation
- Python Modules: `pip install flask flask-sqlalchemy flask-login`

## How-to Run
- Set `FLASK_APP` environment variable: `export FLASK_APP=hotel_service`.
- Now head over to http://127.0.0.1:5000/, and you should see your login page.
- If you cannot use your loopback ip, just run by setting the `host` flag: `flask run --host=0.0.0.0`.
- If you also require to change the port to another, use the `port` flag `flask run --port=5555`.
- For debugging mode, specify the `FLASK_ENV` environment variable: `export FLASK_ENV=development`.

## Routing

> __*__ Indicates users require authentication.

- \*<`/`:**GET**> - Lists all available reservations.
- \*<`/profile`:**GET**> - Users profile information and active reservations.
- <`/login`:**GET**> - User login interface 
- <`/login`:**POST**> - Validates the users credentials with the database.
- \*<`/login`:**POST**> - Clears the users login session from the LoginManager.
- <`/signup`:**GET**> - User signup interface 
- <`/signup`:**POST**> - Verifies the validity of the provided user data with already known accounts, ensuring no duplicates.
- \*<`/listing/<id>`:**GET**> - Interface for the retrieved information for a given listing from the database.
- \*<`/listing/<id>/reserve/<check-in>/<check-out>`:**POST**> - Reserves a listing for the listing id of the logged-in user.
- \*<`/listing/<id>/unreserve`:**POST**> - Unreserves the listing for the listing id of the logged-in user.


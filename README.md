# SendITAPI-V2
[![Maintainability](https://api.codeclimate.com/v1/badges/75b6c19f46773ff41381/maintainability)](https://codeclimate.com/github/MandelaK/SendIT-API-V2/maintainability)  

[![codecov](https://codecov.io/gh/MandelaK/SendIT-API-V2/branch/develop/graph/badge.svg)](https://codecov.io/gh/MandelaK/SendIT-API-V2)
[![Build Status](https://travis-ci.com/MandelaK/SendIT-API-V2.svg?branch=develop)](https://travis-ci.com/MandelaK/SendIT-API-V2)



 SendIT is an application that allows users to create parcel deliveries and send them out. With this version, we implement a persistent database to our SendIT API. The following features are implemented:
	- Users can create parcel delivery orders
	- Users should be able to change destination for orders in transit
	- Users can sign up and log in
	- Admins should be able to change the current location of deliveries in transit
	- Admins can change the status of parcels that haven't been delivered yet
	- The price of a delivery is determined by weight
	- All information is stored in a persistent database
	- All endpoints are secured by JWT


V2 of our API implements the following endpoints:


**EndPoint**                          			**Functionality**


POST /auth/signup			-		Register a user

POST /auth/login			-		Login a user

PUT /parcels/<parcelId>/destination	-		Change the location of a specific parcel delivery order
							Only the user who created the parcel delivery order should be able to change the destination of the parcel.

PUT /parcels/<parcelId>/status		-		Change the status of a specific parcel delivery order
							This endpoint should be accessible by the Admin only.

PUT /parcels/<parcelId>/presentLocation -		Change the present location of a specific parcel delivery order
							This endpoint should be accessible by the Admin only.

GET /users/parcels     			-               Fetch all parcel delivery orders by one user. 
							Users can only see orders they created.

GET /parcels				-		Fetch all parcels in database.
							Only admin can fetch all parcels in the database

POST /users/parcels			-		Create a delivery order
							Only logged in users can use this endpoint


**To install this repository**
- clone it - $ git clone https://github.com/MandelaK/SendITAPI-V2
- create a virtual environment by doing python3 -m venv env and activating your environment with source /env/bin/activate (if you're in the same directory as your virtual environment
- do pip install -r requirements.txt while in your active environment

**To test on Postman:**
- Open Postman and access the following endpoints:
  - `localost:/api/v2/users/parcels` - Send a POST request to this URL, but ensure your input is JSON and has the following fields filled:
	- parcel_name - string type
	- destination - string type
	- weight - integer, must be greater than zero
	- recipient_name - string type
  - `localhost:/api/v2/users/parcels` - This endpoint accepts GET requests and returns all parcels sent by the user who is currently logged in.
  - `localhost:/api/v2/parcels` - Send a GET request to this URL to get all parcels in the database. Only accessible to admins.
  - `localhost:/api/v2/auth/signup` - Send a POST request to this URL to create an account. Fill in the following fields:
	- email
	- First Name
	- Last Name
	- Password
	- Phone, this is the only field not required
  - `localhost:/api/v2/auth/login` - Send a POST request to this URL to log in. You must provide a valid email address and password. If you have no account, you will be asked 	to create one.
  - `localhost:api/v2/parcels/<parcelId>/destination` - This endpoint accepts only PUT requests and allows you to change the destination. Only admin can use this endpoint but must provide valid destination and the parcel must be in transit.
  - `localhost:api/v2/parcels/<parcelId>/status` - Only PUT requests are accepted by this endpoint. Only the admin may use it to change the status of parcels that have not been delivered yet.
  - `localhost:api/v2/parcels/<parcelId>/presentLocation` - Only PUT requests are accepted by this endpoint and only admins can change the location of parcels that are in transit.

**How to test**
- As long as you've installed all dependencies, you can run `pytest` from terminal and it will show you which tests pass.


You can find the Heroku app published here - 

The frontend for this application is available here - https://mandelak.github.io/SendIT/UI/static/html/index.html

Version 1 of this API is found here - https://github.com/MandelaK/SendIT-API

The repository for the UI can be found here - https://github.com/MandelaK/SendIT



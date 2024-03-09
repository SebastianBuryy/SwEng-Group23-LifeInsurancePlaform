from flask import Flask, request, jsonify # may require you to run `pip install flask` on your machine
from flask_cors import CORS, cross_origin # `pip install -U flask-cors`
from services import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# home page of backend
@app.route("/")
def main():
  return "hello world!"
# make similar "pages" that handle get, post, etc. requests to api.

#This route handles Get and Post requests to the overall database
@app.route('/api/customers', methods =['GET', 'POST'])        #define /customers endpoint for methods Get and Post
def customers_Request():
  if request.method == 'GET' :                          #if request is a Get
    return get_customer('all'), 200               # return the database in json format and status code 200(OK)
  elif request.method == 'POST':                        #else if request is a Post
      newCustomer = request.get_json()                  # newCustomer stores values passed from request 
      return add_customer(newCustomer), 201  #return the data in a dictionary in json format alongside status 201(Created)
    

@app.route('/api/customers/<int:id>/<string:itemtoAccess>', methods=['GET', 'PUT', 'DELETE']) #define /customers/id/itemtoAccess endpoint for methods Get, Post and Delete
def customer_Item_Request(id, itemtoAccess):                                                              #if passed id is present in databse
  if request.method == 'GET':                                                            #  if request is a Get
    item = get_customer(id, itemtoAccess)
    if item != None:           #    if passed item is in customer with passed id or passed item is "all"
      return item, 200                                         #      return corresponding item and status code 200(OK)
    else:                                                                                #      else return item not found error and status 404(Not Found)
      return {'error' : 'item not found'}, 404   
  elif request.method == 'PUT':                                                         #  else if request is a Post
    item = get_customer(id, itemtoAccess)
    if itemtoAccess not in db.customerDatabase[id]:                                         #    if itemtoAccess does not already exist in specified customer   
      newItem = request.get_json()                                                       #      store passed json in newItem                                 
      return add_item(id, newItem, itemtoAccess), 201                                          #      return specified customer and status 201(Created)
  elif request.method == 'DELETE':                                                       #  else if request is Delete
    if itemtoAccess in db.customerDatabase[id] or itemtoAccess.lower() == 'all':            #    if itemtoAccess exists or is "all"
      db.delete_Value(id, itemtoAccess)                                                     #      delete specified customer's item or all customer's data
      return {}, 204                                                       #      return error code 204(No Content)
#      else:                                                                                #    else return item not found error and status 404(Not Found)
  return {'error' : 'id or item not found'}, 404
  # 404 is not used like this, its used when the api endpoint was not found
  
@app.route('/api/customers/<int:id>/update', methods=['PUT'])   #define endpoint /customers/id/update for method Patch
def update_Customer(id): 
  if id in db.customerDatabase:                                  #if id is present in database
    updatedValues = request.get_json()                        # store json passed with the request in updatedValues                       
    return update_customer(id, updatedValues), 200   # return customer's data along with status 200(OK)
  else:
    return {'error' : 'id not found'}, 404                    #else return error id not found and status 404(Not Found)

@app.route('/api/login', methods=['POST', 'GET'])
def login_to_Account():
  arguments = request.args
  emailAddress = arguments.get("emailAddress", "")
  #for POST request, url must be /api/login?emailAddress=x
  #where x is email address to be used to sign up
  if request.method == 'POST':
    if emailAddress not in login.Users:
      signupDetails = request.get_json()
      return login.add_Details(emailAddress, signupDetails), 201
    else:
      return {'error' : 'Email Address already in use'}, 401
  #for GET request, url must be /api/login?emailAddress=x&password=y
  #where x is email address and y is password used to sign in  
  elif request.method == 'GET':     
    if emailAddress in login.Users:
      password = arguments.get("password", "")
      result = login.attempt_Login(emailAddress, password)
      if result == None:
        return {'error' : 'Your password is incorrect'}, 400
      else:
        return sid.add_Session_id(emailAddress), 200    #Placeholder, unsure of what to do upon success
    else:
      return {'error' : 'invalid email address'}, 400
  

if __name__ == '__main__':
  app.run()



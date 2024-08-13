# app.py
#
# import of the libraries
import os
import uuid
import boto3

from flask import Flask, jsonify, request

app = Flask(__name__) # flask initialization.
#
# Retrieve the DynamoDB table name from environment variables, serverless.yml
USERS_TABLE = os.environ['USERS_TABLE']
client = boto3.client('dynamodb')        # Selection of the DB
#
# route decorator in Flask of the introduction function.
@app.route("/")
def hello():
    """
    Basic route that returns a simple message.
    """
    return "Hello, welcome to my small project for the hire."
#
# route decorator in Flask of the get_user_by_id
@app.route("/users/<string:user_id>")
def get_user_by_id(user_id):
    """
    Retrieves a user from the DynamoDB table given a user ID.

    Args:
        user_id (str): The user ID that we want to retrieve

    Returns:
        JSON response containing the user details or an error message.
    """
    # Get the user item from DynamoDB by userId using the Key on the selected user table.
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': { 'S': user_id }
        }
    )
    
    # Get the item from the response to see how it went the exection of the query
    item = resp.get('Item')
    
    # If the item doesn't exist, return a 404 error
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    # Return the user details as a JSON response in case the response is positive.
    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S'),
        'email': item.get('email').get('S'),
        'password': item.get('password').get('S')
    })

# route decorator in Flask of the create_user
@app.route("/users", methods=["POST"])

def create_user():
    """
    Creates a new user in the DynamoDB table.

    Request JSON Body:
        - name (str): The name of the user.
        - email (str): The email of the user.
        - password (str): The password of the user.

    Returns:
        JSON response containing the created user details.
    """
    # Generate a unique user ID with the uuid function
    user_id = uuid.uuid4().hex
    
    # Retrieve user details from the request body
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Check if the email contains '@' and raise an error if it does not
    if '@' not in email:
        return jsonify({'error': "Email should contain the '@' character, as it's likely an email."}), 400

    # Check if the password contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return jsonify({'error': "Password must contain at least one uppercase letter."}), 400

    # Check if all required fields are provided
    if not name or not email or not password:
        return jsonify({'error': 'Please provide complete user information (name, email, and password).'}), 400

    # Check if a user with the same userId already exists
    response = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )
    
    if 'Item' in response:
        return jsonify({'error': 'User with this ID already exists.'}), 400

    # Insert the new user into DynamoDB if the userId is unique
    client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id },
            'name': {'S': name },
            'email': {'S': email},
            'password': {'S': password}
        }
    )

    # Return the created user details as a JSON response
    return jsonify({
        'userId': user_id,
        'name': name,
        'email': email,
        'password': password
    })


# route decorator in Flask of the delete_user
@app.route("/users/delete", methods=["POST"])
def delete_user():
    """
    Deleting a user from the DynamoDB table.

    Request JSON Body:
        - userId (str): The ID of the user to delete.

    Returns:
        JSON response confirming the deletion or an error message in case of failing.
    """
    # Retrieve the user ID from the request body
    user_id = request.json.get('userId')
    
    # Ensure a valid user ID is provided, if not an error is raised
    if not user_id:
        return jsonify({'error': 'Please provide a valid user id'}), 400

    # First, check if the user exists in the database
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )
    # Getting the item from the response
    item = resp.get('Item')
    
    # If the user doesn't exist, return a 404 error
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    # If the user exists, delete the user from DynamoDB
    client.delete_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )

    # Return a confirmation message with the information of the deleted user.
    return jsonify({
        'message': f'User with ID {user_id} has been deleted',
        'deletedUserId': user_id
    }), 200

# route decorator in Flask of the update the user.
@app.route("/users/update", methods=["POST"])
def update_user():
    """
    Updates user information in the DynamoDB table.

    Request JSON Body:
        - userId (str): The ID of the user to update.
        - name (str, optional): The new name of the user.
        - email (str, optional): The new email of the user.
        - password (str, optional): The new password of the user.

    Returns:
        JSON response confirming the update or an error message.
    """
    # Retrieve user details from the request body
    user_id = request.json.get('userId')
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    # Ensure a valid user ID is provided
    if not user_id:
        return jsonify({'error': 'Please provide a valid user id'}), 400

    # Check if the email contains '@' and raise an error if it does not
    if '@' not in email:
        return jsonify({'error': "Email should contain the '@' character, as it's likely an email."}), 400

    # Check if the password contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return jsonify({'error': "Password must contain at least one uppercase letter."}), 400

    # Build the update expression and attribute values for the update
    update_expression = "SET " # indicating that we are setting new values for attributes
    expression_attribute_names = {} # useful when your attribute names might conflict with DynamoDB reserved words.
    expression_attribute_values = {} # This dictionary maps placeholders to the actual values you want to set in the DynamoDB table

    # Conditionally add attributes to the update expression and before to do it it checks if it's different from empty
    # in order to avoid conflicts.

    if name is not None:
        update_expression += "#n = :n, "
        expression_attribute_names["#n"] = "name"
        expression_attribute_values[":n"] = {"S": name}

    if email is not None:
        update_expression += "email = :e, "
        expression_attribute_values[":e"] = {"S": email}

    if password is not None:
        update_expression += "password = :p, "
        expression_attribute_values[":p"] = {"S": password}

    # Remove the trailing comma and space from the update expression
    update_expression = update_expression.rstrip(", ")

    # Update the user in the DynamoDB table basing on the key on the table given the new value provided
    try:
        response = client.update_item(
            TableName=USERS_TABLE,
            Key={
                'userId': {'S': user_id}
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
 
        # Return a confirmation message with the updated attributes in case is positve
        return jsonify({
            'message': f'User with ID {user_id} has been updated',
            'updatedAttributes': response.get('Attributes')
        }), 200

    except Exception as e:
        # Handle any errors that occur during the update process, this is a general purpose exception.
        return jsonify({'error': str(e)}), 500

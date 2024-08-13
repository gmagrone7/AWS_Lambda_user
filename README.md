<!--
title: 'Users management by using Serverless Framework Python Flask API service backed by DynamoDB on AWS using AWS Lambdas'
description: 'This template demonstrates how to develop and deploy a simple user management Python Flask API service backed by DynamoDB running on AWS Lambda using the Serverless Framework.'
layout: Doc
framework: v4
platform: AWS
language: Python
priority: 2
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, Inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Users CRUD management by using Serverless Framework Python Flask API service backed by DynamoDB on AWS using AWS Lambdas.

## **Index**
-   [Introduction](#introduction)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Configuration](#configuration)
-   [Deployment](#deployment)
-   [API Endpoints](#api-endpoints)
    -   [Root Endpoint](#root-endpoint)
    -   [Get User by ID](#get-user-by-id)
    -   [Create User](#create-user)
    -   [Delete User](#delete-user)
    -   [Update User](#update-user)
-   [Error Handling](#error-handling)
-   [Testing](#testing)
-   [Contributing](#contributing)
-   [License](#license)

## **1. Introduction**

This project is a serverless Flask application designed for managing user data using AWS DynamoDB. 
The application provides a RESTful API for creating, retrieving, updating, and deleting users. It's deployed on AWS using the Serverless Framework and the AWS lambdas.

## **2. Prerequisites**

Before to start, is important to check if these prerequisities are installed :

-   Python 3.12+
-   AWS CLI configured with appropriate access(if you don't have an account you should create one)
-   Node.js and npm (for Serverless Framework)
-   Serverless Framework installed globally (`npm install -g serverless`)
-  Install also serverless-wsgi and serverless-api-gateway-throttling
(`npm install serverless-wsgi`)
(`npm install serverless-api-gateway-throttling`)
- Also install this
(`serverless dynamodb install`)

## **3. Installation**

To install and set up the project locally:

1.  Clone the repository:  
    `git clone <https://github.com/gmagrone7/AWS_Lambda_user>
    cd <YOUR REPOSITORY>` 
    It's suggested to use git to do this.
    
2.  Install Python dependencies:
    `pip install -r requirements.txt` 
    
3.  Install Serverless plugins and dependencies:
    `npm install` 
    

## **4. Configuration**

We install the serverless framework and from it we initialized a flask application, starting from that point we just used this two file that we used to create and develop the application.

-   **serverless.yml**: This file contains the configuration for deploying the application, including the provided details, the plugins, environment variables, and resource definitions, used for the table.
-  **app.py**:  This is the main application file, this contains the Flask routes and the logic for interacting with the DynamoDB moreover here it's stored the code related to the CRUD function for the user.


## **5. Deployment**

To deploy the application to AWS:

1.  Ensure your AWS credentials are configured correctly, if they are not you need to generate a key from your AWS dashboard and you need to change the settings to make it works with your AWS console
2.  Deploy the application using Serverless Framework:
    `serverless deploy` 
    
3.  After deployment, note the API Gateway URL provided in the output, those are the one that now you can use to work with the server function.

**After the execution you will see something like this:**
Packaging Python WSGI handler...

✔ Service deployed to stack aws-python-flask-dynamodb-api-dev (123s)

endpoints:
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
functions:
  api: aws-python-flask-dynamodb-api-dev-api (41 MB)

-   `USERS_TABLE`: The name of the DynamoDB table used for storing user data. This is dynamically set in `serverless.yml` .

## **6. API Endpoints**

### **Root Endpoint**
This is used to access to the mainpage, it's just the root and it's a good practice because it allow to redirect to the other function
-   **URL**: `/`
-   **Method**: `GET`
-   **Description**: Returns a welcome message to state that you enter into  the page.
-   **Response**:
    -   `200 OK`: "Hello, welcome to my small project for the hire."

### **Get User by ID**
The function used to retrieve the user given the id 
-   **URL**: `/users/<string:user_id>`
-   **Method**: `GET`
-   **Description**: Retrieves a user by `user_id`.
-   **Response**:
    -   `200 OK`: JSON object with user details.
    -   `404 Not Found`: User does not exist.

### **Create User**
The function used to create a new user 
-   **URL**: `/users`
-   **Method**: `POST`
-   **Description**: Creates a new user.
-   **Request Body**:
    -   `name`: String, required.
    -   `email`: String, required (must contain `@`).
    -   `password`: String, required (must contain at least one uppercase letter).
-   **Response**:
    -   `201 Created`: JSON object with created user details.
    -   `400 Bad Request`: Validation errors.

### **Delete User**
The function used to delete a user
-   **URL**: `/users/delete`
-   **Method**: `POST`
-   **Description**: Deletes a user.
-   **Request Body**:
    -   `userId`: String, required.
-   **Response**:
    -   `200 OK`: Confirmation message.
    -   `404 Not Found`: User does not exist.

### **Update User**
The function used to update a user
-   **URL**: `/users/update`
-   **Method**: `POST`
-   **Description**: Updates user information.
-   **Request Body** (all fields optional except `userId`):
    -   `userId`: String, required.
    -   `name`: String, optional.
    -   `email`: String, optional.
    -   `password`: String, optional.
-   **Response**:
    -   `200 OK`: Confirmation message with updated attributes.
    -   `400 Bad Request`: errors.

## **7. Error Handling**

The Handling of the errors its crucial due to the fact that it can interrupt or block the services due this we implement two methods:

-   The API returns appropriate HTTP status codes and error messages in JSON format for different scenarios such as validation errors, missing data, and server issues.
-  Throttling to avoid a too big number of access to the resouces.

## **8. Testing**

-   To test the application locally:
    1.  Run the Flask app:
        `flask run` 
    2.  Use tools like Postman or `curl` to test the endpoints.
 - To test the application remote:
    1.  Run the deployment:
        `serverless deploy` 
    2.  Use tools like Postman or `curl` to test the endpoints, in our case we used Postman to test the application and to see how the endpoints were working.
 


## **9. Contributing**
The following link has been used to study and to develop the application
-   [AWS Free Plan](https://aws.amazon.com/it/free/?trk=ps_a134p000003yhgtAAA&trkCampaign=acq_paid_search_brand&sc_channel=ps&sc_campaign=acquisition_IT&sc_publisher=google&sc_category=core-main&sc_country=IT&sc_geo=EMEA&sc_outcome=Acquisition&sc_detail=amazon%20web%20services&sc_content=Brand_amazon_web_services_e&sc_matchtype=e&sc_segment=455721528617&sc_medium=ACQ-P%7CPS-GO%7CBrand%7CDesktop%7CSU%7CCore-Main%7CCore%7CIT%7CEN%7CText&s_kwcid=AL!4422!3!455721528617!e!!g!!amazon%20web%20services&ef_id=EAIaIQobChMI_NPSh_vo7QIVEL_tCh18rQGNEAAYASAAEgJnl_D_BwE:G:s&s_kwcid=AL!4422!3!455721528617!e!!g!!amazon%20web%20services&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc)
    
-   [AWS lambda](https://aws.amazon.com/it/lambda/)
    
-   [AWS DynamoDB](https://aws.amazon.com/it/dynamodb/)
    
-   [AWS API Gateway](https://aws.amazon.com/it/api-gateway/)
    
-   [Serverless Framework Quick Start](https://www.serverless.com/framework/docs/providers/aws/guide/quick-start/)

## **10. License**

This template demonstrates how to develop and deploy a simple Python Flask API service, backed by DynamoDB, running on AWS Lambda using the Serverless Framework.

This template configures a single function, `api`, which is responsible for handling all incoming requests thanks to configured `http` events. To learn more about `http` event configuration options, please refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/). 

As the events are configured in a way to accept all incoming requests, `Flask` framework is responsible for routing and handling requests internally. 

The implementation takes advantage of `serverless-wsgi`, which allows you to wrap WSGI applications such as Flask apps. 

Additionally, the template also handles provisioning of a DynamoDB database that is used for storing data about users.







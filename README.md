# 📬 MESSAGES REST API

## 📖 Overview
The Message API provides functionality for creating, updating, and deleting messages. It also provides endpoints for retrieving messages related to the authenticated user.

## 📝 Fields

| Field             | Description                                                                                | Required        |
|-------------------|--------------------------------------------------------------------------------------------|-----------------|
| `message_from`    | Foreign key to the User model representing the sender of the message                       | Yes             |
| `message_to`      | Foreign key to the User model representing the recipient of the message                    | Yes             |
| `message_title`   | CharField with a maximum length of 255 characters, representing the title of the message   | Yes             |
| `message_content` | CharField with a maximum length of 255 characters, representing the content of the message | Yes             |
| `created_at`      | DateTimeField set to auto_now_add, representing the timestamp when the message was created | Automatically set  |
| `is_viewed`       | BooleanField with a default value of False, indicating whether the message has been viewed | Automatically set  |
| `viewed_at`       | DateTimeField allowing null and blank values, representing the timestamp when the message was viewed | Optional |

## 🔐 Authentication
This API uses Token Authentication. The token should be included in the Authorization header with the Token keyword, like so: 

```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

# Endpoints for users
```code
## GET /api/messages/
Retrieve a list of all messages related to the authenticated user.
```

```code
## GET /api/messages/{id}/
Retrieve a specific message by its ID. If the message is not viewed, it will be marked as viewed.
```
Example:

GET /api/messages/ Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b


Response:
```json
[
    {
        "id": 21,
        "message_from": "test10",
        "message_to": "admin",
        "message_title": "Hi",
        "message_content": "Open your inbox",
        "created_at": "2024-02-20T01:54:46.603375Z",
        "is_viewed": false,
        "viewed_at": null
    },
    ....
]
```

POST /api/messages/
Create a new message. The request body should include message_to, message_title, and message_body.

Example:

POST /api/messages/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

Request:
```json
JSON

{
    "message_to": "admin",
    "message_title": "Hi",
    "message_content": "Open your inbox",
    "created_at": "2024-02-20T01:54:46.603375Z",
}
```
GET /api/messages/get_user_received_messages/
Retrieve all received messages for the authenticated user.

Example:

GET /api/messages/get_user_received_messages/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

Response:

JSON
```json
[
    {
        "id": 1,
        "message_from": "user1",
        "message_to": "user2",
        "message_title": "Hello",
        "message_body": "Hello, user2!",
        "is_viewed": true
    },
    ...
]
```
GET /api/messages/get_unread_messages/
Retrieve all unread messages for the authenticated user.

Example:

GET /api/messages/get_unread_messages/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

Response:

JSON
```json
[
    {
        "id": 1,
        "message_from": "user1",
        "message_to": "user2",
        "message_title": "Hello",
        "message_body": "Hello, user2!",
        "is_viewed": false
    },
    ...
]
```
# Endpoints for staff

GET /api/messages/get_user_messages/{user_pk}/
API for staff only, Retrieve all messages for the specified user.

Example:
GET /api/messages/get_user_messages/user2/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```json
JSON
[
    {
        "id": 1,
        "message_from": "user1",
        "message_to": "user2",
        "message_title": "Hello",
        "message_body": "Hello, user2!",
        "is_viewed": true
    },
    ...
]
```

GET /api/messages/get_unread_messages_by_user/
API for staff only, Retrieve all unread messages for the specified user.

Example:
GET /api/messages/get_unread_messages_by_user/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```json
JSON
[
    {
        "id": 1,
        "message_from": "user1",
        "message_to": "user2",
        "message_title": "Hello",
        "message_body": "Hello, user2!",
        "is_viewed": false
    },
    ...
]
```
Error Codes
```code
400 BAD REQUEST: Returned when the message_to user does not exist in a POST /api/messages/ request.
401 UNAUTHORIZED: Returned when the user is not authenticated for GET /api/messages/get_unread_messages/ and GET /api/messages/
get_unread_messages_by_user/ requests.
```


# ############################################################################

# 📬 UserViewSet API

This is a ModelViewSet for the User model. It handles creating and updating users.

## 📖 Endpoints

- `GET /users/`: List all users, ordered by id.
- `POST /users/`: Create a new user.
- `GET /users/{id}/`: Retrieve the details of a specific user.
- `PUT /users/{id}/`: Update a specific user.
- `PATCH /users/{id}/`: Partially update a specific user.
- `DELETE /users/{id}/`: Delete a specific user.

## 📝 Fields

- `id`: The unique identifier of the user. This field is read-only.
- `username`: The username of the user.
- `password`: The password of the user. This field is write-only and the input type is password.

## 🔐 Permissions

- `UpdateUserPermission`: Custom permission class that only allows users to edit their own profile.

## 🔑 Authentication

- `TokenAuthentication`: Token-based authentication is used.

## 🛠️ Methods

- `create(validated_data)`: Create and validate a user. If the password is invalid, it raises a ValidationError.
- `update(instance, validated_data)`: Handle updating user account. If ‘password’ is in validated_data, it pops the password and sets it to the instance.

# 📃 User list API

- `GET /api/user/`: return a list of all users

# 📝 Create a User API

- `POST /api/user/`:
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```
PATCH /api/user/1/:
JSON
```json
{
    "password": "newsecurepassword123"
}
```
🔍 Search
You can search for users by their username using the search parameter in the query string. For example, /api/user/?search=johndoe.

🎚️ Filter
Backend filter

🔒 User Login Api
Create User auth token API

Endpoint
/api/auth/login/: Obtain a token for a user.
POST /api/auth/login/:
JSON
```json
{
    "token": "2b6edab8ae1f60a32c98048e8cd50b47ba93e557"
}
```

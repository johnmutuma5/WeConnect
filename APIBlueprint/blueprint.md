FORMAT: 1A
HOST: http://weconnect-api-heroku.herokuapp.com

# WeConnect
WeConnect provides a platform that brings businesses and individuals together.
This platform creates awareness for businesses and gives the users the
ability to write reviews about the businesses they have interacted with.

# Group User

## User Registration [/api/v2/auth/register]
All requests sent by client to register new user accounts are handled by
this resource. Receives data in `json` format and it should check that
all the required fields are supplied.

### Register a user [POST]

+ Request (application/json)

  + Attributes (User Data)


+ Response 201 (application/json)
    The client recievies a success message on registration

  + Attributes
      - msg: SUCCESS: user john_doe created! (string) - The success response message

+ Response 409 (application/json)
    The client receives an error message on sending a registration request with data that contains an unavailable username

  + Attributes
      - msg: Username already exists (string) - The error message that a client gets for trying to register with an existing username


+ Response 422 (application/json)
    The client receives an error message for invalid entries into the request data.
    Invalid username: `Invalid username!`
    Invalid email: `Invalid email!`
    Invalid mobile: `Invalid mobile!`
    Invalid password: `Password too short`


  + Attributes
      - msg: Invalid username! (string) - The error message that the client gets for sending invalid data e.g. username, email, mobile


## Users login [/api/v2/auth/login]
This resource handles all client login requests. The API receives data in
`json` format and logs in the user after verifying the credentials.

### Login a user [POST]

+ Request

  + Attributes
      - username: john_doe (string, required) - A registered username
      - password: userspassword (string, required) - The user's password

+ Response 200 (application/json)
  For successful login

  + Attributes
      - msg: Logged in john_doe (string) - The success message for login

+ Response 401 (application/json)
  For unsuccessful login due to invalid credentials. e.g. a wrong `password`

  + Attributes
      - msg: Invalid username or password (string) - The error message
              the client gets on supplying invalid credentials


## Logout [/api/v2/auth/logout]
Handles logout requests

### Logout user [POST]

+ Request

  + Headers

      Authorization: Bearer valid.jwttoken.string


+ Response 200 (application/json)

  + Attributes
      - msg: Logged out successfully! (string) - Successful logout message

## User Profile [/api/v2/auth/personal-profile]
Users can get their private profile data. This resource requires login.

### Get user profile [GET]

+ Request

  + Headers

      Authorization: Bearer valid.jwttoken.string

+ Response

  + Attributes
      - Include Private Profile


## Resetting passwords [/api/v2/auth/reset-password]
Handles users' requests to change a password. A link with a verification token should be sent to their registered email address to enable changing password

### Reset a user password [POST]

+ Response 201 (application/json)
  Includes a message for successful password reset

  + Attributes
      - msg: Password updated successfully (string) - The success message for updating passwords


+ Response 401 (application/json)
  Includes a message for sending a password reset request without a username

  + Attributes
      - msg: No username (string) - The error message for not supplying a username in the request


+ Response 404 (application/json)
  Includes an error message for supplying an unknown username

  + Attributes
      - msg: Username is unknown (string) - The error message for supplying an unrecognized username in the request


+ Response 422 (application/json)
  Includes an error message for sending a request with an invalid password reset token

  + Attributes
      - msg: Invalid Token (string) - The error message for unrecognized password reset token


# Group Business

## Businesses Resource [/api/v2/businesses]
Resource for registering businesses and getting information for all businesses stored

### Register a business [POST]
This action registers businesses.

+ Request (application/json)
  Includes data for the business to be registered

  + Attributes (Business Registration Info)


+ Response 201 (application/json)
  Includes message for successful registration of business

  + Attributes
      - msg: SUCCESS: business Andela Kenya created! (string) - The message
                for successful business registration.

+ Response 401 (application/json)
  Includes a message for business registration failure as a result of trying to register a business while not logged in.

  + Attributes
      - Include Login Required

+ Response 409 (application/json)
  Includes a message for business registration failure as a result of trying to register a business with an unavailable business name.

  + Attributes
      - Include Business Name Duplication Error


### Get all business' information [GET]
This action gets information for all businesses stored

+ Response 200 (application/json)
  A list of key value pairs for each business's information

  + Attributes (array[Business Info])


## One Business Resource [/api/v2/businesses/{id}]
Resource related to a specific businesses referenced by its `id`

+ Parameters
  - id: 1 (integer, required) - The id of the business as an integer

### Get a single business's info [GET]
This action sends a request to retrieve information of a single business.
It include a URI parameter representing the `id` of the business

+ Response 200 (application/json)
Includes information of a business referenced by `id` mapping to the business's `id`

  + Attributes (Business Info)


+ Response 404 (application/json)
  Includes an error message when a business with the supplied `id` does not exist

  + Attributes
      - Include Business Not Found Error

### Edit business info [PUT]
This action sends a request to edit the information stored about a business.
The targeted business business is referenced by referenced by a URI parameter representing the `id` of the business.

+ Request (application/json)

  + Attributes
      - name: New Name (string, optional) - The new name of the business
      - owner: Alice Doe (string, optional) - The new owner of the business
      - location: Marurui, Off Northern Bypass Rd (string, optional) - The new location of the business
      - mobile: 254700001001 (string, optional) - The new contact number of the business

+ Response 201 (application/json)
  Includes a message for successful business edit operation

  + Attributes
      - msg: Changes recorded successfully (string) - The success message of updating business information


+ Response 401 (application/json)
  Includes a message for business edit failure as a result of trying to edit a business while not logged in.

  + Attributes
      - Include Login Required


+ Response 403 (application/json)
  Includes an error message for forbidden request to edit a business that is registered to another user

  + Attributes
      - Include Forbidden Business Operation Error


+ Response 404 (application/json)
  Includes an error message when a business with the supplied `id` does not exist

  + Attributes
      - Include Business Not Found Error


+ Response 409 (application/json)
  Includes an integrity error message for supplying a business name that is already registered in the API

  + Attributes
      - Include Business Name Duplication Error


### Delete business [DELETE]
This action sends a request to delete a business from the API.

+ Response 201 (application/json)
  Includes a successful delete business operation message

  + Attributes
      - msg: SUCCESS: Business deleted (string) - The business deletion success message

+ Response 403 (application/json)
  Includes an error message for a forbidden request to delete a business registered to another user

  + Attributes
      - Include Forbidden Business Operation Error

+ Response 404 (application/json)
  Includes an error message for trying to delete a business using an `id` that is not recognized

  + Attributes
      - Include Business Not Found Error



## Business Reviews [/businesses/{business_id}/reviews]
This resource handles getting and posting reviews of a business

+ Parameters
    - business_id: 1 (integer) - The id of the business to review

### Review a business [POST]
This action handles posting a review for a business

+ Request (application/json)
  Includes the heading and body of a review

    + Attributes
        - Include Review From User

+ Response 201 (application/json)
  Includes a message for a successful review of a business

    + Attributes
        - msg: SUCCESS: review heading:[Wonderful] created! (string) - The success message for a successful review

+ Response 401 (application/json)
  Includes a message for an unsuccessful review. This is when a user sends a request without login in

    + Attributes
        - Include Login Required


### Get Reviews of a business [GET]
This action handles getting all the reviews of a business

+ Response 200 (application/json)
  Includes a list of all reviews of a business

    + Attributes (array[Full Review Info])

+ Response 404 (application/json)
  Includes an error message for trying to retrieve reviews with an unrecognized business `id`

    + Attributes
          - Include Business Not Found Error




## Data Structures
### User Data
+ first_name: John (string, required) - The first name of the users
+ last_name: Doe (string, required) - The last name of the users
+ gender: Male, Female (enum, required) - The gender name of the users
+ mobile: 254720000000
+ email: johndoe@gmail.com
+ username: john_doe
+ password: pass

### Private Profile
- Include User Data
- businesses(array[Key Business Identity])
- reviews(array[Key Review Identity])


### Key Business Identity
- name: Andela Kenya (string, required) - The name of the business
- id: 1000 (number) - The formatted `id` of the business.


### Business Registration Info
- name: Andela Kenya (string, required) - The name of the business
- owner: Alice Doe (string, optional) - The owner of the business
- location: TRM, Thika Road (string, required) - The location of the business
- mobile: 2547000200 (string, required) - The contact of the business
- category: textile (string, required) - The sector of the business

### Business Info(Business Registration Info)
- id: 1000 (number) - The formatted `id` of the business.

### Key Review Identity
- heading: Wonderful (string) - The `heading` of the review
- id: 100 (number) - The `id` of the review

### Review From User
- heading: Wonderful (string) - The `heading` of the review
- body: Awesome products (string) - The `message` of the review

### Full Review Info(Review From User)
- author_id: 1000 (number) - The `id` of the reviewer
- business_id: 1000 (number) - The `id` of the business to review
- id: 100 (number) - The `id` of the review

### Business Name Duplication Error
- msg: Duplicate business name not allowed (string) - The error message for providing an taken business name

### Business Not Found Error
- msg: UNSUCCESSFUL: Could not find the requested information (string) - The error message for non-existent business `id`

### Forbidden Business Operation Error
- msg: UNSUCCESSFUL: The business is registered to another user (string) - The error message for trying to edit/delete a business registered to another user

### Login Required
- msg: You need to log in to perform this operation (string) - The error message for performing operations that require authentication while not logged in

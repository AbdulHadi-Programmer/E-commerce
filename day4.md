## Today on 17 October :
# I am Learning all types of Authentication in DRF

## Step 1: Authentication in Django Rest Framework 
`Let's dive in with practical examples, not theory.`

| Type                      | Description                                             | Use Case                                  |
| ------------------------- | ------------------------------------------------------- | ----------------------------------------- |
| **BasicAuthentication**   | Username/password for every request (encoded in base64) | Testing or private APIs                   |
| **SessionAuthentication** | Uses Django’s login session                             | For web-based apps (admin panel)          |
| **TokenAuthentication**   | Each user gets a token                                  | Used in mobile apps & APIs                |
| **JWT (JSON Web Token)**  | Token-based, more secure and scalable                   | Modern standard for APIs (we’ll use this) |
|                           |                                                         |                                           |

## Setup Simple JWT (most used in 2025)


## JWT has two type of tokens:
| Token Type        | Purpose                      | Validity                 | Use                                    |
| ----------------- | ---------------------------- | ------------------------ | -------------------------------------- |
| **Access Token**  | Used for actual requests     | short-lived (e.g. 5 min) | Sent in `Authorization` header         |
| **Refresh Token** | Used to get new access token | long-lived (e.g. 1 day)  | Stored securely, used to refresh login |

## Add Token Blacklist:
# What is Blacklist Token 
To make logout secure :
- When a user logs out, their refresh token wil be blacklisted.
- Prevents reuse of refresh tokens after logout 
- Real-World feature —— highly recommended before custom users.

## What are Permission Classes ?
They tells Django who is allowed to access a resource.

| Permission Class         | Meaning                                                  |
| ------------------------ | -------------------------------------------------------- |
| `AllowAny`               | Anyone (no login required).                              |
| `IsAuthenticated`        | Only logged-in users can access.                         |
| `IsAdminUser`            | Only admins/superusers.                                  |
| `DjangoModelPermissions` | Based on Django’s `add`, `change`, `delete` permissions. |

## What is token_blacklist ?
That's not an authentication class. 
It's a Django App (a feature of SimpleJWT) used to blacklist/expire tokens when a user logs out. 
You should not put 'token_blacklist' in the authentication list -- it breaks things.

## How to login with credential and get JWT tokens ?
Method: **POST**
link: localhost:8000/api/token
body: 
```json
{
    "username" : "hadi",
    "password": "1233"
}
```
and then `Username, Access Token, Refresh Token we get` 

Remember that we can only use Authenticated Api using `Access Token` and it is expire in 5 minutes by default we can change it expiration time and also when it is expired we can use `Refresh Token` to regenerate new `Access Token`

like this :
**POST** method
link: localhost:8000/api/token/refresh/
body:
```json
{
    "refresh": ".............................."
}
```
then output: 
```

In Simple word :
#### Token Refresh Endpoint (Auto Renew Access Token)

Why: Access tokens expire fast (usually 5 – 15 min). The frontend can request a new access token using the refresh token — so the user doesn’t need to log in again.

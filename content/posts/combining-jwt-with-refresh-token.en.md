---
date: "2018-12-13T13:07:00+00:00"
title: "User Authentication Practice Based on JWT + Refresh Token"
categories:
  - Tech
---

![](/images/20181213_01.jpg)

HTTP is a stateless protocol, meaning once a request is completed, the server doesn't know who sent the next request (the same IP doesn't represent the same user). In web applications, user authentication and authorization are crucial, and there are multiple practical solutions, each with its own merits.

<!-- more -->

### Session-Based Session Management

In the early development of web applications, most adopted session-based session management, which works as follows:

- The client authenticates using a username and password.
- The server generates and stores a session, returning the SessionID to the client via a cookie.
- When accessing an authenticated endpoint, the client includes the SessionID in the cookie.
- The server looks up the session using the SessionID for authorization and returns the necessary data to the client.

![](/images/20181213_02.jpg)

Session-based methods have several issues:

- The server needs to store sessions, which are often stored in memory or in-memory databases for quick access, consuming significant server resources when many users are online.
- When scaling, the server that creates the session might not be the one validating it, necessitating separate storage and sharing of all sessions.
- Since the client uses cookies to store the SessionID, cross-domain compatibility is required, and it's challenging to prevent CSRF attacks.

### Token-Based Session Management

Due to the drawbacks of session-based management, stateless token-based session management emerged. Stateless means the server no longer stores information, not even sessions. The logic is as follows:

- The client authenticates using a username and password.
- The server verifies the credentials and generates a token to return to the client.
- The client saves the token and includes it in the URL parameters or HTTP header when accessing authenticated endpoints.
- The server decodes the token for authorization and returns the necessary data to the client.

![](/images/20181213_03.jpg)

Token-based session management effectively addresses the issues of session-based management:

- The server doesn't need to store authentication-related information; it's encrypted in the token, and the server only reads the authorization info from the token.
- It avoids the scalability issues caused by shared sessions.
- It doesn't rely on cookies, effectively preventing CSRF attacks.
- CORS can quickly resolve cross-domain issues.

### Introduction to JWT

JWT stands for JSON Web Token. It doesn't define any technical implementation but outlines a rule for token-based session management, including the standard content a token should have and its generation process.

A JWT token looks like this:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NDQ1MTE3NDMsImp0aSI6IjYxYmVmNjkyLTE4M2ItNGYxYy1hZjE1LWUwMDM0MTczNzkxOSJ9.CZzB2-JI1oPRFxNMaoFz9-9cKGTYVXkOC2INMoEYNNA
```

It's composed of three parts: `A.B.C`, representing the Header, Payload, and Signature. The Header and Payload are in JSON format, which is the JSON in JWT. Each part is Base64 encoded and joined with `.` to form a JWT token.

The JWT Header stores the encryption algorithm and token type used.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

The Payload contains the data. JWT specifies some fields and recommends their use, but developers can define their own fields and content, like the following:

```json
{
  "username": "yage",
  "email": "sa@simpleapples.com",
  "role": "user",
  "exp": 1544602234
}
```

Note that the Payload is only Base64 encoded and is essentially stored in plaintext for the client, so sensitive information should not be included.

The Signature part verifies whether the JWT token has been tampered with, using a Secret to encrypt the first two parts as follows:

```
HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
```

### Advantages & Issues of JWT

JWT inherits all the advantages of token-based session management, such as not relying on cookies, which helps prevent CSRF attacks and allows it to function in browsers with cookies disabled.

The main advantage of JWT is that the server no longer needs to store sessions, making it easy to scale the server's authentication and authorization services without introducing components like Redis, reducing system complexity. However, this is also JWT's biggest drawback. Since the validity period is stored in the token, once issued, a JWT token remains valid until expiration and cannot be revoked server-side. When a user logs out, the client must delete the locally stored JWT token. If user deactivation is needed, JWT alone cannot achieve this.

### JWT Practice

Despite JWT's issues and inability to meet some business needs, we can still make improvements in practice to create a balanced solution. After all, there's no silver bullet in user session management.

The tokens discussed earlier are Access Tokens, needed for accessing resource endpoints. There's another type, the Refresh Token, which usually has a longer validity period, while the Access Token has a shorter one. When the Access Token expires, the Refresh Token can be used to obtain a new Access Token. If the Refresh Token also expires, the user must log in again.

In JWT practice, introducing a Refresh Token modifies the session management process as follows:

- The client authenticates using a username and password.
- The server generates a short-lived Access Token (e.g., 10 minutes) and a long-lived Refresh Token (e.g., 7 days).
- The client includes the Access Token when accessing authenticated endpoints.
- If the Access Token hasn't expired, the server authorizes and returns the necessary data to the client.
- If authorization fails (e.g., a 401 error) when accessing an authenticated endpoint with the Access Token, the client uses the Refresh Token to request a new Access Token.
- If the Refresh Token hasn't expired, the server issues a new Access Token to the client.
- The client uses the new Access Token to access authenticated endpoints.

![](/images/20181213_04.jpg)

Store the generated Refresh Token and its expiration in the server's database. Since the Refresh Token isn't validated during business endpoint requests, only when requesting a new Access Token, storing it in the database doesn't impact business endpoint response times and doesn't need to be kept in memory like sessions to handle many requests.

This architecture provides a way for the server to disable user tokens. When a user needs to log out or be deactivated, simply disable or delete the server's Refresh Token. The user won't be able to access authenticated endpoints after the Access Token expires, as they can't obtain a new Access Token. Although there's a window period (depending on the Access Token's expiration), combining this with the client deleting the Access Token upon logout generally meets the precision requirements for user authentication and authorization.

### Summary

Using JWT enhances the efficiency of developing user authentication and authorization features, reduces system complexity, and avoids numerous database and cache queries, lowering business endpoint response delays. However, these advantages also increase the difficulty of token management. By introducing a Refresh Token, we can continue to leverage JWT's benefits while ensuring token management precision meets business needs.
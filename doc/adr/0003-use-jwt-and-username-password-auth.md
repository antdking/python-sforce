# 3. Use JWT and Username-Password Auth

Date: 2019-10-25

## Status

Accepted

## Context

To make setup easier for users of this library, we should setup some reference clients so
developers can get started quicker.

For background applications, the 2 most common flows used will be Username/Password, and JWT Bearer Tokens flows.
They facilitate offline access, and are easy to setup for Admins.

## Decision

Use Authlib to implement the Password flow using a standard `Oauth2Session` with `username` + `password`.
Use Authlib to implement the JWT flow, using the `AssertionSession` + an X509 key.

## Consequences

Implementing multiple flows will require us to make the client/session pluggable. This is good design practice,
but will result in a slightly more complex design.

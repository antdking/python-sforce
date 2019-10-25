# 2. Use Authlib as a Client

Date: 2019-10-25

## Status

Accepted

## Context

Salesforce supports a few different ways of handling authentication.
This is something I care not for dealing with.

Authlib covers all of these authentication methods. While we may only include a few
fully built client backends in this library, we shouldn't put a barrier up for people who
wish to use different Auth Flows.

## Decision

Use [Authlib][authlib] to provide authentication for the API client.
This removes the overhead of building auth flows, such as refreshing tokens.

## Consequences

While it's a well-structured library, and covers all our usecases, there are a few of issues.

- The docs aren't the greatest on the stable branch;
  - It's not always clear how to link different flows with the client.
- It provides it's own Session implementation
  That being said, it **does** adhere to the `requests` Session (inheritance is used), and custom code is kept
  away, **and** `requests` has a stable model at this point, some may want just Auth, and not refresh capabilities.
  Not really an issue for us however.
- No async support

All of these concerns are actually addressed in the upcoming update, with better docs that align with the RFCs more,
Async support in the form of `httpx` integrations, as well as cleaner distinctions between `auth` and `session`
implementations, especially in the `Assertion` flows (used for Salesforce JWT Auth).

[authlib]: https://docs.authlib.org/en/stable/#

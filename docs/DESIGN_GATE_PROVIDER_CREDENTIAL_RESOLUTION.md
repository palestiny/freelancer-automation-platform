# Design Gate — Provider Credential Resolution Boundary

**Status:** APPROVED — V1 application/infrastructure boundary only.

## Purpose

Resolve an opaque provider credential reference into provider-usable authentication material without exposing secret material to the domain.

## V1 Contract

The application boundary may request:

**provider key + credential reference → resolved credential handle/material**

The domain only carries the opaque credential reference.

The resolver:
- is an application/infrastructure port;
- is provider-independent at the port level;
- returns an explicit resolution result or failure;
- never persists secrets in domain objects;
- never logs secret material;
- never chooses credentials by ranking or fallback;
- never authorizes an action;
- never executes a provider call.

## Safety Rules

1. Credential references are identifiers, not secrets.
2. Secret material never crosses into domain entities/value objects.
3. Resolution failure is explicit and must not silently fall back to another credential.
4. Provider key and credential reference must remain bound.
5. Credential resolution does not imply authorization.
6. Credential resolution does not imply provider capability support.
7. Credential resolution does not invoke the provider.
8. Concrete secret stores remain replaceable infrastructure adapters.
9. Secret lifecycle operations such as rotation and refresh remain infrastructure concerns.
10. Tests must use fake/non-secret credential material only.

## Trade-offs

- **Resolver returns secret material:** simple adapter contract, but larger secret exposure surface.
- **Resolver returns an opaque provider credential handle:** safer domain boundary, but provider adapters still need a secure handoff mechanism.
- **Embed credentials in provider adapters:** reduces central abstraction, but duplicates credential concerns across adapters.

V1 chooses an explicit resolver port with an opaque reference and provider-bound resolution. Concrete secret storage is deferred until a real provider integration requires it.

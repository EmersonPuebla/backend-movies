# Autenticación con Amazon Cognito (backend)

`backend-movies` es una API REST con FastAPI. La autenticación se apoya en un **user pool** de
Amazon Cognito, que actúa como proveedor de identidad (OIDC) y emite los JWT que protegen la API.

## Flujo

1. El frontend (SPA de Astro) autentica al usuario contra el user pool y obtiene un **access token**.
2. El frontend llama a la API enviando `Authorization: Bearer <access_token>`.
3. El backend **verifica el JWT** antes de ejecutar el endpoint.

> Para autorizar usa el **access token**. El ID token sirve para conocer *quién* es el usuario,
> no para proteger recursos.

## Variables de entorno

| Variable | Descripción |
| --- | --- |
| `COGNITO_USER_POOL_ID` | ID del user pool (ej. `us-east-1_AbCdEfGhI`) |
| `COGNITO_CLIENT_ID` | ID del app client (público para la SPA) |
| `COGNITO_REGION` | Región de AWS (ej. `us-east-1`) |

## Verificar el token

Usa [`PyJWT`](https://pyjwt.readthedocs.io/) con `PyJWKClient` para validar el token contra el
JWKS del pool (el paquete `aws-jwt-verify` es solo de Node.js):

```python
import jwt
from jwt import PyJWKClient

jwks = PyJWKClient(f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json")

signing_key = jwks.get_signing_key_from_jwt(token)
claims = jwt.decode(
    token,
    signing_key.key,
    algorithms=["RS256"],
    issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
    options={"verify_aud": False},
)
assert claims["token_use"] == "access"
assert claims["client_id"] == client_id
```

Se validan: firma (RS256), `iss` (`https://cognito-idp.{region}.amazonaws.com/{pool_id}`),
`client_id`, `token_use=access` y `exp`. En FastAPI esto está encapsulado en la dependencia
`require_auth` de `src/backend_movies/auth.py`.

## Crear el user pool y el app client

```bash
# User pool con sign-in por email
aws cognito-idp create-user-pool \
  --pool-name movies-users \
  --auto-verified-attributes email \
  --username-attributes email \
  --policies '{"PasswordPolicy":{"MinimumLength":8,"RequireUppercase":true,"RequireLowercase":true,"RequireNumbers":true,"RequireSymbols":false}}'

# App client público (SPA, sin secret)
aws cognito-idp create-user-pool-client \
  --user-pool-id <pool-id> \
  --client-name web-spa \
  --no-generate-secret \
  --explicit-auth-flows ALLOW_USER_SRP_AUTH
```

## Endpoints protegidos

Todos los endpoints de `/movies` deben exigir autenticación. El access token se envía en la
cabecera `Authorization` y se valida en una dependencia de FastAPI compartida.

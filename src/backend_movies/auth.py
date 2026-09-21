import os

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

REGION = os.environ.get("COGNITO_REGION")
USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID")

if not (REGION and USER_POOL_ID and CLIENT_ID):
    raise RuntimeError(
        "Faltan variables de entorno de Cognito: COGNITO_REGION, COGNITO_USER_POOL_ID y COGNITO_CLIENT_ID."
    )

ISSUER = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}"
JWKS_URL = f"{ISSUER}/.well-known/jwks.json"

_jwks_client = PyJWKClient(JWKS_URL)
_bearer = HTTPBearer(auto_error=False)


def _verify_token(token: str) -> dict:
    signing_key = _jwks_client.get_signing_key_from_jwt(token)
    claims = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=ISSUER,
        options={"verify_aud": False},
    )
    if claims.get("token_use") != "access":
        raise ValueError("token_use inválido")
    if claims.get("client_id") != CLIENT_ID:
        raise ValueError("client_id inválido")
    return claims


def require_auth(credentials: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
    try:
        return _verify_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

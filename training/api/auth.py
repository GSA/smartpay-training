
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from training.config import settings
from urllib import request
import json


class JWTUser(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            user = self.decode_jwt(credentials.credentials)
            if user is None:
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            return user
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def decode_jwt(self, token: str):
        token_header = jwt.get_unverified_header(token)
        key_id = token_header.get("kid")

        # Determine if the token is loginless or from an authentication service
        if key_id is None:
            # Loginless token
            return self.decode_loginless_jwt(token)
        else:
            # Authentication token
            return self.decode_auth_jwt(token, key_id)

    def decode_loginless_jwt(self, token: str):
        try:
            return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except InvalidTokenError:
            return

    def decode_auth_jwt(self, token: str, key_id: str):
        jwk = self.get_jwks().get(key_id)
        if jwk is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unrecognized token."
            )
        try:
            return jwt.decode(
                token,
                jwk.get("key"),
                algorithms=[jwk.get("alg")],
                audience="test_client_id"
            )
        except InvalidTokenError:
            return

    def get_jwks(self):
        # Get a list of JSON Web Keys from the OIDC server.

        # This is something we would normally want to cache but in this case,
        # since we're using cloud.gov UAA, their server specifies no caching:
        # "Cache-Control: no-cache, no-store, max-age=0, must-revalidate".
        # If in the future the OIDC server requests that we cache the keys,
        # then we should implement a cache here.

        jwks_endpoint = self.discover_jwks_endpoint()

        with request.urlopen(jwks_endpoint) as res:
            jwks = json.load(res)

        if jwks.get("keys") is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to get required data from authentication server (public keys)."
            )

        keys = {}
        for jwk in jwks.get("keys"):
            kid = jwk.get("kid")
            alg = jwk.get("alg")
            algorithm = jwt.get_algorithm_by_name(alg)
            key = algorithm.from_jwk(jwk)
            keys[kid] = {
                "key": key,
                "alg": alg
            }

        return keys

    def discover_jwks_endpoint(self) -> str:
        # Use the OIDC Discovery endpoint to get the location of the JSON Web
        # Key Set (JWKS) data.

        url_components = [settings.AUTH_AUTHORITY_URL, "/.well-known/openid-configuration"]
        config_endpoint = '/'.join(s.strip('/') for s in url_components)

        with request.urlopen(config_endpoint) as res:
            data = json.load(res)
            jwks_endpoint_uri = data.get("jwks_uri")

        if jwks_endpoint_uri is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to get required data from authentication server (JWKS URI)."
            )

        return jwks_endpoint_uri

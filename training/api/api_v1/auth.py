import json
from typing import Annotated
from urllib.request import urlopen

from fastapi import Request, HTTPException, Depends, status
from fastapi import Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from training.config import settings


class JWTUser(HTTPBearer):
    '''
    Represents a JWT issued by our API.
    This class can be used as a dependency in FastAPI routes like:

    @router.get("/somepath", response_model=SomeModel)
    def my_function( user: dict[str, Any] = Depends(JWTUser())):

    to generate a user with a valid token.

    '''

    async def __call__(self, request: Request):
        # The parent HTTPBearer default's to raising an error if there is
        # no authentication or the authentication schema is not bearer
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)

        user = self.decode_jwt(credentials.credentials)
        if user is None:
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        return user

    def decode_jwt(self, token: str):
        try:
            return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except InvalidTokenError:
            return


class UAAJWTUser(HTTPBearer):
    '''
    Represents a JWT issued by an OAuth server.
    Used as part of the Admin SecureAuth flow
    '''

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        user = self.decode_jwt(credentials.credentials)
        if user is None:
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        return user

    def decode_jwt(self, token: str):
        token_header = jwt.get_unverified_header(token)
        key_id = token_header.get("kid")
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
                audience=settings.AUTH_CLIENT_ID
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

        with urlopen(jwks_endpoint) as res:
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

        with urlopen(config_endpoint) as res:
            data = json.load(res)
            jwks_endpoint_uri = data.get("jwks_uri")

        if jwks_endpoint_uri is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to get required data from authentication server (JWKS URI)."
            )

        return jwks_endpoint_uri


class RequireRole:
    '''
    Used for api routes that should be limited to specific roles. These
    roles will be encoded in the JWT when the user authenticates. This
    checkes the roles in the JWT and compares them to the roles this
    class was initialized with. It can be used like this to ensure we
    either have a user with the `Admin` role or response with a 401:

    @router.post("/some_route", response_model=SomeModel
    def create_user(user=Depends(RequireRole(["Admin"]))):
    '''
    def __init__(self, required_roles: list[str]) -> None:
        self.required_roles = set(required_roles)

    def __call__(self, user=Depends(JWTUser())):
        try:
            user_roles = user['roles']
        except KeyError:
            raise HTTPException(status_code=401, detail="Not Authorized")

        if all(role in user_roles for role in self.required_roles):
            return user
        else:
            raise HTTPException(status_code=401, detail="Not Authorized")


def user_from_form(jwtToken: Annotated[str, Form()]):
    '''
    This allows POST requests to send a token as part of form-encoded request.
    There are places in the front-end where we want to download a file, but we also
    need to authenticate the user. We cannot pass a JWT with a simple html <a>, so instead
    use a form to POST the request. The form can then include the JWT as in input. This
    function is used to decode and validate the JWT in that case. See: "/certificate/{certType}/{id}"
    for an example.
    '''
    try:
        return jwt.decode(jwtToken, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not Authorized")

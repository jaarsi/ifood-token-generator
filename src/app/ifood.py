from typing import Callable, TypeAlias, TypedDict
import requests as rq
import settings


class UserCodeResponse(TypedDict):
    userCode: str
    authorizationCodeVerifier: str
    verificationUrl: str
    verificationUrlComplete: str
    expiresIn: int


class TokenResponse(TypedDict):
    accessToken: str
    type: str
    expiresIn: int


class MerchantResponse(TypedDict):
    id: str
    name: str
    corporateName: str


AuthorizerFunction: TypeAlias = Callable[[str], TokenResponse]


def get_merchants(token: TokenResponse) -> list[MerchantResponse]:
    response = rq.get(
        "https://merchant-api.ifood.com.br/merchant/v1.0/merchants",
        headers={"Authorization": f"Bearer {token['accessToken']}"},
    )
    response.raise_for_status()
    return response.json()


def request_usercode() -> tuple[UserCodeResponse, AuthorizerFunction]:
    response = rq.post(
        "https://merchant-api.ifood.com.br/authentication/v1.0/oauth/userCode",
        data={"clientId": settings.CLIENT_ID},
    )
    response.raise_for_status()
    usercode: UserCodeResponse = response.json()

    def get_token(authorization_code: str) -> TokenResponse:
        response = rq.post(
            "https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token",
            data={
                "grantType": "authorization_code",
                "clientId": settings.CLIENT_ID,
                "clientSecret": settings.CLIENT_SECRET,
                "authorizationCode": authorization_code,
                "authorizationCodeVerifier": usercode["authorizationCodeVerifier"],
            },
        )
        response.raise_for_status()
        return response.json()

    return usercode, get_token

from hypothesis import given

from mythx_models.response import AuthLoginResponse

from .strategies.auth import auth_refresh_response


@given(auth_refresh_response())
def test_serde(response):
    obj = AuthLoginResponse(**response)
    assert obj.dict(by_alias=True) == {
        "access": response["access"],
        "refresh": response["refresh"],
    }

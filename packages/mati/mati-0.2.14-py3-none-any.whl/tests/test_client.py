import pytest
from requests.exceptions import HTTPError

from mati import Client


@pytest.mark.vcr
@pytest.mark.parametrize('score', [None, 'identity'])
def test_client_renew_access_token(score):
    client = Client('api_key', 'secret_key')
    assert client.bearer_tokens.get(score) is None
    client.get_valid_bearer_token(score)
    assert not client.bearer_tokens[score].expired
    assert client.bearer_tokens[score] == client.get_valid_bearer_token(score)


@pytest.mark.vcr
def test_failed_auth():
    client = Client('wrong', 'creds')
    with pytest.raises(HTTPError) as exc_info:
        client.access_tokens.create()
    assert exc_info.value.response.status_code == 401

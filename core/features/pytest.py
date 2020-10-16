def assert_is_request(request, status_code: int = 200):
    assert status_code == request.status_code

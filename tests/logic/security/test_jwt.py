from app.logic.logic import Logic


async def test_encode(token: str):
    assert token is not None


async def test_decode(logic: Logic, token: str):
    data = logic.security.jwt.decode_token(token)
    assert data is not None

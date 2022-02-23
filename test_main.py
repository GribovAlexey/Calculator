from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_calc():
    for expr, result in (
            ('1+2', 2.999),
            # ('1*3*3', 9),
    ):
        response = client.post(
            "/calc/",
            json={"expression": expr}
        )
        assert response.status_code == 200
        assert response.json() == result


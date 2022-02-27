from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_calc_correct_input():
    for expr, result in (
            ('1+2', 3),
            ('1*3*3', 9),
    ):
        response = client.post(
            "/calc/",
            json={"expression": expr}
        )
        assert response.status_code == 200
        assert response.json() == result


def test_calc_signs_in_a_row_error():
    response = client.post("/calc/", json={"expression": "++1+3"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid data: " \
                                        "Signs in a row errors: ++."


def test_calc_tabs_between_digits_error():
    response = client.post("/calc/", json={"expression": "1  2 + 3"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid data: " \
                                        "Spaces between digits errors: 1  2."


def test_calc_bad_first_sign_error():
    response = client.post("/calc/", json={"expression": "*1-2"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid data: " \
                                        "Started with unacceptable " \
                                        "sign error: *."


def test_calc_last_sign_error():
    response = client.post("/calc/", json={"expression": "1-2-"})
    assert response.status_code == 422
    assert response.json()[
               "detail"] == "Invalid data: Ended with sign error: -."


def test_calc_unacceptable_symbols():
    response = client.post("/calc/", json={"expression": "1+3-a2"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid data: " \
                                        "Contains unacceptable symbols"


def test_calc_inconsistent_brackets_error():
    response = client.post("/calc/", json={"expression": "(1-3*(1+2)"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid data: Brackets inconsistency"

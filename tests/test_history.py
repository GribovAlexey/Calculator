from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_history_get_history_without_aruments():
    client.post("/calc/", json={"expression": "5+2"})
    client.post("/calc/", json={"expression": "1-7"})
    response = client.get("/history/")
    assert response.status_code == 200
    expected = [
        {
            "request": "1-7",
            "response": -6,
            "status": "success"
        },
        {
            "request": "5+2",
            "response": 7,
            "status": "success"
        }
    ]
    assert response.json() == expected


def test_history_get_history_with_limit():
    client.post("/calc/", json={"expression": "(1+2)-3*4"})
    response = client.get("/history/?limit=2")
    assert response.status_code == 200
    expected = [
        {
            "request": "(1+2)-3*4",
            "response": -9,
            "status": "success"
        },
        {
            "request": "1-7",
            "response": -6,
            "status": "success"
        }
    ]
    assert response.json() == expected


def test_history_get_history_with_status_success():
    client.post("/calc/", json={"expression": "12-3-"})
    response = client.get("/history/?status=success")
    assert response.status_code == 200
    expected = [
        {
            "request": "(1+2)-3*4",
            "response": -9,
            "status": "success"
        },
        {
            "request": "1-7",
            "response": -6,
            "status": "success"
        },
        {
            "request": "5+2",
            "response": 7,
            "status": "success"
        }
    ]
    assert response.json() == expected


def test_history_get_history_with_status_fail():
    response = client.get("/history/?status=fail")
    assert response.status_code == 200
    expected = [
        {
            "request": "12-3-",
            "response": [
                "Ended with sign error: -."
            ],
            "status": "fail"
        }
    ]
    assert response.json() == expected


def test_history_get_history_with_limit_and_status_success():
    client.post("/calc/", json={"expression": "7*3*"})
    response = client.get("/history/?limit=2&status=success")
    assert response.status_code == 200
    expected = [
        {
            "request": "(1+2)-3*4",
            "response": -9,
            "status": "success"
        },
        {
            "request": "1-7",
            "response": -6,
            "status": "success"
        }
    ]
    assert response.json() == expected


def test_history_get_history_with_limit_and_status_fail():
    response = client.get("/history/?limit=2&status=fail")
    assert response.status_code == 200
    expected = [
        {
            "request": "7*3*",
            "response": [
                "Ended with sign error: *."
            ],
            "status": "fail"
        },
        {
            "request": "12-3-",
            "response": [
                "Ended with sign error: -."
            ],
            "status": "fail"
        }
    ]

    assert response.json() == expected


def test_history_get_history_status_error():
    response = client.get("/history/?status=mistake")
    assert response.status_code == 422
    expected = "Invalid attributes: Status error. Wrong status: mistake"
    assert response.json()["detail"] == expected


def test_history_get_history_limit_error():
    response = client.get("/history/?limit=-2")
    assert response.status_code == 422
    expected = "Invalid attributes: History length error. Wrong length: -2"
    assert response.json()["detail"] == expected

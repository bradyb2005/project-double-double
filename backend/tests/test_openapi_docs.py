from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def operations():
    schema = client.get("/openapi.json").json()
    for path, methods in schema["paths"].items():
        for method, op in methods.items():
            yield method.upper(), path, op

def test_openapi_schema_is_served():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Project Double Double API"

def test_every_endpoint_has_summary_description_and_tag():
    for method, path, op in operations():
        assert op.get("summary"), f"{method} {path} has no summary"
        assert op.get("description"), f"{method} {path} has no description"
        assert op.get("tags"), f"{method} {path} has no tag"

def test_every_endpoint_has_a_response_model():
    for method, path, op in operations():
        success = next(code for code in op["responses"] if code.startswith("2"))
        schema = op["responses"][success]["content"]["application/json"]["schema"]
        assert schema, f"{method} {path} has an empty response schema"

def test_error_responses_are_documented():
    expected = {
        ("GET", "/restaurants/{id}"): "404",
        ("GET", "/restaurants/{restaurant_id}/menu"): "404",
        ("POST", "/restaurants"): "400",
        ("POST", "/restaurants/{restaurant_id}/menu"): "400",
        ("PUT", "/restaurants/{restaurant_id}/menu/{item_id}"): "400",
        ("PUT", "/restaurants/update/{restaurant_id}"): "404",
    }
    documented = {(method, path): op for method, path, op in operations()}
    for key, status_code in expected.items():
        assert status_code in documented[key]["responses"], f"{key} does not document {status_code}"

def test_documented_status_codes_match_behaviour():
    assert client.get("/restaurants/9999").status_code == 404
    assert client.get("/restaurants/9999/menu").status_code == 404
    assert client.get("/restaurants/names").status_code == 200

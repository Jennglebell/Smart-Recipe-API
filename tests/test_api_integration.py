import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.recipe import Recipe, Ingredient

client = TestClient(app)

@pytest.fixture
def sample_recipe_data():
    return {
        "title": "Test Recipe",
        "description": "A test recipe description",
        "ingredients": [
            {
                "name": "Test Ingredient",
                "amount": 100,
                "unit": "g",
                "calories_per_unit": 1.5
            }
        ],
        "instructions": ["Step 1", "Step 2"],
        "prep_time": 10,
        "cook_time": 20,
        "servings": 4,
        "tags": ["test", "integration"]
    }

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_recipe(sample_recipe_data):
    response = client.post("/api/v1/recipes", json=sample_recipe_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_recipe_data["title"]
    assert "id" in data
    return data["id"]

def test_get_recipe(sample_recipe_data):
    create_response = client.post("/api/v1/recipes", json=sample_recipe_data)
    recipe_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_recipe_data["title"]

def test_search_recipes(sample_recipe_data):
    client.post("/api/v1/recipes", json=sample_recipe_data)
    
    response = client.get("/api/v1/recipes?query=Test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == sample_recipe_data["title"]

def test_search_by_tags(sample_recipe_data):
    client.post("/api/v1/recipes", json=sample_recipe_data)
    
    response = client.get("/api/v1/recipes?tags=test,integration")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "test" in data[0]["tags"]

def test_generate_meal_plan(sample_recipe_data):
    client.post("/api/v1/recipes", json=sample_recipe_data)
    
    response = client.get("/api/v1/meal-plan?days=1&calories_per_day=2000")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_invalid_recipe_creation():
    invalid_recipe = {
        "title": "",
        "description": "Test",
        "ingredients": [],
        "instructions": [],
        "prep_time": -1,
        "cook_time": 20,
        "servings": 4
    }
    response = client.post("/api/v1/recipes", json=invalid_recipe)
    assert response.status_code == 422

def test_recipe_not_found():
    response = client.get("/api/v1/recipes/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found" 
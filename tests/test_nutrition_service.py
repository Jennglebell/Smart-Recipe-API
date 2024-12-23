import pytest
from app.models.recipe import Recipe, Ingredient
from app.services.nutrition_service import NutritionService

@pytest.fixture
def nutrition_service():
    return NutritionService()

@pytest.fixture
def sample_ingredients():
    return [
        Ingredient(
            name="Chicken Breast",
            amount=200,
            unit="g",
            calories_per_unit=1.65
        ),
        Ingredient(
            name="Olive Oil",
            amount=15,
            unit="ml",
            calories_per_unit=8.2
        )
    ]

def test_calculate_recipe_calories(nutrition_service, sample_ingredients):
    total_calories = nutrition_service.calculate_calories(sample_ingredients)
    expected_calories = (200 * 1.65) + (15 * 8.2)
    assert abs(total_calories - expected_calories) < 0.01

def test_validate_recipe_nutrition(nutrition_service, sample_ingredients):
    is_healthy = nutrition_service.is_healthy_recipe(sample_ingredients)
    assert is_healthy == True
import pytest
from app.models.recipe import Recipe, Ingredient
from app.services.recipe_service import RecipeService

@pytest.fixture
def recipe_service():
    return RecipeService()

@pytest.fixture
def sample_recipe():
    return Recipe(
        title="Healthy Smoothie",
        description="A nutritious breakfast smoothie",
        ingredients=[
            Ingredient(
                name="Banana",
                amount=1,
                unit="piece",
                calories_per_unit=105.0
            ),
            Ingredient(
                name="Greek Yogurt",
                amount=200,
                unit="g",
                calories_per_unit=0.59
            )
        ],
        instructions=["Blend all ingredients", "Serve cold"],
        prep_time=5,
        cook_time=2,
        servings=1,
        tags=["breakfast", "healthy", "quick"]
    )

@pytest.mark.asyncio
async def test_create_recipe(recipe_service, sample_recipe):
    created = await recipe_service.create_recipe(sample_recipe)
    assert created.id is not None
    assert created.title == sample_recipe.title

@pytest.mark.asyncio
async def test_get_recipe(recipe_service, sample_recipe):
    created = await recipe_service.create_recipe(sample_recipe)
    retrieved = await recipe_service.get_recipe(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id

@pytest.mark.asyncio
async def test_search_recipes(recipe_service, sample_recipe):
    await recipe_service.create_recipe(sample_recipe)
    
    # Test search by title
    results = await recipe_service.search_recipes("smoothie")
    assert len(results) == 1
    
    # Test search by tag
    results = await recipe_service.search_recipes(None, ["healthy"])
    assert len(results) == 1
    
    # Test search with no matches
    results = await recipe_service.search_recipes("pizza")
    assert len(results) == 0

@pytest.mark.asyncio
async def test_generate_meal_plan(recipe_service, sample_recipe):
    await recipe_service.create_recipe(sample_recipe)
    
    # Test valid meal plan generation
    meal_plan = await recipe_service.generate_meal_plan(1, 2000.0)
    assert len(meal_plan) == 3  # 3 meals for 1 day
    
    # Test meal plan with impossible constraints
    meal_plan = await recipe_service.generate_meal_plan(1, 10.0)
    assert len(meal_plan) == 0 
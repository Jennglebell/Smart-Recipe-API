from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from app.models.recipe import Recipe, Ingredient
from app.services.recipe_service import RecipeService
from app.utils.exceptions import RecipeNotFoundError, InvalidRecipeError, MealPlanGenerationError
from app.utils.validators import (
    validate_recipe_ingredients,
    validate_recipe_instructions,
    validate_recipe_times
)

router = APIRouter(tags=["recipes"])
recipe_service = RecipeService()

async def validate_recipe(recipe: Recipe):
    """Validate recipe data before processing"""
    if not validate_recipe_ingredients(recipe.ingredients):
        raise InvalidRecipeError("Invalid ingredients")
    if not validate_recipe_instructions(recipe.instructions):
        raise InvalidRecipeError("Invalid instructions")
    if not validate_recipe_times(recipe.prep_time, recipe.cook_time):
        raise InvalidRecipeError("Invalid preparation or cooking time")
    return recipe

@router.post("/recipes", response_model=Recipe)
async def create_recipe(recipe: Recipe = Depends(validate_recipe)):
    try:
        return await recipe_service.create_recipe(recipe)
    except Exception as e:
        raise InvalidRecipeError(str(e))

@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: str):
    recipe = await recipe_service.get_recipe(recipe_id)
    if not recipe:
        raise RecipeNotFoundError(recipe_id)
    return recipe

@router.get("/recipes", response_model=List[Recipe])
async def search_recipes(
    query: Optional[str] = None,
    tags: Optional[List[str]] = Query(None)
):
    try:
        return await recipe_service.search_recipes(query, tags)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching recipes: {str(e)}")

@router.get("/meal-plan", response_model=List[Recipe])
async def generate_meal_plan(
    days: int = Query(..., gt=0, le=7),
    calories_per_day: float = Query(..., gt=0)
):
    try:
        meal_plan = await recipe_service.generate_meal_plan(days, calories_per_day)
        if not meal_plan:
            raise MealPlanGenerationError(
                f"No suitable recipes found for {calories_per_day} calories per day"
            )
        return meal_plan
    except Exception as e:
        if isinstance(e, MealPlanGenerationError):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Error generating meal plan: {str(e)}"
        ) 
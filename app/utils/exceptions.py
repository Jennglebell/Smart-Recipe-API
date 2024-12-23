from fastapi import HTTPException

class RecipeException(HTTPException):
    """Base exception for recipe-related errors"""
    pass

class RecipeNotFoundError(RecipeException):
    def __init__(self, recipe_id: str):
        super().__init__(
            status_code=404,
            detail=f"Recipe with ID {recipe_id} not found"
        )

class InvalidRecipeError(RecipeException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=f"Invalid recipe: {message}"
        )

class MealPlanGenerationError(RecipeException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=f"Could not generate meal plan: {message}"
        ) 
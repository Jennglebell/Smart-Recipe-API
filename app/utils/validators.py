from typing import List
from app.models.recipe import Recipe, Ingredient

def validate_recipe_ingredients(ingredients: List[Ingredient]) -> bool:
    """
    Validate that ingredients have reasonable values
    """
    if not ingredients:
        return False
        
    for ingredient in ingredients:
        if ingredient.amount <= 0 or ingredient.calories_per_unit < 0:
            return False
        if not ingredient.unit or not ingredient.name:
            return False
    
    return True

def validate_recipe_instructions(instructions: List[str]) -> bool:
    """
    Validate that recipe instructions are properly formatted
    """
    if not instructions:
        return False
        
    return all(
        isinstance(step, str) and len(step.strip()) > 0 
        for step in instructions
    )

def validate_recipe_times(prep_time: int, cook_time: int) -> bool:
    """
    Validate that recipe times are reasonable
    """
    return prep_time > 0 and cook_time > 0 and (prep_time + cook_time) <= 24 * 60  # Max 24 hours 
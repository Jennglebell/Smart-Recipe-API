from typing import List, Optional
from app.models.recipe import Recipe
import asyncio

class RecipeService:
    def __init__(self):
        # In a real application, this would be a database
        self.recipes: List[Recipe] = []

    async def create_recipe(self, recipe: Recipe) -> Recipe:
        recipe.id = str(len(self.recipes) + 1)  # Simple ID generation
        self.recipes.append(recipe)
        return recipe

    async def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        return next((r for r in self.recipes if r.id == recipe_id), None)

    async def search_recipes(self, query: str, tags: List[str] = None) -> List[Recipe]:
        results = self.recipes
        
        if query:
            results = [
                r for r in results 
                if query.lower() in r.title.lower() or query.lower() in r.description.lower()
            ]
        
        if tags:
            results = [
                r for r in results 
                if any(tag in r.tags for tag in tags)
            ]
            
        return results

    async def generate_meal_plan(self, days: int, calories_per_day: float) -> List[Recipe]:
        """Generate a meal plan based on caloric requirements"""
        suitable_recipes = [
            r for r in self.recipes 
            if r.calculate_total_calories() <= calories_per_day / 3
        ]
        
        if not suitable_recipes:
            return []

        # Simple meal plan generation
        meal_plan = []
        for _ in range(days * 3):  # 3 meals per day
            meal_plan.append(suitable_recipes[len(meal_plan) % len(suitable_recipes)])
            
        return meal_plan 
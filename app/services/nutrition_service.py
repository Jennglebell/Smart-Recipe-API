from typing import List
from app.models.recipe import Ingredient

class NutritionService:
    RECOMMENDED_DAILY_VALUES = {
        'calories': 2000,
        'protein': 50,
        'fat': 70,
        'carbs': 260
    }

    def calculate_calories(self, ingredients: List[Ingredient]) -> float:
        """Calculate total calories for a list of ingredients"""
        return sum(
            ingredient.amount * ingredient.calories_per_unit 
            for ingredient in ingredients
        )

    def is_healthy_recipe(self, ingredients: List[Ingredient]) -> bool:
        """
        Determine if a recipe is healthy based on its caloric content
        and nutritional balance
        """
        total_calories = self.calculate_calories(ingredients)
        
        # Simple example: consider a recipe healthy if it's between 
        # 200-800 calories per serving
        return 200 <= total_calories <= 800

    def get_nutritional_info(self, ingredients: List[Ingredient]) -> dict:
        """
        Calculate comprehensive nutritional information for a recipe
        """
        total_calories = self.calculate_calories(ingredients)
        
        return {
            'calories': total_calories,
            'percent_daily_value': (total_calories / self.RECOMMENDED_DAILY_VALUES['calories']) * 100
        } 
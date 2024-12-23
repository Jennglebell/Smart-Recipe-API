from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str
    calories_per_unit: float

class Recipe(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10)
    ingredients: List[Ingredient]
    instructions: List[str]
    prep_time: int  # in minutes
    cook_time: int  # in minutes
    servings: int
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def calculate_total_calories(self) -> float:
        return sum(ing.amount * ing.calories_per_unit for ing in self.ingredients) 
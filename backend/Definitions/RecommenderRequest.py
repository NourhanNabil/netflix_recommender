from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    show_id : int
    model_name : str
    
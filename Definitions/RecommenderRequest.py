from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    show_id : str
    model_name : str
    
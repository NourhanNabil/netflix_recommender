from fastapi import FastAPI
import uvicorn

from Controllers import HealthController, RecommenderController

app = FastAPI()

app.include_router(HealthController.health_router)
app.include_router(RecommenderController.recommender_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

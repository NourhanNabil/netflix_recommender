from fastapi import FastAPI
import uvicorn
import os

from Controllers import HealthController, RecommenderController

app = FastAPI()

app.include_router(HealthController.health_router)
app.include_router(RecommenderController.recommender_router)

if __name__ == "__main__":
    uvicorn.run(app, host=os.environ['SERVICE_HOST'], port=os.environ['SERVICE_PORT'])

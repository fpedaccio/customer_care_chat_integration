# main.py
from fastapi import FastAPI
from routers.slack import router as slack_router
from settings import setup_cors

app = FastAPI()

# Include the Slack router
app.include_router(slack_router)

# Setup CORS
setup_cors(app)

@app.on_event("startup")
async def startup():
    # Add any startup actions, like connecting to external services
    pass

@app.on_event("shutdown")
async def shutdown():
    # Add any shutdown actions, like disconnecting from external services
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.main import router as apiRouter
from admin.main import router as adminRouter

# testing git
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=3005, reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apiRouter)
app.include_router(adminRouter)

@app.get('/')
def index():
    return "Welcome to the billing app"
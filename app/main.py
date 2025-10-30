import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.middleware import TimerMiddleware
from app.routers import auth, users, posts, tags

logging.basicConfig(
    level=logging.INFO,
    format='\033[1;36m%(asctime)s\033[0m | \033[1;32m%(levelname)s\033[0m | \033[1;34m%(message)s\033[0m'
)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador personalizado para errores de validación"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error de validación",
            "errors": [
                {
                    "loc": err["loc"],
                    "msg": err["msg"],
                    "type": err["type"]
                }
                for err in exc.errors()
            ]
        }
    )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TimerMiddleware)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(tags.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  
    )
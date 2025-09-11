from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import uvicorn

redirect_app = FastAPI()
redirect_app.add_middleware(HTTPSRedirectMiddleware)
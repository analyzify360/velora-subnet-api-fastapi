import time
import typer
import logging
import getpass
import os

from dotenv import load_dotenv
from typing import Annotated
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from subnet.validator_api import VeloraValidatorAPI

from communex._common import get_node_url  # type: ignore
from communex.client import CommuneClient  # type: ignore
from communex.compat.key import classic_load_key  # type: ignore


# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VeloraSubnetAPI:
    def __init__(self, 
        commune_key: Annotated[str, typer.Argument(help="Name of the key present in `~/.commune/key`")],
        use_testnet: bool = typer.Option(False)
    ):
        self.app = FastAPI()
        
        password = getpass.getpass(prompt="Enther the password:")
        keypair = classic_load_key(commune_key, password=password)  # type: ignore
        c_client = CommuneClient(get_node_url(use_testnet = use_testnet))  # type: ignore
        
        self.validator_api = VeloraValidatorAPI(keypair, 30, c_client, 60)

        # Add CORS middleware to allow cross-origin requests
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # You can specify allowed origins
            allow_credentials=True,
            allow_methods=["*"],  # Allow all HTTP methods
            allow_headers=["*"],  # Allow all headers
        )

        # Add custom request logging middleware
        self.app.add_middleware(RequestLoggingMiddleware)

        # Add request processing time middleware
        self.app.add_middleware(RequestTimeLoggingMiddleware)

        # Add exception handling middleware
        self.app.add_middleware(ExceptionHandlingMiddleware)

        # Define routes
        @self.app.get('/current-pool-metric')
        def getCurrentPoolMetric():
            return self.validator_api.getCurrentPoolMetric()

        @self.app.get('/current-token-metric')
        def getCurrentTokenMetric():
            return self.validator_api.getCurrentTokenMetric()

        @self.app.get('/token_metric')
        def getTokenMetric():
            return self.validator_api.getTokenMetric()

# Middleware to log request processing time
class RequestTimeLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()  # Record start time
        response = await call_next(request)  # Process the request
        process_time = time.time() - start_time  # Calculate processing time
        logger.info(f"Request {request.method} {request.url} processed in {process_time:.4f} seconds")
        response.headers["X-Process-Time"] = str(process_time)  # Optionally add it to response headers
        return response

# Middleware to log requests
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Received {request.method} request at {request.url}")
        response = await call_next(request)
        logger.info(f"Response status code: {response.status_code}")
        return response

# Middleware to handle exceptions globally
class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            response = JSONResponse(
                status_code=500,
                content={"detail": "An unexpected error occurred."}
            )
        return response

if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    app = VeloraSubnetAPI(os.getenv("COMMUNE_KEY"), False)
    uvicorn.run(app.app, host="0.0.0.0", port=8000)
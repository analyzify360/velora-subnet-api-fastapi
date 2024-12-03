import time
import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VeloraSubnetAPI:
    def __init__(self):
        self.app = FastAPI()

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
            return {"message": "Current pool metric data"}

        @self.app.get('/current-token-metric')
        def getCurrentTokenMetric():
            return {"message": "Current token metric data"}

        @self.app.get('/token_metric')
        def getTokenMetric():
            return {"message": "Token metric data"}

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
    api = VeloraSubnetAPI()
    uvicorn.run(api.app, host="0.0.0.0", port=8000)

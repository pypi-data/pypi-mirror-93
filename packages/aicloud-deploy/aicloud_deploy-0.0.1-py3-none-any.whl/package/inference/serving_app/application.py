import os
import re

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette_prometheus import PrometheusMiddleware

from kfserving.kfserving.kfmodel import KFModel
from .exceptions import InitServingException
from .settings import settings
from .service import service_route
from .serving import serving_route

_app = None

ORIGINS = [
    "*",
]


class ServingServer(KFModel):
    APP = None

    def __init__(self):
        self.name = os.environ.get('HOSTNAME')
        self.ready = False
        self.protocol = "v1"
        self.predictor_host = None
        self.explainer_host = None
        # The timeout matches what is set in generated Istio resources.
        # We generally don't want things to time out at the request level here,
        # timeouts should be handled elsewhere in the system.
        self.timeout = 600
        self._http_client_instance = None

    @property
    def app(self):
        if not self.APP:
            self.APP = FastAPI(
                title="Inference Serving Server",
                version="0.0.1",
                description="HTTP Service for serving you AI model",
                exception_handlers=None,
                middleware=(
                    Middleware(PrometheusMiddleware),
                    Middleware(
                        CORSMiddleware,
                        allow_origins=ORIGINS,
                        allow_credentials=True,
                        allow_methods=["*"],
                        allow_headers=["*"],
                    ),
                ),
            )

            self.APP.include_router(service_route)
            self.APP.include_router(serving_route)

            if settings.SENTRY_DSN:
                sentry_sdk.init(dsn=settings.SENTRY_DSN)
                self.APP.add_middleware(SentryAsgiMiddleware)

        return self.APP

    def start(self):
        self.load()
        uvicorn.run(
            self.app,
            reload=False,
            host=settings.HOST,
            port=settings.PORT,
            log_level=settings.LOG_LEVEL,
            http="h11",
            loop="asyncio",
        )

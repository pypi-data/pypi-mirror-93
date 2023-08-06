from fastapi import APIRouter

router = APIRouter(prefix="/v2")


@router.get("/health/live")
def liveness():
    return "OK"


@router.get("/models")
def get_models():
    return "OK"


@router.get("/models/([a-zA-Z0-9_-]+)/status")
def get_models():
    return "OK"


@router.get("/v2/models/([a-zA-Z0-9_-]+)/infer")
def get_models():
    return "OK"


@router.get("/models/([a-zA-Z0-9_-]+)/explain")
def get_models():
    return "OK"


@router.get("repository/models/([a-zA-Z0-9_-]+)/unload")
def get_models():
    return "OK"

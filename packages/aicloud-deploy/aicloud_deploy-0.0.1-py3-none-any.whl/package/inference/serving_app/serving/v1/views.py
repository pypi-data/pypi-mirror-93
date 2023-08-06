from fastapi import APIRouter

router = APIRouter(prefix="/v1")


@router.get("/model/([a-zA-Z0-9_-]+):predict")
def predict():
    return "OK"


@router.get("/models")
def models_list():
    return "OK"


@router.get("/models/([a-zA-Z0-9_-]+):explain")
def explain():
    return "OK"


@router.get("/models/([a-zA-Z0-9_-]+)")
def get_model():
    return "OK"

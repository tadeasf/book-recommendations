from fastapi import APIRouter, Request
from scalar_fastapi import get_scalar_api_reference

router = APIRouter()

@router.get("/scalar", include_in_schema=False)
async def scalar_html(request: Request):
    return get_scalar_api_reference(
        openapi_url=request.app.openapi_url,
        title=request.app.title,
    )

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

view_router = APIRouter(prefix="/template", tags=["view_router"])


@view_router.get("/", response_class=HTMLResponse)
async def interface():

    with open("view/interface.html") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content, status_code=200)

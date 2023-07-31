from typing_extensions import Annotated

from fastapi import FastAPI, HTTPException, Form
from starlette.requests import Request
from starlette.responses import HTMLResponse
from google.oauth2 import id_token
from google.auth.transport import requests

from starlette.templating import Jinja2Templates

app = FastAPI()


templates = Jinja2Templates(directory="templates")

GOOGLE_CLIENT_ID = "using your google client id here"


@app.get('/')
async def homepage(request: Request):
    return HTMLResponse('<a href="/login">login</a>')

@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.post('/auth')
async def auth(credential: Annotated[str, Form()], request: Request):
    print("request ----- ", credential)
    try:
        idinfo = id_token.verify_oauth2_token(credential, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(403, "Bad code")
    else:
        print(idinfo)
    return templates.TemplateResponse("login_success.html", {"request": request, "uid": idinfo['sub']})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

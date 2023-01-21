from fastapi import FastAPI, Path, Query, Body, Form, File, UploadFile, Header, Cookie, Request, status, Response, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse 

app = FastAPI()

class UserType(str, Enum):
    STANDARD = "standard"
    ADMIN = 'admin'


class User(BaseModel):
    name: str
    age: int 

class Post(BaseModel):
    title: str
    nb_views: int


# Response Model
class PublicPost(BaseModel):
    title: str


@app.get('/')
async def hello_world(hello: str = Header(...)):
    return {'hello': hello}

@app.get('/req')
async def get_request_object(request: Request):
    return {'path': request.url.path}

@app.get('/agent')
async def get_header(user_agent: str = Header(...)):
    return {'user_agent': user_agent}

@app.get('/cookie')
async def get_cookie(hello: Optional[str] = Cookie(None)):
    return {'hello': hello}


@app.get('/users/{id}')
async def get_user(id: int = Path(..., ge=1)):
    return {'id': id}

@app.get('/users/{type}/{id}')
async def get_user_type(type: UserType, id: int):
    return {'type': type, 'id': id}

@app.get('/license-plates/{license}')
async def get_license_plate(license: str = Path(..., regex=r'^\w{2}-\d{3}-\w{2}$')):
    return {'license': license}

@app.get('/users_pag')
async def get_users_pagination(page: int = Query(1, gt=0), size: int = Query(10, le=100)):
    return {'page': page, 'size': size}

@app.post('/users')
async def create_user(user: User, priority: int = Body(..., ge=1, le=3)):
    return {'user': user, 'priority': priority}

@app.post('/users/form')
async def create_user_form(name: str = Form(...), age: int = Form(...)):
    return {'name': name, 'age': age}
    
# @app.post('/files')
# async def upload_file(file: bytes = File(...)):
#     return {"file_size": len(file)}

@app.post('/files')
async def upload_file(file: UploadFile = File(...)):
    return {"file_name": file.filename, 'content-type': file.content_type}

@app.post('/files/multiple')
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    return [
        {'file_name': file.filename, 'content_type': file.content_type}
        for file in files
    ]


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    return post

# Dummy database
posts = {
    1: Post(title='Hello', nb_views=100),
}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    posts.pop(id, None)
    return None

@app.put('/posts/{id}')
async def update_or_create_post(id: int, post: Post, response: Response):
    if id not in posts:
        response.status_code = status.HTTP_201_CREATED
    posts[id] = post
    return posts[id]

@app.get('/posts/{id}', response_model=PublicPost)
async def get_post(id: int):
    return posts[id]

@app.get('/response')
async def get_response(response: Response):
    response.headers['Custom-Header'] = "Custom-header-value"
    response.set_cookie('cookie-name', 'cookie-value', max_age=86400)
    return {'hello': 'world'}

@app.post('/password')
async def check_password(password: str = Body(...), password_confirm: str = Body(...)):
    if password != password_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={ 
                'message': 'Password dont match.',
                'hints': [
                    'Check the caps lock on your keyboard',
                    'Try to make the password visible by clicking on the eye icon to check your typing',
                ],
            },
        )
    return {"message": "Password match."}

@app.get('/html', response_class=HTMLResponse)
async def get_html():
    return '''
        <html>
            <head>
                <title>Hello world!</title>
            </head>
            <body>
                <h1>Hello world!</h1>
            </body>
        </html>
    '''

@app.get('/text', response_class=PlainTextResponse)
async def text():
    return "Hello world!"

@app.get('/redirect')
async def redirect():
    return RedirectResponse('/new-url', status_code=status.HTTP_301_MOVED_PERMANENTLY)

@app.get('/cat')
async def get_cat():
    root_directory = path.dirname(path.dirname(__file__))
    picture_path = path.join(root_directory, 'assets', 'example.jpg')
    return FileResponse(picture_path)

@app.get('/xml')
async def get_xml():
    content = '''<?xml version='1.0' encoding='UTF-8'?>
        <Hello>World</Hello>
    '''
    return Response(content=content, media_type='application/xml')
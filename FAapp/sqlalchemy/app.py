from fastapi import FastAPI, Depends, HTTPException, Query, status 
from typing import List, Tuple
from database import Database
from FAapp.sqlalchemy.database import sqlalchemy_engine, get_database
from FAapp.sqlalchemy.models import( 
        metadata, 
        posts,
        PostDB,
        PostCreate,
        PostPartialUpdate 
)

app = FastAPI()

@app.on_event('startup')
async def startup():
    await database.connect()
    metadata.create_all(sqlalchemy_engine)
    
@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
    
    
@app.post('/posts', response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, database: Database = Depends(get_database)) -> PostDB:
    insert_query    = posts.insert().value(post.dict())
    post_id         = await database.execute(insert_query)
    post_db         = await get_post_or_404(post_id, database)
    return post_db
    
@app.get('/posts')
async def list_posts(
    pagination  :   Tuple[int, int]     = Depends(pagination),
    database    :   Database            = Depends(get_database),
) -> List[PostDB]:
    skip, limit     = pagination
    select_query    = post.select().offset(skip).limit(limit)
    rows            = await database.fetch_all(select_query)
    results         = [PostDB(**row) for row in rows]
    return results 

@app.get('/posts/{id}', response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post

async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query    =   posts.select().where(posts.c.id == id)
    raw_post        =   await database.fetch_one(select_query)
    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return PostDB(**raw_post)
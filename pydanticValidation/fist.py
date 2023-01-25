from pydantic import BaseModel 
from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ValidationError, Field, EmailStr, HttpUrl, validator, root_validator


class Gender(str, Enum):
    MALE    = 'MALE'
    FEMALE  = 'FEMALE'

class Address(BaseModel):
    street_address  :   str
    postal_code     :   str
    city            :   str
    country         :   str

class Person(BaseModel):
    first_name              :   str             =   Field(..., min_length=3)
    last_name               :   str             =   Field(..., min_length=3)
    email                   :   EmailStr
    age                     :   Optional[int]   =   Field(None, ge=0, le=120)
    gender                  :   Gender
    birthdate               :   date
    website                 :   HttpUrl
    interests               :   List[str]
    address                 :   Address
    location                :   Optional[str]   = None
    subscribed_newsletter   :   bool = True


person = Person(
    first_name  =   'John',
    last_name   =   'Doe',
    gender      =   Gender.MALE,
    birthdate   =   '1991-01-01',
    interests   =   ['travel', 'sports'],
    address     =   {
        'street_address'    :   '12 Squirell Street',
        'postal_code'       :   '424242',
        'city'              :   'Woodtown',
        'country'           :   'US',
    }, 
)

print(person)


def list_factory():
    return ['a', 'b', 'c']

#Dynamic default values
class Model(BaseModel):
    l   :   List[str]   =   Field(default_factory=list_factory)
    d   :   datetime    =   Field(default_factory=datetime.now)
    l2  :   List[str]   =   Field(default_factory=list)


# class PostCreate(BaseModel):
#     title   :   str
#     content :   str


# class PostPublic(BaseModel):
#     id      :   int
#     title   :   str
#     content :   str


# class PostDB(BaseModel):
#     id          :   int
#     title       :   str
#     content     :   str
#     nb_views    :   int   =   0   


class PostBase(BaseModel):
    title       :   str
    content     :   str

    def excerpt(self) -> str:
        return f'{self.content[:140]}...'

class PostCreate(PostBase):
    pass

class PostPublic(PostBase):
    id  :   int

class PostDB(PostBase):
    id          :   int
    nb_views    :   int = 0


# Validation at field level
class User(BaseModel):
    first_name  :   str
    last_name   :   str
    birthdate   :   date

    @validator('birthdate')
    def valid_birthdate(cls, v: date):
        delta   =   data.today() - v
        age     =   delta.days / 365
        if age > 120:
            raise ValueError('You seem a bit too old!')
        return v

# Validation at object level
class UserRegistration(BaseModel):
    email                   :   EmailStr
    password                :   str
    password_confirmation   :   str

    @root_validator()
    def password_match(cls, values):
        password                =   values.get('password')
        password_confirmation   =   values.get('password_confirmation')
        if password != password_confirmation:
            raise ValueError('Passwords don\'t match')
        return values

#Applying validation before Pydantic parsing
class Model(BaseModel):
    values      :   List[int]

    @validator('values', pre=True)
    def split_string_values(cls, v):
        if isinstance(v, str):
            return v.split(',')
        return v


person = Person(
    first_name      =   'John',
    last_name       =   'Doe',
    gender          =   Gender.MALE,
    birthdate       =   '1991-01-01',
    interests       =   ['travel', 'sports'],
    address         =   {
        'street_address'    :   '12 Squirell Street',
        'postal_code'       :   '424242',
        'city'              :   'Woodtown',
        'country'           :   'US',
    },
)

person_dict     = person.dict()
person_include  = person.dict(include={'first_name', 'last_name'})


#Creating an instance from a sub-class object
class PostBase(BaseModel):
    title       :   str
    content     :   str

class PostParticularUpdate(BaseModel):
    title       :   Optional[str]   =   None
    content     :   Optional[str]   =   None


@app.patch('/posts/{id}', response_model=PostPublic)
async def partial_update(id: int, post_update: PostParticularUpdate):
    try:
        post_db             =   db.posts[id]
        updated_fields      =   post_update.dict(exclude_unset=True)
        update_post         =   post_db.copy(update=updated_fields)
        db.posts[id]        =   update_post
        return update_post
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)



























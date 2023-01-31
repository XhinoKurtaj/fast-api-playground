from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email    :      EmailStr
    
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password    : str

class User(UserBase):
    id  :   int

class UserDB(User):
    hashed_password :   str


class UserTortoise(Model):
    id = fields.IntField(pk=True, generate=True)
    email = fields.CharField(index=True, unique=True, null=False, max_length=255)
    hashed_password = fields.CharField(null=False)

    class Meta:
        table = 'users'

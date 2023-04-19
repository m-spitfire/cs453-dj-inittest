from dataclasses import dataclass



class FieldNodeType:
    ...


class Model(FieldNodeType):
    """Foreign Key (e.g., Post, User)"""
    ...

class DB_FIELD(FieldNodeType):
    """Database Fields (e.g., VARCHAR)"""
    ...

@dataclass
class Varchar(DB_FIELD):
    max_len: int = 20

class Text(DB_FIELD):
    ...



from interface import API

apis = [
    API(
        method="GET",
        path="posts/",
        request_type={},
        response_type={
            "items": {
                "properties": {
                    "User::author": {"type": "integer"},
                    "content": {"type": "string"},
                    "Post::id": {"type": "integer"},
                    "title": {"type": "string"},
                },
                "required": ["title", "content", "User::author", "id"],
                "type": "object",
            },
            "type": "array",
        },
        uses=["Post"],
        creates=[],
    ),
    API(
        method="POST",
        path="posts/",
        request_type={
            "properties": {
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "title": {"type": "string"},
            },
            "required": ["title", "content", "User::author"],
            "type": "object",
        },
        response_type={
            "properties": {
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "Post::id": {"type": "integer"},
                "title": {"type": "string"},
            },
            "required": ["title", "content", "User::author", "id"],
            "type": "object",
        },
        uses=["User"],
        creates=["Post"],
    ),
    API(
        method="POST",
        path="fancy-posts/",
        request_type={
            "properties": {
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "title": {"type": "string"},
            },
            "required": ["title", "content", "User::author"],
            "type": "object",
        },
        response_type={
            "properties": {
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "Post::id": {"type": "integer"},
                "title": {"type": "string"},
            },
            "required": ["title", "content", "User::author", "id"],
            "type": "object",
        },
        uses=["User"],
        creates=["Post"],
    ),
    API(
        method="GET",
        path="posts/<int:Post::pk/",
        request_type={},
        response_type={
            "properties": {
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "Post::id": {"type": "integer"},
                "title": {"type": "string"},
            },
            "required": ["title", "content", "User::author", "id"],
            "type": "object",
        },
        uses=["Post"],
        creates=[],
    ),
    API(
        method="PUT",
        path="posts/<int:Post::pk/",
        request_type={
            "properties": {
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "title": {"type": "string"},
            },
            "required": [],
            "type": "object",
        },
        response_type={
            "properties": {
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "Post::id": {"type": "integer"},
                "title": {"type": "string"},
            },
            "required": ["title", "content", "User::author", "id"],
            "type": "object",
        },
        uses=["Post"],
        creates=[],
    ),
    API(
        method="DELETE",
        path="posts/<int:Post::pk/",
        request_type={},
        response_type={},
        uses=["Post"],
        creates=[],
    ),
   API(
        method="GET",
        path="users/",
        request_type={},
        response_type={
            "items": {
                "properties": {
                    "email": {"type": "string"},
                    "User::id": {"type": "integer"},
                    "username": {"type": "string"},
                },
                "required": ["username", "email", "id"],
                "type": "object",
            },
            "type": "array",
        },
        uses=["User"],
        creates=[],
    ),
    API(
        method="POST",
        path="users/",
        request_type={
            "properties": {"email": {"type": "string"}, "username": {"type": "string"}},
            "required": ["username", "email"],
            "type": "object",
        },
        response_type={
            "properties": {
                "email": {"type": "string"},
                "User::id": {"type": "integer"},
                "username": {"type": "string"},
            },
            "required": ["username", "email", "id"],
            "type": "object",
        },
        uses=[],
        creates=["User"],
    ),
    API(
        method="GET",
        path="users/<int:User::pk/",
        request_type={},
        response_type={
            "properties": {
                "email": {"type": "string"},
                "User::id": {"type": "integer"},
                "username": {"type": "string"},
            },
            "required": ["username", "email", "id"],
            "type": "object",
        },
        uses=["User"],
        creates=[],
    ),
    API(
        method="PUT",
        path="users/<int:User::pk/",
        request_type={
            "properties": {"email": {"type": "string"}, "username": {"type": "string"}},
            "required": [],
            "type": "object",
        },
        response_type={
            "properties": {
                "email": {"type": "string"},
                "User::id": {"type": "integer"},
                "username": {"type": "string"},
            },
            "required": ["username", "email", "id"],
            "type": "object",
        },
        uses=["User"],
        creates=[],
    ),
    API(
        method="DELETE",
        path="users/<int:User::pk/",
        request_type={},
        response_type={},
        uses=["User"],
        creates=[],
    ),
]

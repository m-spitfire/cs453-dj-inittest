from interface import APINode

apis = [
    APINode(
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
    APINode(
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
    APINode(
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
    APINode(
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
    APINode(
        method="DELETE",
        path="posts/<int:Post::pk/",
        request_type={},
        response_type={},
        uses=["Post"],
        creates=[],
    ),
    APINode(
        method="GET",
        path="comments/",
        request_type={},
        response_type={
            "items": {
                "properties": {
                    "Post::post": {"type": "integer"},
                    "User::author": {"type": "integer"},
                    "content": {"type": "string"},
                    "Comment::id": {"type": "integer"},
                },
                "required": ["User::author", "content", "Post::post", "id"],
                "type": "object",
            },
            "type": "array",
        },
        uses=["Comment"],
        creates=[],
    ),
    APINode(
        method="POST",
        path="comments/",
        request_type={
            "properties": {
                "Post::post": {"type": "integer"},
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
            },
            "required": ["User::author", "content", "Post::post"],
            "type": "object",
        },
        response_type={
            "properties": {
                "Post::post": {"type": "integer"},
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "Comment::id": {"type": "integer"},
            },
            "required": ["User::author", "content", "Post::post", "id"],
            "type": "object",
        },
        uses=["User", "Post"],
        creates=["Comment"],
    ),
    APINode(
        method="GET",
        path="comments/<int:Comment::pk/",
        request_type={},
        response_type={
            "properties": {
                "Post::post": {"type": "integer"},
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "Comment::id": {"type": "integer"},
            },
            "required": ["User::author", "content", "Post::post", "id"],
            "type": "object",
        },
        uses=["Comment"],
        creates=[],
    ),
    APINode(
        method="PUT",
        path="comments/<int:Comment::pk/",
        request_type={
            "properties": {
                "Post::post": {"type": "integer"},
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
            },
            "required": [],
            "type": "object",
        },
        response_type={
            "properties": {
                "Post::post": {"type": "integer"},
                "User::author": {"type": "integer"},
                "content": {"type": "string"},
                "Comment::id": {"type": "integer"},
            },
            "required": ["User::author", "content", "Post::post", "id"],
            "type": "object",
        },
        uses=["Comment"],
        creates=[],
    ),
    APINode(
        method="DELETE",
        path="comments/<int:Comment::pk/",
        request_type={},
        response_type={},
        uses=["Comment"],
        creates=[],
    ),
    APINode(
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
    APINode(
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
    APINode(
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
    APINode(
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
    APINode(
        method="DELETE",
        path="users/<int:User::pk/",
        request_type={},
        response_type={},
        uses=["User"],
        creates=[],
    ),
]

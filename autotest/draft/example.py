"""
What should writer automatically generate
"""

"""
TODO
How can we find the path to import models?
"""
from ... import Post, User


def helper_create_user():
    """
    TODO:
    we may not need this since user has no deps
    instead, we can call body directly from the dependers
    """

    u = User.objects.create(
        email="sangachoi@kaist.ac.kr", username="retroinspect", password="passwd"
    )
    u.save()
    return u


def helper_create_post():
    u = helper_create_user()
    p = Post.objects.create(title="title", content="content", author=u)
    p.save()
    return p

from django.contrib.auth import get_user_model

User = get_user_model()


def _paginate(offset: int, limit: int):
    offset = max(offset, 0)
    limit  = min(max(limit, 1), 100)
    return offset, limit


def get_user_by_id(user_id: str):
     return User.objects.filter(id=user_id).first()


def get_user_by_email(email: str):
     return User.objects.filter(email=email).first()


def list_users(offset: int = 0, limit: int = 20):
    offset, limit = _paginate(offset, limit)
    return User.objects.all()[offset:offset + limit]


def list_active_users(offset: int = 0, limit: int = 20):
    offset, limit = _paginate(offset, limit)
    return User.objects.filter(is_active=True)[offset:offset + limit]


def list_inactive_users(offset: int = 0, limit: int = 20):
    offset, limit = _paginate(offset, limit)
    return User.objects.filter(is_active=False)[offset:offset + limit]


def list_users_by_school(school_id: str, offset: int = 0, limit: int = 20):
    offset, limit = _paginate(offset, limit)
    return User.objects.filter(school_id=school_id)[offset:offset + limit]


def list_users_by_school_name(school_name: str, offset: int = 0, limit: int = 20):
    offset, limit = _paginate(offset, limit)
    return User.objects.filter(school__name__icontains=school_name)[offset:offset + limit]


def list_users_by_role(role: str, offset: int = 0, limit: int = 20):
    offset, limit = _paginate(offset, limit)
    return User.objects.filter(role=role)[offset:offset + limit]
from users.models import User
from rest_framework.response import Response
from .models import Organization
from functools import wraps

PERMISSION_ERROR = {
    "message": "You do not have enough permissions to access this view!"
}

# Allow view only if is a organization owner.
def is_organization_owner(f):
    @wraps(f)
    def wrapper(request):
        if request.user.is_authenticated and (
            request.user.role == User.ORGANIZATION_OWNER or request.user.is_superuser
        ):
            return f(request)
        return Response(PERMISSION_ERROR, status=403)

    return wrapper

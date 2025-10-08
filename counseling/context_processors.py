from django.contrib.auth.models import Group


def user_role(request):
    """Return a simple role string for the currently logged-in user.

    Roles returned: 'admin', 'counselor', 'class_incharge', 'hod', 'director', or ''
    This looks for group membership first, then falls back to is_superuser.
    """
    role = ''
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        if user.is_superuser:
            role = 'admin'
        else:
            # check groups in priority order
            if user.groups.filter(name__iexact='counselor').exists():
                role = 'counselor'
            elif user.groups.filter(name__iexact__in=['class_incharge','incharge','class-incharge']).exists():
                role = 'class_incharge'
            elif user.groups.filter(name__iexact='hod').exists():
                role = 'hod'
            elif user.groups.filter(name__iexact='director').exists():
                role = 'director'
    return {'user_role': role}

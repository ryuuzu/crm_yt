from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(viewFunc):
    def wrapperFunc(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return viewFunc(request, *args, **kwargs)

    return wrapperFunc


def admin_only(redirectTo="accounts:user"):
    def decorator(viewFunc):
        def wrapperFunc(request, *args, **kwargs):
            if request.user.groups.exists():
                groupNames = [
                    group.name for group in request.user.groups.all()]

                if "Admin" in groupNames:
                    return viewFunc(request, *args, **kwargs)
                else:
                    return redirect(redirectTo)
        return wrapperFunc
    return decorator


def allowed_users(allowed_roles=[]):
    def decorator(viewFunc):
        def wrapperFunc(request: HttpRequest, *args, **kwargs):
            allowed = False
            if request.user.groups.exists():
                for group in request.user.groups.all():
                    if group.name in allowed_roles:
                        allowed = True
                        break
            if allowed:
                return viewFunc(request, *args, **kwargs)

            return HttpResponse("You are not allowed to view this page.")

        return wrapperFunc

    return decorator

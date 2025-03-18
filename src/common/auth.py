from functools import wraps
from account.models import CustomUser
from django.http import HttpResponseForbidden, HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from common.django_utils import AsyncViewT
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


__all__ = [
    'aclient_required',
    'awriter_required',
    'aanonymous_required',
    'aprofile_required',
    'ensure_for_current_user',
]

USER_PROFILES = {
    'client': lambda user: not user.is_writer,
    'writer': lambda user: user.is_writer,
}


def aclient_required(client_view: AsyncViewT):
    @login_required(login_url='login')
    @wraps(client_view)
    async def fun(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = await aget_user(request)
        if user.is_authenticated and not user.is_writer:
            return await client_view(request, *args, **kwargs)
        return HttpResponseForbidden('Only clients can access this page')
    return fun 

def aanonymous_required(original_view: AsyncViewT):
    @wraps(original_view)
    async def decorated_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = await aget_user(request)
        redirect_to = (
            'writer-dashboard' if user.is_authenticated and user.is_writer else
            'client-dashboard' if user.is_authenticated else
            ''
        )
        if redirect_to:
            return redirect(redirect_to)
        return await original_view(request, *args, **kwargs)
    return decorated_view

def awriter_required(writer_view: AsyncViewT):
    @login_required(login_url='login')
    @wraps(writer_view)
    async def fun(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = await aget_user(request)
        if user.is_authenticated and user.is_writer:
            return await writer_view(request, *args, **kwargs)
        return HttpResponseForbidden('Only writers can access this page')
    return fun   

def ensure_for_current_user(model: type, *, id_in_url: str = 'id', redirect_if_missing: str):
    def decorator(view: AsyncViewT):
        async def async_view(request: HttpRequest, *args, **kargs) -> HttpResponse:
            obj_id = kargs[id_in_url]
            current_user = await aget_user(request)
            try:
                obj = await model.objects.aget(id = obj_id, user = current_user)
                del kargs[id_in_url]
                return await view(request, obj, *args, **kargs)
            except ObjectDoesNotExist:
                return redirect(redirect_if_missing)
        return async_view
    return decorator

def aprofile_required(profile: str, login_url: str = 'login'):
    if profile not in USER_PROFILES:
        raise ValueError(f"Unknown profile: {profile}")
    is_of_profile = USER_PROFILES[profile]
    def decorator(original_view: AsyncViewT):
        @login_required(login_url=login_url) # type: ignore
        @wraps(original_view)
        async def decorated_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            user: CustomUser = await aget_user(request)
            if user.is_authenticated and is_of_profile(user):
                return await original_view(request, *args, **kwargs)
            return HttpResponseForbidden(f"Only members of '{profile}' can access this page")
        return decorated_view
    return decorator
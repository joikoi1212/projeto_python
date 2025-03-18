__all__ = (
    'AsyncFormMixin',
    'AsyncModelFormMixin',
    'arender',
    'AsyncViewT'
    'alogout'
)

from django import forms
from django.contrib import auth
from django.http import HttpResponse, HttpRequest
from asgiref.sync import sync_to_async
from django.shortcuts import render
from typing import Protocol

class AsyncViewT(Protocol):
    async def __call__(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        ...

class AsyncFormMixin(forms.BaseForm):

    @sync_to_async
    def ais_valid(self):
        return self.is_valid()
    
    @sync_to_async
    def arender(self):
        return self.render()


class AsyncModelFormMixin(AsyncFormMixin):
    async def asave(self: forms.ModelForm, *args, **kwargs):
        @sync_to_async
        def sync_call_save():
            return self.save(*args, **kwargs)
        return await sync_call_save()
       
async def arender(*render_args, **render_kwargs) -> HttpResponse:
    @sync_to_async
    def sync_call_render() -> HttpResponse:
        return render(*render_args, **render_kwargs)
    return await sync_call_render()

async def alogout(*render_args, **render_kwargs) -> HttpResponse:
    @sync_to_async
    def sync_call_logout():
        auth.logout(*render_args, **render_kwargs)
    await snyc_call_logout()
"""Django extension that allow using asynchronous generators in StreamingHttpResponse

Patch application and use AsyncStreamingHttpResponse instead of django's StreamingHttpResponse
"""
import types

from django.core.handlers.asgi import ASGIHandler as ASGIHandlerOriginal
from ._classes import AsyncStreamingHttpResponse, AsyncStreamingAsgiHandlerMixin


class ASGIHandler(AsyncStreamingAsgiHandlerMixin, ASGIHandlerOriginal):
    pass


def patch_application(application):
    assert isinstance(application, ASGIHandlerOriginal)
    application.send_response = types.MethodType(AsyncStreamingAsgiHandlerMixin.send_response, application)


__author__ = 'svinerus (svinerus@gmail.com)'
__version__ = '0.3'
__all__ = [
    'AsyncStreamingHttpResponse',
    'AsyncStreamingAsgiHandlerMixin', 'ASGIHandler', 'patch_application'
]

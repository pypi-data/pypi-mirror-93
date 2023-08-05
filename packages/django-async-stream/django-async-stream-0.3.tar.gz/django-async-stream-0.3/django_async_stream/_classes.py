from asgiref.sync import sync_to_async
from django.http.response import HttpResponseBase


class AsyncStreamingAsgiHandlerMixin:
    async def send_response(self, response, send):
        """Encode and send a response out over ASGI."""
        # Collect cookies into headers. Have to preserve header case as there
        # are some non-RFC compliant clients that require e.g. Content-Type.
        response_headers = []
        for header, value in response.items():
            if isinstance(header, str):
                header = header.encode('ascii')
            if isinstance(value, str):
                value = value.encode('latin1')
            response_headers.append((bytes(header), bytes(value)))
        for c in response.cookies.values():
            response_headers.append(
                (b'Set-Cookie', c.output(header='').encode('ascii').strip())
            )
        # Initial response message.
        await send({
            'type': 'http.response.start',
            'status': response.status_code,
            'headers': response_headers,
        })
        # Streaming responses need to be pinned to their iterator.
        if response.streaming:
            # Access `__iter__` and not `streaming_content` directly in case
            # it has been overridden in a subclass.

            # ######### THE LIBRARY CHANGES ONLY LINE BELOW ###########
            if isinstance(response, AsyncStreamingHttpResponse):
                async for part in response:
                    for chunk, _ in self.chunk_bytes(part):
                        await send({
                            'type': 'http.response.body',
                            'body': chunk,
                            # Ignore "more" as there may be more parts; instead,
                            # use an empty final closing message with False.
                            'more_body': True,
                        })
            else:
                for part in response:
                    for chunk, _ in self.chunk_bytes(part):
                        await send({
                            'type': 'http.response.body',
                            'body': chunk,
                            # Ignore "more" as there may be more parts; instead,
                            # use an empty final closing message with False.
                            'more_body': True,
                        })
            # Final closing message.
            await send({'type': 'http.response.body'})
        # Other responses just need chunking.
        else:
            # Yield chunks of response.
            for chunk, last in self.chunk_bytes(response.content):
                await send({
                    'type': 'http.response.body',
                    'body': chunk,
                    'more_body': not last,
                })
        await sync_to_async(response.close, thread_sensitive=True)()


class AsyncStreamingHttpResponse(HttpResponseBase):
    streaming = True

    def __init__(self, streaming_content=(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._streaming_content = streaming_content

    async def stream_content(self):
        async for i in self._streaming_content:
            yield self.make_bytes(i)

    def __aiter__(self):
        return self.stream_content()

    def __iter__(self):
        raise RuntimeError(f"{self.__class__.__name__} working only under patched ASGI")



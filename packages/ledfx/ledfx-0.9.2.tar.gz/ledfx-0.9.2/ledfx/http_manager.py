import logging
import os
import sys

import aiohttp_jinja2
import jinja2
from aiohttp import web

import ledfx_frontend
from ledfx.api import RestApi

try:
    base_path = sys._MEIPASS
except BaseException:
    base_path = os.path.abspath(".")

_LOGGER = logging.getLogger(__name__)


class HttpServer(object):
    def __init__(self, ledfx, host, port):
        """Initialize the HTTP server"""

        self.app = web.Application()
        self.api = RestApi(ledfx)
        templates_path = os.path.abspath(
            os.path.dirname(ledfx_frontend.__file__)
        )
        aiohttp_jinja2.setup(
            self.app, loader=jinja2.FileSystemLoader(templates_path)
        )
        self.register_routes()

        self._ledfx = ledfx
        self.host = host
        self.port = port

    @aiohttp_jinja2.template("index.html")
    async def index(self, request):
        return {}

    def register_routes(self):
        self.api.register_routes(self.app)
        self.app.router.add_static(
            "/static",
            path=ledfx_frontend.where() + "/static",
            name="static",
        )

        self.app.router.add_route("get", "/", self.index)
        self.app.router.add_route("get", "/{extra:.+}", self.index)

    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        try:
            site = web.TCPSite(self.runner, self.host, self.port)
            await site.start()
        except OSError as error:
            _LOGGER.error(
                "Failed to create HTTP server at port %d: %s",
                self.port,
                error,
            )

        self.base_url = ("http://{}:{}").format(self.host, self.port)
        print(("Started webinterface at {}").format(self.base_url))

    async def stop(self):
        await self.app.shutdown()
        if self.runner:
            await self.runner.cleanup()
        await self.app.cleanup()

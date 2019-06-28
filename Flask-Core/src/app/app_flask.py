from core.base_flask import BaseFlask, Controller
from core.request import Response, Request


class AppFlask(BaseFlask):
    def on_intercept(self, req: Request, res: Response):
        return None


class AppController(Controller):
    def on_intercept(self, req: Request, res: Response):
        if req.header("Authorization") is None:
            return res.unauthor("Token fail")
        return None


app = AppFlask(__name__)

from core.request import Request, Response
from src.app.app_cache import AppCache
from src.app.app_flask import app, AppController


class User(AppController):
    def __init__(self, app_cache: AppCache):
        self.app_cache = app_cache

    @app.get("")
    def get_profile(self, res: Response):
        return res.success(f"User success {self.app_cache.nameCached}")

    @app.post("")
    def post_profile(self, req: Request, res: Response):
        return res.success(f'{req.authorization()}\'s post profile')

from src.app.app_cache import AppCache
from src.app.app_flask import app, AppController
from core.injector import inject
from core.request import Request, Response


class User(AppController):

    @inject
    def app_cache(self) -> AppCache: pass

    @app.link("", ["GET", "POST"])
    def profile(self, req: Request, res: Response):
        return req.on(get=self.get_profile, post=self.post_profile)

    def get_profile(self, req: Request, res: Response):
        return res.success('{}\'s get profile and {}'.format(req.authorization(), self.app_cache().nameCached))

    def post_profile(self, req: Request, res: Response):
        return res.success('{}\'s post profile'.format(req.authorization()))

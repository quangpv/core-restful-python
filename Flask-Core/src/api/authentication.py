from src.app.app_flask import app
from src.app.app_validator import Validator
from core.base_flask import Controller
from core.request import Request, Response
from core.validation import Validation


class Authentication(Controller):

    @app.post("login", validate=Validation([
        Validator.email,
        Validator.password,
    ]))
    def login(self, req: Request, res: Response):
        return res.success("Login success")

    @app.post("registry", validate=Validation([
        Validator.email,
        Validator.password
    ]))
    def registry(self, req: Request, res: Response):
        return res.success('{}\'s profile registered'.format(req.form("email")))

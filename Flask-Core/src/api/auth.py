from core.base_flask import Controller
from core.request import Request, Response
from core.validation import Validation
from src.app.app_flask import app
from src.app.app_validator import Validator


class Auth(Controller):

    def __init__(self):
        pass

    @app.post("login", validate=Validation([
        Validator.email,
        Validator.password,
    ]))
    def login(self, res: Response):
        return res.success("login success")

    @app.post("registry", validate=Validation([
        Validator.email,
        Validator.password
    ]))
    def registry(self, req: Request, res: Response):
        return res.success(f'{req.form("email")}\'s profile registered')

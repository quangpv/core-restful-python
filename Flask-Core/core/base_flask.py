from typing import List, Any

import qpvdi
from flask import Flask, request

from core.request import Request, Response
from core.validation import Validation


class Controller(object):
    def on_intercept(self, req: Request, res: Response) -> Any:
        """
        Intercept request after by pass by app intercept and before Validation
        :param req: Request
        :param res: Response
        """
        pass


class BaseFlask(Flask):
    __cache = dict()
    __router_cache = dict()

    @staticmethod
    def __getTypeName(f):
        return f.__qualname__.split(".")[0]

    @staticmethod
    def __makeOptions(methods: List[str]):
        options = {
            "methods": methods
        }
        return options

    @staticmethod
    def __make_path(f_class_name, rule):
        if str(rule).__len__() == 0:
            return "/{}".format(f_class_name.lower())
        return "/{}/{}".format(f_class_name.lower(), rule)

    def __link(self, rule, f, **options):
        endpoint = options.pop('endpoint', rule)
        self.add_url_rule(rule, endpoint, f, **options)

    def __is_not_declare(self, path):
        return path not in self.__cache

    def __save_path(self, path):
        self.__cache[path] = True

    def link(self, rule: str, methods: List[str], validate: Validation = None):
        """
        Make a route
        :param rule: path as sub of folder
        :param methods: includes POST, GET, PUT, DELETE...
        :param validate: Validate form data after user request
        :return: Response data can be error or success
        """
        options = self.__makeOptions(methods)
        return self.__declare(rule, validate, **options)

    def get(self, path: str, validate: Validation = None):
        """
        Make a route as GET request
        :param path: path as sub of folder
        :param validate: Validate form data after user request
        :return: Response data can be error or success
        """
        return self.link(path, ["GET"], validate)

    def post(self, path: str, validate: Validation = None):
        """
        Make a route as POST request

        Ex:
        @app.post("registry", validate=Validation([
            KeyForm("email", str, Constraint(notnull=True, custom=[
                Validate(lambda x: str(x).__len__() != 0, "Email should not be null"),
                Validate(lambda x: str(x).__contains__("@"), "Email invalid format"),
            ])),
            KeyForm("password", str, Constraint(notnull=True, custom=[
                Validate(lambda x: str(x).__len__() >= 8, "Password too short"),
            ]))
        ]))
        def registry(self, req: Request, res: Response):
            return res.success('{}\'s profile registered'.format(req.form("email")))

        :param path: path as sub of folder
        :param validate: Validate form data after user request
        :return: Response data can be error or success
        """
        return self.link(path, ["POST"], validate)

    def routers(self, *routes: Controller):
        """
        Declare controllers

        Ex:
        app.routers(Authentication, User)

        :param routes: controller class
        """
        for route in routes:
            qpvdi.auto_single(route, route)
            self.__router_cache[route.__name__] = qpvdi.get(route)

    def __declare(self, rule, validate: Validation, **options):
        def decorate(f):
            f_class_name = self.__getTypeName(f)
            path = self.__make_path(f_class_name, rule)
            if self.__is_not_declare(path):
                def callback(*args, **kwargs):
                    f_self = self.__router_cache[f_class_name]
                    req = Request(kwargs, request)
                    res = Response

                    error = self.on_intercept(req, res)
                    if error is not None:
                        return error

                    if issubclass(type(f_self), Controller):
                        error = f_self.on_intercept(req, res)
                        if error is not None:
                            return error

                    if validate is not None:
                        error = validate.validate(req)
                        if error is not None:
                            return res.bad_request(error)
                    annotations = getattr(f, "__annotations__", None)
                    if annotations is None:
                        return f(f_self)
                    else:
                        params = []
                        for key in annotations:
                            if annotations[key].__name__ == Request.__name__:
                                params.append(req)
                            else:
                                params.append(res)
                        return f(f_self, *params)

                self.__link(path, callback, **options)
                self.__save_path(path)

        return decorate

    def on_intercept(self, req: Request, res) -> Any:
        """
        Intercept request before Controller intercept
        :param req: Request
        :param res: Response
        """
        pass

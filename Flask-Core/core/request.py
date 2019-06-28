from flask.json import jsonify


class Response(object):

    @staticmethod
    def bad_request(value):
        """
        Should make response data when validation error
        :param value: payload data
        :return: response as bad request code 400
        """
        return jsonify({
            "error": value
        }), 400

    @staticmethod
    def success(value):
        """
        :param value: payload data
        :return: response as success request code 200
        """
        return jsonify({
            "data": value
        }), 200

    @staticmethod
    def unauthor(value):
        """
        when token is not valid, or...
        :param value: payload data
        :return: response as un-authorize request code 401
        """
        return jsonify({
            "error": value
        }), 401


class Request(object):
    __query: dict
    __path: dict

    def __init__(self, path, request):
        self.__path = path
        self.__request = request

    def path(self, key):
        return self.__path.get(key, None)

    def query(self, key):
        return self.__request.args.get(key, None)

    def form(self, key):
        return self.__request.form.get(key, None)

    def files(self, key):
        return self.__request.files.get(key, None)

    def header(self, key):
        return self.__request.headers.get(key, None)

    def authorization(self):
        return self.__request.headers.get("Authorization", None)

    def is_post(self):
        return self.__request.method == "POST"

    def is_get(self):
        return self.__request.method == "GET"

    def is_put(self):
        return self.__request.method == "PUT"

    def is_delete(self):
        return self.__request.method == "DELETE"

    def on(self, get=None, post=None, put=None, delete=None):
        """
        Split request to other methods as GET, POST, PUT, DELETE

        Ex:

        @app.link("", ["GET", "POST"])
        def profile(self, req: Request, res: Response):
            return req.on(get=self.get_profile, post=self.post_profile)

        def get_profile(self, req: Request, res: Response):
            return res.success('{}\'s get profile and {}'.format(req.authorization()))

        def post_profile(self, req: Request, res: Response):
            return res.success('{}\'s post profile'.format(req.authorization()))

        :param get: GET method
        :param post: POST method
        :param put: PUT method
        :param delete: DELETE method
        :return: Response data as success or error
        """
        res = Response
        if self.is_post():
            return post(self, res)
        if self.is_put():
            return put(self, res)
        if self.is_delete():
            return delete(self, res)
        return get(self, res)

from typing import List

from core.request import Request


def parseInt(value):
    # noinspection PyBroadException
    try:
        return int(value)
    except Exception:
        return None


class Validate(object):
    def __init__(self, check_valid, error):
        self.check_valid = check_valid
        self.error = error


class Constraint(object):
    def __init__(self, notnull=False, custom: List[Validate] = None):
        self.type = type
        self.notnull = notnull
        self.custom = custom

    def validate(self, key, value):

        if self.notnull and value is None:
            return "{} can not be null".format(key)

        if self.custom is not None:
            for validate in self.custom:
                if validate.check_valid(value) is not True:
                    return validate.error

        return None

    def parse(self, value):
        if self.type == int:
            parseValue = parseInt(value)
            if parseValue is not None:
                return parseValue
        return value


class KeyInfo(object):
    def __init__(self, key, type=None, constraint: Constraint = None):
        self.key = key
        self.type = type
        self.constraint = constraint

    def is_type_valid(self, value):
        if self.type is None:
            return True
        if self.type == int and parseInt(value) is not None:
            return True
        if type(value) is self.type:
            return True
        return False

    def validate(self, value):
        if value is None:
            return "Not found field {}".format(self.key)

        if not self.is_type_valid(value):
            return "{} should be type of {}".format(self.key, self.type.__name__)

        if self.constraint is not None:
            return self.constraint.validate(self.key, self.constraint.parse(value))
        return None


class KeyQuery(KeyInfo):
    pass


class KeyForm(KeyInfo):
    pass


class KeyPath(KeyInfo):
    pass


class Validation(object):
    def __init__(self, keys: List[KeyInfo]):
        self.keys = keys

    def validate(self, req: Request):
        for key in self.keys:
            typeKey = type(key)
            if typeKey is KeyQuery:
                result = req.query(key.key)
            elif typeKey is KeyPath:
                result = req.path(key.key)
            else:
                result = req.form(key.key)
            valid = key.validate(result)
            if valid is not None:
                return valid
        return None

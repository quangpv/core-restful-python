from core.validation import KeyForm, Constraint, Validate


class Validator:
    email = KeyForm("email", str, Constraint(notnull=True, custom=[
        Validate(lambda x: str(x).__len__() != 0, "Email should not be null"),
        Validate(lambda x: str(x).__contains__("@"), "Email invalid format"),
    ]))

    password = KeyForm("password", str, Constraint(notnull=True, custom=[
        Validate(lambda x: str(x).__len__() >= 8, "Password too short"),
    ]))

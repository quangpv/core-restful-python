from src.api.auth import Auth
from src.api.user import User
from src.app.app_flask import app

app.routers(Auth, User)

if __name__ == "__main__":
    app.run(debug=True)

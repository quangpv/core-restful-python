from src.api.authentication import Authentication
from src.api.user import User
from src.app.app_cache import AppCache
from src.app.app_file import AppFile
from src.app.app_flask import app
from core.injector import singles

singles(AppCache, AppFile)

app.routers(Authentication, User)

if __name__ == "__main__":
    app.run(debug=True)

from qpvdi import component


@component(singleton=True)
class AppCache:
    def __init__(self):
        self.nameCached = "Cached"

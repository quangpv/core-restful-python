import functools
import typing
from typing import TypeVar, Generic

T = TypeVar('T')


class Bean(Generic[T]):
    __value = None

    def __init__(self, invokable, is_single):
        self.__invokable = invokable
        self.__single = is_single

    def get_instance(self) -> T:
        if self.__single:
            if self.__value is None:
                self.__value = self.__invokable()
            return self.__value
        return self.__invokable()


class __Injector:
    def __init__(self):
        self.__cache = {}

    def put(self, genType: Generic[T], bean: Bean):
        self.__cache[genType.__name__] = bean

    def get(self, genType: Generic[T]) -> Bean:
        return self.__cache[genType.__name__]


__injector = __Injector()


def singles(*args: Generic[T]):
    """
    Declare Class will be instance as singleton

    Ex:
    singles(AppCache, AppFile)

    :param args: Classes
    """
    for type in args:
        __injector.put(type, Bean[T](lambda: type(), True))


def inject(f):
    """
    Annotation to get instance when function be called

    Ex:
    @inject
    def app_cache(self) -> AppCache: pass

    :param f: function mark inject
    :return: Singleton or new instance
    """

    @functools.wraps(f)
    def callF(*args):
        returnType = typing.get_type_hints(f)['return']
        return __injector.get(returnType).get_instance()

    return callF


def get(genType):
    """
    Lazy get instance of type

    Ex:
    def __init__(self):
        app_cache = get(AppCache)

    :param genType:
    :return: Singleton or new instance
    """
    return __injector.get(genType).get_instance()

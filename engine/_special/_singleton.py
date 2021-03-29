class Singleton:
    __slots__ = ()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def exists_instance(cls):
        return cls._instance is not None

    @classmethod
    def create_instance(cls, *args, **kwargs):
        cls(*args, **kwargs)

    @classmethod
    def instance(cls):
        return cls._instance

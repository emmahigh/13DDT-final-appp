class UserSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
            cls._user = None
        return cls._instance

    def set_user(self, user):
        self._user = user

    def get_user(self):
        return self._user
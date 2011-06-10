class APIError(Exception):
    pass


class RealmNotFound(APIError):
    pass

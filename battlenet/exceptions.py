class APIError(Exception):
    pass

class CharacterNotFound(APIError):
    pass

class GuildNotFound(APIError):
    pass

class RealmNotFound(APIError):
    pass

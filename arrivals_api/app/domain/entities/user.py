from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User:
    def __init__(self, id: int, username: str, hashed_password: str, role: str):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.role = role

    def verify_password(self, plain_password: str) -> bool:
        """Verifica si la contraseña proporcionada coincide con la almacenada."""
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Genera un hash para la contraseña proporcionada."""
        return pwd_context.hash(plain_password)

from backend.app.database import Base, engine
from backend.app.models import Release


def create_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")
from .db import init_engine
from .models import Base
from .config import Settings


def migrate():
    settings = Settings()
    init_engine(settings.DATABASE_URL)
    engine = Base.metadata.bind or Base.metadata.create_all  # type: ignore
    # create all tables
    from sqlalchemy import create_engine as _ce
    engine = _ce(settings.DATABASE_URL)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    migrate()
    print("migrated")
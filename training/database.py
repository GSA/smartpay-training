from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from training.config import settings


# cloud.gov provides the URI in postgres:// format, but SQLAlchemy requires
# PostgreSQL URIs to use postgresql://
db_uri = settings.DB_URI.replace("postgres://", "postgresql://")

engine = create_engine(db_uri)
Session = sessionmaker(engine)

# TODO: Alembic migrations
from training.models import Base
Base.metadata.create_all(engine)

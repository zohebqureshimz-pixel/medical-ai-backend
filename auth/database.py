import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "medical_ai.db").replace("\\", "/")
DEFAULT_SQLITE_DB = f"sqlite:///{db_path}"

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = DEFAULT_SQLITE_DB

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

def create_app_engine(url):
    if url.startswith("sqlite"):
        eng = create_engine(
            url,
            connect_args={"check_same_thread": False},
            pool_pre_ping=True
        )

        @event.listens_for(eng, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

        return eng
    else:
        try:
            eng = create_engine(
                url,
                pool_pre_ping=True,
                pool_recycle=300
            )
            # Test connection
            with eng.connect() as conn:
                pass
            print("[Database] Successfully connected to PostgreSQL.")
            return eng
        except Exception as e:
            print(f"[Database Error] Failed to connect to PostgreSQL ({e}). Falling back to SQLite.")
            return create_app_engine(DEFAULT_SQLITE_DB)


engine = create_app_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
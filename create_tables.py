from auth.database import engine, Base
from auth.models import User, Document


Base.metadata.create_all(
    bind=engine
)

print("Tables created successfully")
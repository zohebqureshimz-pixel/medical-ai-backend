import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.database import Base, engine
from auth.models import User, Document

Base.metadata.create_all(bind=engine)

print("Database created successfully!")
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://${{secrets.DATABASE_USERNAME}}:${{secrets.DATABASE_PASSWORD}}@${{secrets.DATABASE_HOST_NAME}}:${{secrets.DATABASE_PORT}}/${{secrets.DATABASE_NAME}}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# DB connection for Raw SQL
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapibackend",
#             user="root",
#             password="password",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)

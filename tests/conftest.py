from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.         DATABASE_HOST_NAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user_one(client):
    user_data = {"email": "testuser_1@gmail.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_two(client):
    user_data = {"email": "testuser_2@gmail.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user_one):
    return create_access_token({"user_id": test_user_one["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user_one, session, test_user_two):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user_one["id"],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user_one["id"],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user_one["id"],
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user_one["id"],
        },
        {
            "title": "fifth title",
            "content": "fifth content",
            "owner_id": test_user_two["id"],
        },
    ]

    def create_posts(post):
        return models.Post(**post)

    posts = list(map(create_posts, posts_data))
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

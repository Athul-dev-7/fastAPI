from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts")
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)

    def validate(post):
        return schemas.PostVoteResponse(**post)

    posts_map = map(validate, response.json())
    posts_list = list(posts_map)
    sorted_list = sorted(posts_list, key=lambda x: x.Post.id)

    for index, post in enumerate(test_posts):
        assert sorted_list[index].Post.id == post.id
        assert sorted_list[index].Post.title == post.title
        assert sorted_list[index].Post.content == post.content
        assert sorted_list[index].Post.owner_id == post.owner_id


def test_unauthorized_get_all_posts(client):
    response = client.get("/posts")
    assert response.status_code == 401


def test_unauthorized_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_one_non_existing_post(authorized_client):
    response = authorized_client.get("/posts/5454")
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    post = schemas.PostVoteResponse(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("This is my first title", "Awesome content", True),
        ("This is my second title", "second content", False),
        ("This is my third title", "third content", False),
    ],
)
def test_create_post(authorized_client, test_user_one, title, content, published):
    response = authorized_client.post(
        "/posts", json={"title": title, "content": content, "published": published}
    )
    assert response.status_code == 201
    created_post = schemas.PostResponse(**response.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user_one["id"]


@pytest.mark.parametrize(
    "title, content",
    [
        ("This is my first title", "Awesome content"),
        ("This is my second title", "second content"),
        ("This is my third title", "third content"),
    ],
)
def test_create_post_default_published_to_true(
    authorized_client, test_user_one, title, content
):
    response = authorized_client.post(
        "/posts",
        json={"title": title, "content": content},
    )
    assert response.status_code == 201
    created_post = schemas.PostResponse(**response.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == True
    assert created_post.owner_id == test_user_one["id"]


def test_unauthorized_user_create_posts(client):
    response = client.post(
        "/posts",
        json={"title": "test title", "content": "test content"},
    )
    assert response.status_code == 401


def test_unauthorized_user_delete_posts(client, test_posts):
    response = client.delete(
        f"/posts/{test_posts[0].id}",
    )
    assert response.status_code == 401


def test_delete_posts(authorized_client, test_posts):
    response = authorized_client.delete(
        f"/posts/{test_posts[0].id}",
    )
    assert response.status_code == 204


def test_delete_one_non_existing_post(authorized_client, test_posts):
    response = authorized_client.delete(
        f"/posts/{test_posts[4].id}",
    )
    assert response.status_code == 403


def test_update_post(authorized_client, test_posts, test_user_one):
    data = {
        "title": "updated title",
        "content": "updated first content",
        "id": test_user_one["id"],
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**response.json())
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.id == data["id"]


def test_update_other_user_post(authorized_client, test_posts, test_user_two):
    data = {
        "title": "updated title",
        "content": "updated first content",
        "id": test_user_two["id"],
    }
    response = authorized_client.put(f"/posts/{test_posts[4].id}", json=data)
    assert response.status_code == 403


def test_unauthorized_user_update_posts(client, test_posts):
    response = client.put(
        f"/posts/{test_posts[0].id}",
    )
    assert response.status_code == 401


def test_update_non_existing_post(authorized_client, test_posts, test_user_two):
    data = {
        "title": "updated title",
        "content": "updated first content",
        "id": test_user_two["id"],
    }
    response = authorized_client.put("/posts/58788", json=data)
    assert response.status_code == 404

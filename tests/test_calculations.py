import pytest
from app.calculations import add, sub, mul


@pytest.mark.parametrize(
    "num1,num2,expected",
    [
        (3, 2, 5),
        (1, 2, 3),
        (3, 3, 6),
        (3, 7, 10),
        (4, 3, 7),
    ],
)
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

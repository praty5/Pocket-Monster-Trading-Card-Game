import pytest
from project import  vault, save,star

def main():
    test_save()
    test_vault()
    test_star()

def test_save():
    assert save('y') == 0
    assert save('n') == None
    assert save('k') == None


def test_vault():

    assert vault(30.0) == 30.00
    vault(20.0)
    assert vault(15.0) == 65.00
    assert vault(-15.00) == 50.00


def test_star():
    assert star(2) == "   ⭐⭐     "
    assert star(1) == "    ⭐      "
    assert star(3) == "  ⭐⭐⭐   "
    with pytest.raises(ValueError):
        assert star(6)

if __name__ == "__main__":
    main()

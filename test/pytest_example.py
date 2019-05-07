def test_pass():
    print("Test 1")


def test_equal():
    actual = [1, 2, 3]
    expected = [1, 2, 3]
    print(f"actual is {actual}")
    assert expected == actual


class TestSomeStuff():
    def test_three(selfs):
        assert {1, 2, 2} == {1, 2}

    def test_four(self):
        assert [1, 2] == [1, 2]
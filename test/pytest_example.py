def test_pass():
    print("Test 1")


def test_equal():
    actual = [1, 2, 3]
    expected = [1, 2, 3]
    print(f"actual is {actual}")
    assert expected == actual



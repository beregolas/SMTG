from SMTG import _find_all


def test_empty():
    assert _find_all("", "a") == []


def test_no_match():
    assert _find_all("abc", "d") == []


def test_no_match_2():
    assert _find_all("abc", "ac") == []


def test_no_match_3():
    assert _find_all("abc", "abcd") == []


def test_trivial_match():
    assert _find_all("abcde", "") == [0, 1, 2, 3, 4]


def test_trivial_match_2():
    assert _find_all("a", "a") == [0]


def test_trivial_match_3():
    assert _find_all("ab", "ab") == [0]


def test_trivial_match_4():
    assert _find_all("  this is a test", "this is a test") == [2]


def test_match():
    assert _find_all("This is a normal text and a good text. We try to find all a's in this text!", "a") == [8, 14, 22,
                                                                                                             26, 54, 58]


def test_match_2():
    assert _find_all("This is a normal text and a good text. We try to find all instances of a certain word in this "
                     "text!", "text") == [17, 33, 94]


def test_if():
    assert _find_all("This is a template text with an if statement {? 1 == 1 | that is true ?}", "{?") == [45]


def test_if_2():
    assert _find_all(
        "This is a template text with an if statement {? 1 == 1 | that is true ?} {? 1 == 2 | that is false ?}",
        "{?") == [45, 73]

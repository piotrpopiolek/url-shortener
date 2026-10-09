from shortener.codes import CODE_CHARACTERS, CODE_LENGTH, generate_code, is_valid_code


def test_generate_code_has_default_length() -> None:
    code = generate_code()
    assert len(code) == CODE_LENGTH


def test_generate_code_respects_custom_length() -> None:
    code = generate_code(10)
    assert len(code) == 10


def test_generate_code_uses_only_alphabet_characters() -> None:
    code = generate_code()
    assert all(char in CODE_CHARACTERS for char in code)


def test_generate_code_returns_different_values() -> None:
    codes = {generate_code() for _ in range(100)}
    assert len(codes) > 1


def test_is_valid_code_returns_true_for_valid_code() -> None:
    code = generate_code()
    assert is_valid_code(code)


def test_is_valid_code_rejects_wrong_length() -> None:
    assert not is_valid_code("12345678")
    assert not is_valid_code("1234567890")
    assert not is_valid_code("12345678901")


def test_is_valid_code_rejects_characters_outside_alphabet() -> None:
    assert not is_valid_code("abc\\1!@")
    assert not is_valid_code("ABC_123")
    assert not is_valid_code("abc-123")

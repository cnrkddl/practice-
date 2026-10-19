class CalculatorError(Exception):
    pass

def _check(a, b):
    for x in (a, b):
        if not isinstance(x, (int, float)):
            raise CalculatorError(f"숫자가 아닙니다: {x!r}")

def add(a, b):
    _check(a, b)
    return a + b


def subtract(a, b):
    _check(a, b)
    return a - b


def multiply(a, b):
    _check(a, b)
    return a * b


def divide(a, b):
    _check(a, b)
    if b == 0:
        raise CalculatorError("0으로 나눌 수 없습니다")
    return a / b


if __name__ == "__main__":
    print("3 + 5 =", add(3, 5))
    print("10 - 4 =", subtract(10, 4))
    print("6 * 7 =", multiply(6, 7))
    print("9 / 2 =", divide(9, 2))
    try:
        divide(1, 0)  # 0으로 나누기 → 실패해야 정상
    except CalculatorError as e:
        print("계산 실패:", e)
    try:
        add("3", 5)  # 문자열 입력 → 실패해야 정상
    except CalculatorError as e:
        print("계산 실패:", e)


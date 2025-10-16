def match_k(k):
    """Returns a function that checks if digits k apart match.

    >>> match_k(2)(1010)
    True
    >>> match_k(2)(2010)
    False
    >>> match_k(1)(1010)
    False
    >>> match_k(1)(1)
    True
    >>> match_k(1)(2111111111111111)
    False
    >>> match_k(3)(123123)
    True
    >>> match_k(2)(123123)
    False
    """
    divisor = 10 ** k
    def check(x):
        while x // divisor > 0:
            end = x % divisor
            rest = x // divisor
            if rest % divisor != end:
                return False
            x = rest
        return True
    return check
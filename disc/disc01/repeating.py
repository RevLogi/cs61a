def repeating(t, n):
    """Return whether t digits repeat to form positive integer n.

    >>> repeating(1, 6161)
    False
    >>> repeating(2, 6161)  # repeats 61 (2 digits)
    True
    >>> repeating(3, 6161)
    False
    >>> repeating(4, 6161)  # repeats 6161 (4 digits)
    True
    >>> repeating(5, 6161)  # there are only 4 digits
    False
    """
    divisor = pow(10, t)
    if pow(10, t-1) > n:  # make sure n has at least t digits
        return False
    end = n % divisor
    rest = n // divisor
    while rest:
        if rest % divisor != end:
           return False
        rest = rest // divisor
    return True
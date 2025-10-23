class Store:
    """A Store selling programs has branches forming a tree of Stores.
    >>> north, south = Store (['Cats', 'Ants']), Store (['Cats', 'Cats', 'Hog'])
    >>> east, west = Store (['Cats', 'Hog', 'Hog'], [north, south]), Store (['Cats', 'Cats', 'Ants'])
    >>> main Store (['Ants', 'Ants', 'Hog'], [east, west])
    >>> east.copies ('Cats')
    4
    # 1 in north, 2 in south, 1 in east
    >>> main.copies ('Ants')
    4
    #2 in main, 1 in north, 1 in west
    >>> main.add_to (1) ('Ants') # Add 'Ants' to the inventory of west, the branch of main at index 1
    >>> [main.copies ('Ants'), west.copies ('Ants')] # increased copies in both main and west
    [5, 2]
    """
    def _init__(self, programs, branches=[]):
        assert all([isinstance (b, Store) for b in branches])
        self.branches = branches
        self.inventory = programs
    def copies (self, s):
        """Return the number of times s (string) appears in all inventories of this tree."""
        return sum([p for p in self.inventory if p == s] + [b.copies(s) for b in self.branches])

    def add_to(self, k):
        """Return a function that appends a string to the inventory of the branch at index k."""
        return self.branch[k].inventory.append

def semiperfect (n):
    """Return whether positive integer n is a sum of some (or all) of its proper divisors.
    >>> [k for k in range(1, 40) if semiperfect(k)]
    [6, 12, 18, 20, 24, 28, 30, 36]
    """
    def f(s, d):
        if s == 0:
            return True
        if d >= n:
            return False
        if n % d == 0 and f(s - d , d+1):
            return True
        return f(s, d + 1)
    return f(n, 1)

def subsums (s, n):
    """Yield all sublists of s that sum to n.
    >>> list (subsums ([1, 2, 3, 6, 9], 18))
    [[1, 2, 6, 9], [3, 6, 9]]
    >>> list (subsums ([1, 2, 3, 4, 6], 16))
    [[1, 2, 3, 4, 6]]
    >>> list (subsums ([1, 2, 3, 4, 6, 8, 12], 12))
    [[1, 2, 3, 6], [1, 3, 8], [2, 4, 6], [4, 8], [12]]
    """
    if s:
        if s == n:
            yield [n]
        for t in subsums(s[1:], n - s[0]):
            yield s[:1] + t
        yield from subsums(s[1:], n)

def semisums(n):
    """Return a list of all lists (with no repeats) of
    proper divisors of n that sum to n.
    >>> semisums (22)
    []
    # 22 is not semiperfect, so there are no sums.
    >>> semisums (30)
    [[1, 3, 5, 6, 15],
    # 30 is semiperfect. It has three different sums.
    [2, 3, 10, 15], [5, 10, 15]]
    """
    return list(subsums([k for k in range(1, n) if n % k == 0], n))

def primitive_semiperfect (n):
    """Return whether n is semiperfect and has no semiperfect proper divisors.
    >>> [k for k in range(1, 300) if primitive_semiperfect (k)]
    [6, 20, 28, 88, 104, 272]
    """
    return semiperfect(n) and not any(map(semiperfect, filter(lambda k: n % k == 0, range(0, n))))

def longer(s, t):
    """Return the longer linked list, s or t. (Same length? return s.)
    >>> longer(Link(2, Link(3)), Link.empty)
    Link(2, Link(3))
    >>> longer(Link(2, Link(3)), Link(4, Link(5)))
    Link(2, Link(3))
    >>> longer(Link(2, Link(3)), Link(4, Link(5, Link(6, Link(7)))))
    Link(4, Link(5, Link(6, Link(7))))
    >>> longer(Link.empty, Link.empty) is Link.empty
    True
    """
    a, b = s, t
    while b is not Link.empty:
        if a is Link.empty:
            return t
        a, b = a.rest, b.rest
    return s

def longest(s, n):
    """Return the longest sublist of s that sums to n or less.
    >>> longest(Link(5, Link(1, Link(3, Link(4, Link(2, Link(7)))))), 7)
    Link(1, Link(3, Link(2)))
    >>> longest(Link(5, Link(1, Link(3, Link(4, Link(2, Link(7)))))), 70)
    Link(5, Link(1, Link(3, Link(4, Link(2, Link(7))))))
    >>> longest(Link(3, Link(4, Link(5))), 2) is Link.empty
    True
    """
    if s is Link.empty:
        return s
    t = longest(s.rest, n)
    if s.first <= n:
        return longer(Link(s.first, longest(s.rest, n - s.first)), t)
    else:
        return t

def climb(t, f):
    if t.is_leaf():
        return [t.label]
    return [t.label] + climb(max(t.branches, key=f), f)

def max_path(t, g):
    """Return the path s from the root of t to a leaf for which g(s) is largest.
    >>> scare = Tree(0, [Tree(4), Tree(5, [Tree(10)]), Tree(2)])
    >>> crow = Tree(4, [Tree(5), Tree(9, [scare, Tree(7, [Tree(6)])]), Tree(8)])
    >>> max_path(crow, lambda p: -p[-1]) # The path to the smallest leaf
    [4, 9, 0, 2]
    >>> max_path(crow, len) # The longest path
    [4, 9, 0, 5, 10]
    >>> max_path(crow, lambda p: -abs(p[0]-p[-1])) # To the leaf closest in value to the root
    [4, 9, 0, 4]
    """
    x = [t.label] # You can use x instead of [t.label] to shorten your answer!
    return climb(t, lambda b: ______ )

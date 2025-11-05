class Library:
    """A library with one copy of each title that can be checked out.
    >>> cs = Library(['Composing Programs', 'Python Docs', 'Berkeley Academic Guide'])
    >>> bs = [cs.checkout('Composing Programs'), cs.checkout('Python Docs')]
    >>> cs.checkout('Composing Programs')
    Composing Programs is checked out
    >>> bs[0].bring_back()
    # This time, no Book is returned
    >>> cs.checkout('Composing Programs').title # This time, a Book is returned
    'Composing Programs'
    """
    def __init__(self, titles):
        self.books = {t: Book(t, self) for t in titles}
        self.out = []# A list of Book objects

    def checkout(self, title):
        assert title in self.books, title + " isn't in this library' collection"
        book = self.books[title]
        if book not in self.out:
            self.out.append(book)
            return book
        else:
            print(book, 'is checked out')

class Book:
    def __init__(self, title, library):
        self.title = title # a string
        self.library = library # a Library object
    def bring_back(self):
        self.library.out.remove(self)
    def __str__(self):
        return self.title

def fit (total, n):
    """Return whether there are n positive perfect squares that sums to total.
    >>> [fit(4, 1), fit(4, 2), fit(4, 3), fit(4, 4)] # 1*(2*2) for n=1 4*(1*1) for n=4
    [True, False, False, True]
    >>> [fit(12, n) for n in range(3, 8)] # 3*(2*2), 3*(1*1)+3*3, 4*(1*1)+2*(2*2)
    [True, True, False, True, False]
    >>> [fit(32, 2), fit(32, 3), fit(32, 4), fit(32, 5)] # 2*(4*4), 3*(1*1)+2*2+5*5
    [True, False, False, True]
    """
    def f(total, n, k):
        if total == 0 and n == 0:
            return True
        elif n == 0: 
            return False
        else:
            return f(total - k * k, n - 1, k) or f(total, n, k + 1)
    return f(total, n, 1)

def squares (total, k):
    """Yield the ways in which perfect squares greater or equal to k*k sum to total.
    >>> list(squares(10, 1))
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [4, 1, 1, 1, 1, 1, 1], [4, 4, 1, 1], [9, 1]]
    # All lists of perfect squares that sum to 10
    >>> list(squares(20, 2))
    [[4, 4, 4, 4, 4], [16, 4]]
    # Only use perfect squares greater or equal to 4 (2*2).
    """
    assert total > 0 and k > 0
    if total == k * k:
        yield [k * k]
    elif total > k * k:
        for s in squares(total - k * k, k)
            yield s + [k * k]
        yield from squares(total, k+1)

def only_paths (t, n):
    """Return a Tree with only the nodes of t along paths from the root to a leaf of t
    for which the node labels of the path sum to n. If no paths sum to n, return None.
    >>> print (only_paths (Tree (5, [Tree (2), Tree (1, [Tree(2)]), Tree (1, [Tree(1)])]), 7))
    5
      2
      1
        1
    >>> t = Tree (3, [Tree (4), Tree (1, [Tree (3, [Tree (2)]), Tree(2, [Tree (1)]), Tree (5), Tree(3)])])
    >>> print (only_paths (t, 7))
    3
      4
      1
        2
          1
        3
    >>> print (only_paths (t, 9))
    3
      1
        3
          2
        5
    >>> print (only_paths (t, 3))
    None
    """
    if t.is_leaf and t.label == n:
        return t
    new_branches = [only_paths(b, n - t.label) for b in t.branches]
    
    if any(new_branches):
        return Tree(t.label, [b for b in new_branches if b is not None])

only_paths = (lambda f: lambda t, n: only_paths(t, n - 1))(only_paths)
def only_long_paths(t, n):
    """Return a Tree with only the nodes of t along paths from the root to a leaf of t
    for which the sum of node labels plus the length of the path is n.
    >>> example = Tree(5, [Tree(3), Tree(1, [Tree(2)]), Tree(1, [Tree(1)])])
    >>> only_long_paths(example, 10) # Result has paths 5-3 (length 2) and 5-1-1 (length 3)
    Tree(5, [Tree(3), Tree(1, [Tree(1)])])
    """
    return only_paths(t, n)

def after(s, a, b):
    """Return whether b comes after a in linked list s.
    >>> t = Link(3, Link(6, Link(5, Link(4))))
    >>> after(t, 6, 4)
    True
    >>> after(t, 4, 6)
    False
    >>> after(t, 6, 6)
    False
    """
    def find(s, n, f):
        if s == Link.empty:
            return False
        elif s.first == n:
            return f(s.rest)
        else:
            return find(s.rest, n, f)
    return find(s, a, lambda rest: find(rest, b, lambda _: True))

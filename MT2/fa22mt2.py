def make_test_dice(outcomes):
    """Return an infinite iterator that cycles through the elements of outcomes.
    >>> dice = make_test_dice ([1, 2, 3])
    >>> next (dice)
    1
    >>> next (dice)
    2
    >>> next (dice)
    3
    >>> next (dice)
    1
    >>> next (dice)
    2
    >>> next (dice)
    3
    >>> next (dice)
    1
    >>> next(dice)
    2
    """
    outcomes = list (outcomes)
    while True:
        for i in outcomes :
            yield i

def roll_dice(num_rolls, dice):
    """Return the number of points scored by rolling dice num_rolls times.
    >>> dice = make_test_dice ([6, 6, 6, 6, 6, 1])
    >>> roll_dice (5, dice) # 6, 6, 6, 6, 6
    30
    >>> roll_dice(5, dice) # 1, 6, 6, 6, 6
    1
    >>> roll_dice(2, dice) # 6, 1
    1
    >>> roll_dice(10, make_test_dice([2, 4, 3])) # 2, 4, 3, 2, 4, 3, 2, 4, 3, 2
    29
    """
    rolls = [next(dice) for _ in range(num_rolls)]
    if 1 in rolls :
        return 1
    return sum(rolls)

def is_hydra(t):
    """Return True if Tree instance t properly represents a hydra and False otherwise.
    >>> is_hydra (Tree (1))
    True
    >>> is_hydra (Tree (2, [Tree (1), Tree (1)]))
    True
    >>> is_hydra (Tree (3, [Tree (1)
    , Tree (2)]))
    # Wrong leaf label
    False
    >>> is_hydra (Tree (3
    , [Tree (1)
    , Tree (1) ]))
    # Wrong root label
    False
    >>> is_hydra (Tree (3, [Tree (3, [Tree (1), Tree (1)]), Tree(1)))) # Wrong node label below root
    False
    >>>is_hydra(lerna) # lerna the six-headed hydra is defined above
    True
    """
    if t.is_leaf():
        return t.label == 1
    if len(t.branches) != 2:
        return False
    return (t.label == sum[b.label for b in t.branches]) and all(is_hydra(b) for b in t.branches) 

def chop_head(hydra, n):
    """
    >>> lerna = Tree(1)
    >>> chop_head (lerna, 1) # Note that n is 1-indexed
    >>> chop_head(lerna, 1)
    >>> chop_head(lerna, 3)
    >>> chop_head (lerna, 1)
    >>> chop_head (lerna, 3)
    >>> lerna
    Tree (6, [Tree (4, [Tree (2, [Tree (1), Tree(1))), Tree(2, [Tree (1), Tree(1)])]), Tree(2, [Tree (1), Tree(1)])])
    >>> chop_head (lerna, 2)
    >>> lerna
    Tree (7, [Tree (5, [Tree (3, [Tree (1), Tree(2, [Tree (1), Tree (1)])]), Tree (2, [Tree (1), Tree(1)])]), Tree(2, [Tree (1), Tree (1)])])
    """
    assert is_hydra (hydra)
    assert n > 0 and n <= hydra.label
    if hydra.is_leaf():
        hydra.label = 2
        hydra.branches = [Tree(1), Tree(1)]
        return
    hydra.label += 1
    left, right = hydra.branches
    if left.label >= n:
        chop_head (left, n)
    else:
        chop_head(right, n - left.label)

def count_subsets(s):
    """
    >>> count_subsets([25, 50, 75, 100, 125, 150]) # [25, 75], [100]
    2
    >>> count_subsets([25, 50, 25, 75]) # [25, 75] (first 25), [25, 75] (second 25), [25, 50, 25]
    3
    >>> count_subsets(list(range(1,10000)))
    444793
    """
    def helper(sum_so_far, index):
        if index == len(s):
            if sum_so_far == 100:
                return 1
            return 0
        return helper(sum_so_far + s[index], index + 1) + helper(sum_so_far, index + 1]
    return helper(0,0)

class Graph:
    "A graph."
    def __init__(self, nodes):
        self.nodes = nodes
        self.edges = []
    def add_edge(self, source, destination):
        "Add an edge from source to destination."
        if source >= 0 and source < self.nodes:
            if destination >= 0 and destination < self.nodes:
                if (source, destination) not in self.edges:
                    self.edges.append((source, destination))
    def destinations(self, source):
        "Returns a list of all destinations of the given node."
        assert source >= 0 and source < self.nodes
        return [i[1] for i in self.edges if i[0] == source]
    def has_path(self, source, destination):
        "Returns True if a path exists from source to destination, and False otherwise."
        ... # The implementation of this method is omitted, but assume it works.
        
def compose_path(funcs, x, y, maxval):
    """
    >>> f, g, h = lambda x: 2*x-1, lambda x: x*x+1, lambda x: x-4
    >>> #3->10->6->11->122->118->114->110->106->102->98
    >>> # g h f g h h h h h h
    >>> compose_path([f, g, h], 3, 98, 1000)
    True
    >>> #The above path hits 122, and no other path exists to get from 3 to 98
    >>> compose_path([f, g, h], 3, 98, 122)
    False
    >>> [i for i in range(100) if compose_path([h], 10, i, 100)]
    [2, 6, 10]
    """
    g = Graph(maxval)
    for f in funcs:
        for j in range(maxval):
            g.add_edge(j, f(j))
    return g.has_path(x, y)

def tree_to_graph(tree):
    def helper(tree, op1, op2):
        a = op1()
        return op2(a, [helper(b, op1, op2) for b in tree.branches]) or a
    num_nodes = helper(tree, lambda: 1, lambda a, b: a + sum(b))
    g = Graph(num_nodes)
    b = iter(range(num_nodes))
    helper(tree, lambda: next(b), lambda a, b: (g.add_edge(a, i) for i in b))
    return g

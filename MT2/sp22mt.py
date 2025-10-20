def make_necklace(beads, length):
    """
    Returns a linked list where each value is taken from the BEADS list,
    repeating the values from the BEADS list until the linked list has reached
    LENGTH. You can assume that LENGTH is greater than or equal to 1, there is
    at least one bead in BEADS, and all beads are string values.
    >>> wavy_ats = make_necklace(["~", "@"], 3)
    >>> wavy_ats
    Link('~', Link('@', Link('~')))
    >>> print(wavy_ats)
    <~ @ ~>
    >>> wavy_ats2 = make_necklace(["~", "@"], 4)
    >>> print(wavy_ats2)
    <~ @ ~ @>
    >>> curly_os = make_necklace(["}", "O", "{"], 9)
    >>> print(curly_os)
    <} O { } O { } O {>
    """
    if length == 0:
        return Link(beads[0])
    return Link(beads[0], make_necklace(beads[1:] + beads[:1], length - 1))

def filetree_to_dict(t):
    """
    >>> filetree_to_dict(Tree("hw05.py"))
    {"hw05.py": "FILE"}
    >>> filetree = Tree("C:", [Tree("Documents", [Tree("hw05.py")]), Tree("pwd.txt")])
    >>> filetree_to_dict(filetree)
    {"C:": {"Documents": {"hw05.py": "FILE"}, "pwd.txt": "FILE"}}
    """
    res = {}
    if t.is_leaf():
        res[t.label] = FILE
    else:
        nested = {}
        for branch in t.branches:
            nested[branch.label] = filetree_to_dict(branch)[branch.label]
        res[t.label] = nested
    return res

def flower_keeper(t):
    """
    Mutates the tree T to keep only paths that end in flowers ('V').
    If a path consists entirely of stems ('|'), it must be pruned.
    If T has no paths that end in flowers, the root node is still kept.
    You can assume that a node with a flower will have no branches.
    >>> one_f = Tree('|', [Tree('|', [Tree('|'), Tree('|')]), Tree('|', [Tree('V'), Tree('|')])])
    >>> print(one_f)
    |
    |
    |
    |
    |
    V
    |
    >>> flower_keeper(one_f)
    >>> one_f
    Tree('|', [Tree('|', [Tree('V')])])
    >>> print(one_f)
    |
    |
    V
    >>> no_f = Tree('|', [Tree('|', [Tree('|'), Tree('|')]), Tree('|', [Tree('|'), Tree('|')])])
    >>> flower_keeper(no_f)
    >>> no_f
    Tree('|')
    >>> just_f = Tree('V')
    >>> flower_keeper(just_f)
    >>> just_f
    Tree('V')
    >>> two_f = Tree('|', [Tree('|', [Tree('V')]), Tree('|', [Tree('|'), Tree('V')])])
    >>> flower_keeper(two_f)
    >>> two_f
    Tree('|', [Tree('|', [Tree('V')]), Tree('|', [Tree('V')])])
    """
    for b in t.branches:
        flower_keeper(b)
    t.branches = [b for b in t.branches if b == 'V' or b.branches]

class HoopPlayer:
    def __init__(self, strategy):
        """Initialize a player with STRATEGY, and a starting SCORE of 0. The
        STRATEGY should be a function that takes this player's score and a list
        of other players' scores.
        """
        self.strategy = strategy
        self.score = 0

class HoopDice:
    def __init__(self, values):
        """Initialize a dice with possible values VALUES, and a starting INDEX
        of 0. The INDEX indicates which value from VALUES to return when the
        dice is rolled next.
        """
        self.values = values
        self.index = 0

    def roll(self):
        """
        Roll this dice. Advance the index to the next step before returning."""
        value = self.values[self.index]
        self.index = (self.index + 1) % len(self.values)
        return value
    
class HoopGame:
    def __init__(self, players, dice, goal):
        """Initialize a game with a list of PLAYERS, which contains at least one
 HoopPlayer, a single HoopDice DICE, and a goal score of GOAL.
 """
        self.players = players
        self.dice = dice
        self.goal = goal

    def next_player(self):
        """Infinitely yields the next player in the game, in order.
 >>> player_gen = game.next_player()
 >>> next(player_gen) is player1
 True
 >>> next(player_gen) is player3
 False
 >>> next(player_gen) is player3
 True
 >>> next(player_gen) is player1
 True
 >>> next(player_gen) is player2
 True
 >>> new_player_gen = game.next_player()
 >>> next(new_player_gen) is player1
 True
 >>> next(player_gen) is player3
 True
 """
        yield from self.players
        yield from self.next_player()

    def get_scores(self):
        """Collects and returns a list of the current scores for all players
 in the same order as the SELF.PLAYERS list.
 """
        # Implementation omitted.
    
    def get_scores_except(self, player):
        """Collects and returns a list of the current scores for all players
 except PLAYER.
     >>> game.get_scores_except(player2)
     [0, 0]
     """
        return [get_scores(pl) for pl in self.players if pl is not player]

    def roll_dice(self, num_rolls):
        """Simulate rolling SELF.DICE exactly NUM_ROLLS > 0 times. Return sum of
 the outcomes unless any of the outcomes is 1. In that case, return 1.
 >>> game.roll_dice(4)
 20
 """
        outcomes = [self.dice.roll() for x in range(num_rolls)]
        ones = [outcome == 1 for outcome in outcomes]
        return 1 if any(ones) else sum(outcomes)

    def play(self):
        """Play the game while no player has reached or exceeded the goal score.
 After the game ends, return all players' scores.
 >>> game.play()
 [20, 10, 60]
 """
        player_gen = self.next_player()
        while max(self.get_scores()) < self.goal:
            player = next(player_gen)
            other_scores = self.get_scores_except(player)
            num_rolls = player.strategy(player.score, other_scores)
            outcome = self.roll_dice(num_rolls)
            player.score += outcome
        return self.get_scores()

class BrokenHoopDice(HoopDice):
    def __init__(self, values, when_broken):
        super().__init__(values)
        self.when_broken = when_broken
        self.is_broken = False
    
    def roll(self):
        """
 >>> broken = BrokenHoopDice([5, 6, 7], 11)
 >>> broken.roll()
 5
 >>> [broken.roll() for _ in range(6)]
 [11, 6, 11, 7, 11, 5]
 """
        if self.is_broken:
            self.is_broken = not self.is_broken
            return self.when_broken
        else:
            self.is_broken = not self.is_broken
            return super().roll()    

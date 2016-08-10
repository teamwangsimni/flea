import itertools


class Direction(object):
    """Class that encapsulates directions and provides direction compositions
    with elementary operator overloadings.

    """

    # A tuple of elementary direction names
    __TOP__, __BOTTOM__, __LEFT__, __RIGHT__, __NONE__ = \
        __ELEMENTARY_DIRECTIONS__ = \
        ('TOP', 'BOTTOM', 'LEFT', 'RIGHT', 'NONE')

    # A tuple of composite direction names
    __TOP_LEFT__, __TOP_RIGHT__, __BOTTOM_LEFT__, __BOTTOM_RIGHT__ = \
        __COMPOSITE_DIRECTIONS__ = \
        ('TOP_LEFT', 'TOP_RIGHT', 'BOTTOM_LEFT', 'BOTTOM_RIGHT')

    # A tuple of valid direction names
    __DIRECTIONS__ = __ELEMENTARY_DIRECTIONS__ + __COMPOSITE_DIRECTIONS__
    __HORIZONTAL__ = (__LEFT__, __RIGHT)
    __VERTICAL__ = (__TOP__, __BOTTOM__)

    # Direction composition relationships
    __COMPOSITION__ = {
        frozenset([]): __NONE__,
        frozenset([__TOP__]): __TOP__,
        frozenset([__BOTTOM__]): __BOTTOM__,
        frozenset([__LEFT__]): __LEFT__,
        frozenset([__RIGHT__]): __RIGHT__,
        frozenset([__TOP__, __LEFT__]): __TOP_LEFT__,
        frozenset([__TOP__, __RIGHT__]): __TOP_RIGHT__,
        frozenset([__BOTTOM__, __LEFT__]): __BOTTOM_LEFT__,
        frozenset([__BOTTOM__, __RIGHT__]): __BOTTOM_RIGHT__,
    }
    __REVERSED_COMPOSITION__ = {v: k for k, v in __COMPOSITION__.items()}

    # Negation relationships
    __NEGATIONS__ = {
        __TOP__: __BOTTOM__, 
        __LEFT__: __RIGHT__,
        __TOP_LEFT__: __BOTTOM_RIGHT__,
        __TOP_RIGHT__: __BOTTOM_LEFT__,
        __NONE__: __NONE__,
    }
    __NEGATIONS__.update({v: k for k, v in __NEGATIONS__.items()})

    def __init__(self, *directions):
        """Initializes direction instance from a source.

        :param directions: Direction instances or valid names of directions.
            Direction instances and composite direction names will be 
            expanded to elementary directions before it is stored to frozenset.
        :type directions: :class:`Direction` or :class:`str`

        """
        self.directions = self._reduce(frozenset(itertools.chain(*[
            self._expand(d) for d in directions
        ])))

    def __nonzero__(self):
        return bool(self.directions)

    def __bool__(self):
        return self.__nonzero__()

    def __hash__(self):
        return hash(self.directions)

    def __eq__(self, x):
        return hash(self) == hash(Direction(x))

    def __ne__(self, x):
        return not self.__eq__(x)

    def __add__(self, x):
        return Direction(*self.directions.union(x.directions))

    def __sub__(self, x):
        return Direction(*self.directions.difference(x.directions))

    def __neg__(self):
        return Direction(self.__NEGATIONS__[self.name])

    def __str__(self):
        return 'Direction {}'.format(self.name)

    def __repr__(self):
        return str(self)

    @classmethod
    def _validate(cls, x):
        if not isinstance(x, Direction) and not x in cls.__DIRECTIONS__:
            raise ValueError('Invalid direction has been given: {}'.format(x))

    @classmethod
    def _expand(cls, x):
        cls._validate(x)
        return x.directions if isinstance(x, Direction) else \
            cls.__REVERSED_COMPOSITION__[x]

    @classmethod
    def _reduce(cls, directions):
        if cls.__TOP__ in directions and cls.__BOTTOM__ in directions:
            directions = directions.difference(frozenset([
                cls.__TOP__, cls.__BOTTOM__
            ]))

        if cls.__LEFT__ in directions and cls.__RIGHT__ in directions:
            directions = directions.difference(frozenset([
                cls.__LEFT__, cls.__RIGHT__
            ]))

        return directions

    @property
    def name(self):
        return self.__COMPOSITION__[self.directions]

    @property
    def vertical(self):
        for d in self.directions:
            if d in self.__VERTICAL__:
                return Direction(d)

    @property
    def horizontal(self):
        for d in self.directions:
            if d in self.__HORIZONTAL__:
                return Direction(d)

    @property
    def is_vertical(self):
        return len(self.directions) == 1 and self.vertical

    @property
    def is_horizontal(self):
        return len(self, directions) == 1 and self.horizontal

    @property
    def is_composite(self):
        return len(self.directions) >= 2


# ==========
# Directions
# ==========

TOP = Direction('TOP')
BOTTOM = Direction('BOTTOM')
LEFT = Direction('LEFT')
RIGHT = Direction('RIGHT')
NONE = Direction('NONE')

TOP_LEFT = Direction('TOP_LEFT')
TOP_RIGHT = Direction('TOP_RIGHT')
BOTTOM_LEFT = Direction('BOTTOM_LEFT')
BOTTOM_RIGHT = Direction('BOTTOM_RIGHT')

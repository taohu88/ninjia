class FieldDimension:
    def __init__(self, dimension, indexes):
        self.dimension = dimension
        self.indexes = indexes

    @classmethod
    def to_index(cls, t):
        """
        :param t: t look like "1" or "4-7"
        :return: tuple either size of 1 or 2 (1) or (4, 7)
        """
        a = t.split('-')
        return tuple((int(i) for i in a))

    @classmethod
    def to_field_dimension(cls, dimension_str, v_str):
        dimension = int(dimension_str)
        indexes = [cls.to_index(t) for t in v_str.split(',')]
        return FieldDimension(dimension, indexes)

    def __str__(self):
        return "%s:%s" % (self.indexes, self.dimension)
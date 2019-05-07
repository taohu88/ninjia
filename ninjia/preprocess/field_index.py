class FieldIndex:
    def __init__(self, name, values):
        self.name = name
        self.values = values

    @classmethod
    def to_index(cls, t):
        """
        :param t: t look like "1" or "4-7"
        :return: tuple either size of 1 or 2 (1) or (4, 7)
        """
        a = t.split('-')
        return tuple((int(i) for i in a))

    @classmethod
    def to_filed_index(cls, name, v_str):
        # convert any space to '-'
        k = '-'.join(name.split())
        # get rid of any space in value
        v = ''.join(v_str.split())
        values = [cls.to_index(t) for t in v.split(',')]
        return FieldIndex(k, values)

    def __str__(self):
        return "%s:%s" % (self.name, self.values)
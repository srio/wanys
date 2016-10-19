class Enum(object):
    def __init__(self, enum_type):
        self._enum_type = enum_type

    def __eq__(self, candidate):
        return self._enum_type == candidate._enum_type

    def __ne__(self, candidate):
        return not (self==candidate)

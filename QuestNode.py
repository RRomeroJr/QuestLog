

class QuestNode:
    def __init__(self, _header="", _short_desc="", _long_desc=""
                 , _subquests=None, _id=-1):
        self.header = _header
        self.short_desc = _short_desc
        self.long_desc = _long_desc
        self.subquests = _subquests or []
        self.id = _id
        self.parent = None

    def add_subquest(self, _in):
        self.subquests.append(_in)

    @classmethod
    def fromdict(cls, datadict):
        sq_list = datadict["subquests"]
        loaded_subquests = []
        new_questnode = cls(datadict["header"], datadict["short_desc"], datadict["long_desc"])
        if(len(sq_list) > 0):
            for sq in sq_list:
                sq_obj = cls.fromdict(sq)
                sq_obj.parent = new_questnode
                loaded_subquests.append(sq_obj)
        new_questnode.subquests = loaded_subquests
        return new_questnode
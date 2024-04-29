import json

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
                loaded_subquests.append(sq_obj) # --check: Doesn't it default to an empty list? Just use that?
        new_questnode.subquests = loaded_subquests 
        return new_questnode

class QuestNodeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, QuestNode):
            
            _subquests = [] # Needed to make the deafult an empty array instead of None
            if(len(o.subquests) > 0):
                for sq in o.subquests:
                    _subquests.append(self.default(sq))

            # Getting a dict obj. Dicts become JSON objects
            return {"header": o.header, "short_desc": o.short_desc, "long_desc": o.long_desc, "subquests": _subquests, "id": o.id}

        return super().default(o) #This is make the Encoder Error out.
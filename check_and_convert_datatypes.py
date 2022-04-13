def check_int(self, data) -> bool:
    if isinstance(data, int) : return True
    else: return False

def check_bool(self, data) -> bool:
    if isinstance(data, bool) : return True
    else: return False

def is_none_or_false(self, data = False) -> bool:
    if isinstance(data, bool) and data == False: return True
    if data == None: return True
    else: return True
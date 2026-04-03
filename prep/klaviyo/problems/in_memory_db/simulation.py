"""
All your implementation code for the bank system simulation goes here.
"""
class InMemoryDatabase:
    def __init__(self):
        self.db: dict[str, dict[str, tuple[str, int | None, int | None]]] = {}
    
    # ========== Level 1 Operations ==========
    def set(self, key: str, field: str, value: str):
        return self.__set_internal(key, field, value, None, None)
    
    def get(self, key: str, field: str):
        return self.db.get(key, {}).get(field, ("", None, None))[0]

    def delete(self, key: str, field: str):
        if self.db.get(key) is not None and self.db[key].get(field) is not None:
            del self.db[key][field]
            return "true"
        else:
            return "false"
    
    # ========== Level 2 Operations ==========
    def scan(self, key: str):
        return self.scan_by_prefix(key, "")

    def scan_by_prefix(self, key: str, prefix: str):
        if self.db.get(key) is not None:
            s: list[str] = []
            for k,v in sorted(self.db.get(key, {}).items()):
                if k.startswith(prefix):
                    s.append(f"{k}({v[0]})")

            return ", ".join(s)
        return ""

    def __set_internal(self, key: str, field: str, value: str, timestamp: int | None, expiry: int | None):
        if self.db.get(key) is not None:
            self.db[key][field] = (value, timestamp, expiry)
        else:
            self.db.setdefault(key, {field: (value, timestamp, expiry)})
        return ""

    def __is_live(self, key: str, field: str, timestamp: int):
        if self.db.get(key) is None or self.db[key].get(field) is None:
            return False

        expiry = self.db[key][field][2]
        if expiry is None:
            return True

        return expiry > timestamp

    # ========== Level 3 Operations ==========
    def set_at(self, key: str, field: str, value: str, timestamp: int):
        return self.__set_internal(key, field, value, timestamp, None)

    def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int):
        return self.__set_internal(key, field, value, timestamp, timestamp+ttl)

    def delete_at(self, key: str, field: str, timestamp: int):
        if self.db.get(key) is not None and self.db[key].get(field) is not None:
            if self.__is_live(key, field, timestamp):
                del self.db[key][field]
                return "true"
        return "false"

    def get_at(self, key: str, field: str, timestamp: int):
        if self.__is_live(key, field, timestamp):
            return self.get(key, field)
        return ""

    def scan_at(self, key: str, timestamp: int):
        return self.scan_by_prefix_at(key, "", timestamp)

    def scan_by_prefix_at(self, key: str, prefix: str, timestamp: int):
        if self.db.get(key) is not None:
            s: list[str] = []
            for k,v in sorted(self.db.get(key, {}).items()):
                if k.startswith(prefix) and self.__is_live(key, k, timestamp):
                    s.append(f"{k}({v[0]})")

            return ", ".join(s)
        return ""

    # ========== Level 4 Operations ==========
    def backup(self, timestamp: int):
        pass

    def restore(self, timestamp: int, timestampToRestore: int):
        pass

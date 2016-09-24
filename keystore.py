from typing import Callable, TypeVar, Generic

T = TypeVar('T', int, str, bool)

class KeyEntry(Generic[T]):    

    def __init__(self, key: str, validate_func: Callable[[T], bool], description: str = "", default_val: T = None, required: bool = True) -> None:
        self.__key = key
        self.__value = default_val
        self.__default_value = default_val
        self.__validate = validate_func
        self.__description = "[No Description]" if description == "" else description
        self.__required = required
        self.__is_set = False
    

    def to_default(self) -> None:
        self.__is_set = False
        self.__value = self.__default_value


    def set(self, value: T) -> bool:
        if self.__validate(value):
            self.__is_set = True
            self.__value = value
            return True

        return False


    @property
    def key(self) -> str:
        return self.__key

    @property
    def value(self) -> T:
        return self.__value


    @property
    def description(self) -> str:
        return self.__description


    @property
    def required(self) -> bool:
        return self.__required


    def satisfied(self) -> bool:
        return True if self.required and self.__is_set else False
    

    def __str__(self) -> str:
        return self.key + ": " + str(self.value) + " - " + self.description 



class KeyStore(Generic[T]):

    def __init__(self):
        self.store = {}


    def add_key(self, key: str, validate_func: Callable[[T], bool], description: str = "",
                default_val: T = None, required: bool = True) -> bool:

        if self.contains(key):
            return False

        self.store[key] = KeyEntry(key, validate_func, description, default_val, required)
        return True


    def get_key(self, key: str) -> KeyEntry:
        return self.store[key]

    def keys(self):
        return self.store.keys


    def contains(self, key: str) -> bool:
        return key in self.store


    def __str__(self):
        res = ""
        for key in self.store:
            res += str(self.store[key]) + '\n'

        return res.rstrip()



if __name__ == "__main__":
    obj = KeyStore()
    obj.add_key("rails", (lambda x: x >= 3), "number of rails to decode the ciphertext with", 3, True)

    print(obj)

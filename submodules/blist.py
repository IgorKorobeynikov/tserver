class ListBlockedError(OverflowError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BList(list):
    def __init__(self, capacity, items=()):
        if len(items) > capacity:
            raise OverflowError(
                "The initial size of list is bigger then max size")

        self.__capacity = capacity
        super().__init__(items)

    @property
    def is_full(self):
        return len(self) == self.__capacity

    def append(self, item):
        if self.is_full:
            raise ListBlockedError("list is blocked")
        else:
            super().append(item)

    def insert(self, position, item):
        if self.is_full:
            raise ListBlockedError("list is blocked")
        else:
            super().insert(position, item)

    def extend(self, items):
        if self.__capacity - len(self) < len(items):
            raise OverflowError("The list will be overflow")
        elif self.is_full and items:
            raise ListBlockedError("list is blocked")
        else:
            super().extend(items)

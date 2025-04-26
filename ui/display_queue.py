class DisplayQueue:
    def __init__(self, initial_list=None,console=None):
        self._data = list(initial_list) if initial_list else []
        self.console = console
    def append(self, item):
        
        self._data.append(item)
        self.console.refresh()


    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __delitem__(self, index):
        del self._data[index]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, item):
        return item in self._data

    def __reversed__(self):
        return reversed(self._data)

    def insert(self, index, item):
        self._data.insert(index, item)

    def extend(self, iterable):
        self._data.extend(iterable)

    def remove(self, item):
        self._data.remove(item)

    def pop(self, index=-1):
        return self._data.pop(index)

    def clear(self):
        self._data.clear()

    def index(self, item, *args):
        return self._data.index(item, *args)

    def count(self, item):
        return self._data.count(item)

    def sort(self, *, key=None, reverse=False):
        self._data.sort(key=key, reverse=reverse)

    def reverse(self):
        self._data.reverse()

    def copy(self):
        return DisplayQueue(    self._data.copy())

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data!r})"

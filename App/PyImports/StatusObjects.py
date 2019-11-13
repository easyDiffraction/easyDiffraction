from collections.abc import MutableSet


class StatusList(MutableSet):
    """StatusList is a set container for StatusItems

    Note: This class inherits from MutableSet. This was chosen due to the `add` and `discard`
    methods. It was envisaged that other pars of the code could add and remove status items
    as needed while maintaining the `set` properties.

        :arg itemList: List of StatusItem to be stored.

    """

    def __init__(self, itemList=None):
        if itemList is None:
            self._store = []
        else:
            self._store = itemList

    def __contains__(self, item):
        return item in self._store

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def add(self, item):
        if item not in self._store:
            self._store.append(item)

    def discard(self, item):
        try:
            self._store.remove(item)
        except ValueError:
            raise KeyError

    def getItem(self, itemName):
        """"Get an item by short name"""
        for item in self._store:
            if item.name == itemName:
                return item
        return None

    def setItemValue(self, itemName, value):
        """"Set an items value by short name"""
        item = self.getItem(itemName)
        if item is None:
            raise KeyError
        item.value = value

    def getItemValue(self, itemName):
        """Get an items value by short name"""
        item = self.getItem(itemName)
        if item is None:
            raise KeyError
        return item.value

    def getItems(self):
        return self._store


# noinspection PyPep8Naming,PyPep8Naming
class StatusItem:
    def __init__(self, name, value=None, title=None, additionalData=None):
        self._name = name
        self._value = value
        self._previous = None
        self._title = title
        self._previousTitle = None
        self._returnPrevious = False
        self.additionalData = additionalData

    @property
    def name(self):
        """Returns the given name and appends previous when getting the previous value"""
        if self._returnPrevious & self.hasPrevious:
            return self._name + '_previous'
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        """Returns the current value or previous value if in `previous` mode"""
        if self._returnPrevious & self.hasPrevious:
            if self._previous == self._value:
                return None
            return self._previous
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value, note that only when there's a change!!"""
        if value == self._value:
            return
        self._previous = self._value
        self._value = value

    @property
    def previous(self):
        """Return the previous value"""
        return self._previous

    @property
    def title(self):
        """Returns the current title or alternative title if in `previous` mode"""
        if self._returnPrevious & self.hasPrevious:
            return self._previousTitle
        if self._title is None:
            return self._name
        return self._title

    @title.setter
    def title(self, value):
        if self._returnPrevious:
            self._previousTitle = value
        else:
            self._title = value

    @property
    def hasPrevious(self):
        """An object has previous if it has a previous title.
        NOTE that it can have a previous value while this is False"""
        if self._previousTitle is None:
            return False
        else:
            return True

    def setReturn(self, value):
        """"Switch for `previous` mode"""
        self._returnPrevious = value

    def copy(self):
        """"Make a deep copy. NOTE that some values are lost"""
        return StatusItem(self._name, self._value, self._title)

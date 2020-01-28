import pytest
import logging
import dictdiffer
from ast import literal_eval
from typing import Union, Any, NoReturn, List, Iterable, Tuple
from collections import UserDict
from copy import deepcopy

from PySide2.QtWidgets import QUndoStack, QUndoCommand


class _EmptyCommand(QUndoCommand):
    """
    The _EmptyCommand class is the custom base class of all undoable commands
    stored on a QUndoStack.
    """

    def __init__(self, dictionary: 'UndoableDict', key: Union[str, list], value: Any):
        QUndoCommand.__init__(self)
        self._dictionary = dictionary
        self._key = key
        self._new_value = value
        self._old_value = dictionary.getItem(key)
        #print(f"dict: {id(self._dictionary)}, key: {id(self._key)}, new val: {id(self._old_value)}, old val: {id(self._old_value)}")


class _AddItemCommand(_EmptyCommand):
    """
    The _AddItemCommand class implements a command to add a key-value pair to
    the UndoableDict-base_dict dictionary.
    """

    def __init__(self, dictionary: 'UndoableDict', key: Union[str, list], value: Any):
        super().__init__(dictionary, key, value)
        self.setText("Adding: {} = {}".format(self._key, self._new_value))

    def undo(self) -> NoReturn:
        self._dictionary._realDelItem(self._key)

    def redo(self) -> NoReturn:
        self._dictionary._realAddItem(self._key, self._new_value)


class _SetItemCommand(_EmptyCommand):
    """
    The _SetItemCommand class implements a command to modify the value of
    the existing key in the UndoableDict-base_dict dictionary.
    """

    def __init__(self, dictionary: 'UndoableDict', key: Union[str, list], value: Any):
        super().__init__(dictionary, key, value)
        self.setText("Setting: {} = {}".format(self._key, self._new_value))

    def undo(self) -> NoReturn:
        self._dictionary._realSetItem(self._key, self._old_value)

    def redo(self) -> NoReturn:
        self._dictionary._realSetItem(self._key, self._new_value)


class PathDict(UserDict):
    """
    The PathDict class extends a python dictionary with methods to access its nested
    elements by list-base_dict path of keys.
    """

    # Private methods

    def _realSetItem(self, key: Union[str, List], value: Any) -> NoReturn:
        """Actually changes the value for the existing key in dictionary."""
        if isinstance(key, list):
            self.getItemByPath(key[:-1])[key[-1]] = value
        else:
            super().__setitem__(key, value)

    def _realAddItem(self, key: str, value: Any) -> NoReturn:
        """Actually adds a key-value pair to dictionary."""
        super().__setitem__(key, value)

    def _realDelItem(self, key: str) -> NoReturn:
        """Actually deletes a key-value pair from dictionary."""
        del self[key]

    def _realSetItemByPath(self, keys: list, value: Any) -> NoReturn:
        """Actually sets the value in a nested object by the key sequence."""
        self.getItemByPath(keys[:-1])[keys[-1]] = value

    # Public methods

    def __setitem__(self, key: str, val: Any) -> NoReturn:
        """Overrides default dictionary assignment to self[key] implementation."""
        if key in self:
            self._realSetItem(key, val)
        else:
            self._realAddItem(key, val)

    def setItemByPath(self, keys: list, value: Any) -> NoReturn:
        """Set a value in a nested object by key sequence."""
        self._realSetItem(keys, value)

    def setItem(self, key: Union[str, list], value: Any) -> NoReturn:
        """Set a value in a nested object by key sequence or by simple key."""
        if isinstance(key, list):
            self.setItemByPath(key, value)
        else:
            self[key] = value

    def getItemByPath(self, keys: list, default=None) -> Any:
        """Returns a value in a nested object by key sequence."""
        item = self
        for key in keys:
            if isinstance(item, list):
                item = item[key]
            else:
                if key in item.keys():
                    item = item[key]
                else:
                    return default
        return item

    def getItem(self, key: Union[str, list], default=None):
        """Returns a value in a nested object. Key can be either a sequence
        or a simple string."""
        if isinstance(key, list):
            return self.getItemByPath(key, default)
        else:
            return self.get(key, default)

    def asDict(self) -> dict:
        """Returns self as a python dictionary."""
        base_dict = deepcopy(self.data)
        for key in base_dict.keys():
            item = base_dict[key]
            if hasattr(item, 'asDict'):
                base_dict[key] = item.asDict()
        return base_dict

    def dictComparison(self, another_dict: Union['PathDict', dict], ignore=None) -> Tuple[list, list]:
        """
        Compare self to a dictionary or PathDict and return the update path and value
        :param ignore: What to ignore e.g. set(['a']))
        :param another_dict: dict or PathDict to compare self to
        :return: path and value updates for self to become newDict
        """

        if not isinstance(another_dict, (PathDict, dict)):
            raise TypeError

        key_list = []
        value_list = []

        for item in dictdiffer.diff(self, another_dict, ignore=ignore):
            type = item[0]
            path = item[1]
            changes = item[2]

            if isinstance(path, str):
                path = path.split(".")

            if type == 'change':
                if isinstance(path[-1], int):
                    path = path[:-1]
                    if path in key_list:
                        continue
                    new_value = another_dict.getItemByPath(path)
                else:
                    new_value = changes[1]
            elif type == 'add':
                if not isinstance(changes[0][0], int):
                    path.append(changes[0][0])
                    new_value = changes[0][1]
                else:
                    if path in key_list:
                        continue
                    new_value = another_dict.getItemByPath(path)
                if path[0] == '':
                    del path[0]
            elif type == 'remove':
                continue

            key_list.append(path)
            value_list.append(new_value)

        return key_list, value_list


class UndoableDict(PathDict):
    """
    The UndoableDict class implements a PathDict-base_dict class with undo/redo
    functionality base_dict on QUndoStack.
    """

    def __init__(self, *args, **kwargs):
        self.__stack = QUndoStack()
        self._macroRunning = False
        super().__init__(*args, **kwargs)

    # Public methods: dictionary-related

    def __setitem__(self, key: str, val: Any) -> NoReturn:
        """
        Calls the undoable command to override PathDict assignment to self[key]
        implementation and pushes this command on the stack.
        """
        if key in self:
            self.__stack.push(_SetItemCommand(self, key, val))
        else:
            self.__stack.push(_AddItemCommand(self, key, val))

    def setItemByPath(self, keys: list, value: Any) -> NoReturn:
        """
        Calls the undoable command to set a value in a nested object
        by key sequence and pushes this command on the stack.
        """
        self.__stack.push(_SetItemCommand(self, keys, value))

    # Public methods: undo/redo-related

    def clearUndoStack(self) -> NoReturn:
        """
        Clears the command stack by deleting all commands on it, and
        returns the stack to the clean state.
        """
        self.__stack.clear()

    def canUndo(self) -> bool:
        """
        :return true if there is a command available for undo;
        otherwise returns false.
        """
        return self.__stack.canUndo()

    def canRedo(self) -> bool:
        """
        :return true if there is a command available for redo;
        otherwise returns false.
        """
        return self.__stack.canRedo()

    def undo(self) -> NoReturn:
        """
        Undoes the current command on stack.
        """
        self.__stack.undo()

    def redo(self) -> NoReturn:
        """
        Redoes the current command on stack.
        """
        self.__stack.redo()

    def undoText(self) -> str:
        """
        :return the current command on stack.
        """
        return self.__stack.undoText()

    def redoText(self) -> str:
        """
        :return the current command on stack.
        """
        return self.__stack.redoText()

    def startBulkUpdate(self, text='Bulk update') -> NoReturn:
        """
        Begins composition of a macro command with the given text description.
        """
        if self._macroRunning:
            print('Macro already running')
            return
        self.__stack.beginMacro(text)
        self._macroRunning = True

    def endBulkUpdate(self) -> NoReturn:
        """
        Ends composition of a macro command.
        """
        if not self._macroRunning:
            print('Macro not running')
            return
        self.__stack.endMacro()
        self._macroRunning = False

    def bulkUpdate(self, key_list: list, item_list: list, text='Bulk update') -> NoReturn:
        """
        Performs a bulk update base_dict on a list of keys and a list of values
        :param key_list: list of keys or path keys to be updated
        :param item_list: the value to be updated
        :return: None
        """
        self.startBulkUpdate(text)
        for key, value in zip(key_list, item_list):
            self.setItemByPath(key, value)
        self.endBulkUpdate()


if __name__ == "__main__":
    # Run unit tests
    #pytest.main(["-v"])

    d1 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    d2 = PathDict(dict(a=1, b=2, c=dict(d=333, e=dict(f=4, g=555))))
    print("A", d1.dictComparison(d2))

    d1 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    d2 = {'a': 1, 'b': 2, 'c': {'d': 333, 'e': {'f': 4, 'g': 555}}}
    print("c", d1.dictComparison(d2))

    d1 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    d2 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4))))
    print("D", d1.dictComparison(d2))

    d1 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(g=5))))
    d2 = PathDict(dict(a=1, b=2, c=dict(d=3, e=dict(f=4, g=5))))
    print("E", d1.dictComparison(d2))

    d1 = PathDict({ 'a': 1, 'b': 2, 'c': PathDict({ 'd': 3, 'e': PathDict({ 'f': 4 }) }) })
    d2 = PathDict({ 'a': 1, 'b': 2, 'c': PathDict({ 'd': 3, 'e': PathDict({ 'f': 4, 'g': 5 }) }) })
    print("F", d1.dictComparison(d2))

    d1 = PathDict({ 'a': 1, 'b': 2 })
    d2 = PathDict({ 'a': 1, 'b': 2, 'c': PathDict({ 'd': 3, 'e': PathDict({ 'f': 4, 'g': 5 }) }) })
    print("G", d1.dictComparison(d2))

    d1 = PathDict({ 'a': 1, 'b': 2, 'm': 0  })
    d2 = PathDict({ 'a': 9, 'c': PathDict({ 'd': 3, 'e': PathDict({ 'f': 4, 'g': 5 }) }), 'm': 1 })
    print("H", d1.dictComparison(d2))

    d1 = PathDict({ 'a': 9, 'c': { 'd': 3, 'e 1': { 'f': 4, 'g': 5 } }, 'm': 1, 'o': { 'p': { 'q': 8, 'r.2': 0 } } })
    d2 = { 'a': 99, 'c': { 'd': 3, 'e 1': { 'f': 4, 'g': 55, 'h': 66 } }, 'm': 11, 'o': { 'p': { 'r.2': 2 } } }
    print("K", d1.dictComparison(d2))

    d1 = PathDict({ 'a': 9, 'c': PathDict({ 'd': 3, 'e 1': PathDict({ 'f': 4, 'g': 5 }) }), 'm': 1, 'o': PathDict({ 'p': PathDict({ 'q': 8, 'r.2': 0 }) }) })
    d2 = PathDict({ 'a': 99, 'c': PathDict({ 'd': 3, 'e 1': PathDict({ 'f': 4, 'g': 55, 'h': 66 }) }), 'm': 11, 'o': PathDict({ 'p': PathDict({ 'r.2': 2 }) }) })
    print("M", d1.dictComparison(d2))

    d1 = PathDict({ 'a': 9, 'c': PathDict({ 'd': 3, 'e 1': PathDict({ 'f': 4, 'g': 5 }) }), 'm': 1, 'o': PathDict({ 'p': PathDict({ 'q': 8, 'r.2': 0 }) }) })
    d2 = PathDict({ 'aa': PathDict(alpha=1, beta=2), 'a': 99, 'c': PathDict({ 'd': 3, 'e 1': PathDict({ 'f': 4, 'g': 55, 'h': 66 }) }), 'm': 11, 'o': PathDict({ 'p': PathDict({ 'r.2': 2 }) }) })
    print("N", d1.dictComparison(d2))
    k, v = d1.dictComparison(d2)
    for item in v:
        print(item, type(item))

    d1 = PathDict(a=[1, 2, 3], b={'c': 2})
    d2 = PathDict(a=[1, 2, 3, 4], b={'c': 2, 'd': 4, 3: 5})
    print("O", d1.dictComparison(d2))
    print(list(dictdiffer.diff(d1, d2)))
    # k, v = d1.dictComparison(d2)


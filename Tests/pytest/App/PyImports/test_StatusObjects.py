import pytest


## TESTS FOR STATUSITEM

def test_StatusItem_creation():
    # Empty Item creation....
    with pytest.raises(TypeError):
        item = StatusItem()

    assert isinstance(StatusItem('test0'), StatusItem)
    assert isinstance(StatusItem('test0', 0), StatusItem)
    assert isinstance(StatusItem('test0', 0, 'Testing Object Number 0'), StatusItem)
    assert isinstance(StatusItem('test0', 0, 'Testing Object Number 0', 1), StatusItem)


def test_StatusItem_getName():
    def getName(thisItem):
        return thisItem.name

    item = StatusItem('test0')
    assert getName(item) == 'test0'

    item = StatusItem('test0', 0)
    assert getName(item) == 'test0'

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    assert getName(item) == 'test0'

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    assert getName(item) == 'test0'


def test_StatusItem_setName():
    n = 2

    def setName(thisItem, n):
        thisItem.name = 'test%i' % (n + 2)

    def getName(thisItem):
        return thisItem.name

    item = StatusItem('test0')
    setName(item, n)
    assert getName(item) == 'test%i' % (n + 2)

    item = StatusItem('test0', 0)
    setName(item, n)
    assert getName(item) == 'test%i' % (n + 2)

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    setName(item, n)
    assert getName(item) == 'test%i' % (n + 2)

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    setName(item, n)
    assert getName(item) == 'test%i' % (n + 2)


def test_StatusItem_getValue():
    def getValue(thisItem):
        return thisItem.value

    item = StatusItem('test0')
    assert getValue(item) == None

    item = StatusItem('test0', 0)
    assert getValue(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    assert getValue(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    assert getValue(item) == 0


def test_StatusItem_setValue():
    n = 2

    def setValue(thisItem, n):
        thisItem.value = n + 2

    def getValue(thisItem):
        return thisItem.value

    item = StatusItem('test0')
    setValue(item, n)
    assert getValue(item) == (n + 2)

    item = StatusItem('test0', 0)
    setValue(item, n)
    assert getValue(item) == (n + 2)

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    setValue(item, n)
    assert getValue(item) == (n + 2)

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    setValue(item, n)
    assert getValue(item) == (n + 2)


def test_StatusItem_getPrevious():
    n = 2

    def setValue(thisItem, n):
        thisItem.value = n + 2

    def getPrevious(thisItem):
        return thisItem.previous

    # Test the case where value changes
    item = StatusItem('test0')
    setValue(item, n)
    assert getPrevious(item) == None

    item = StatusItem('test0', 0)
    setValue(item, n)
    assert getPrevious(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    setValue(item, n)
    assert getPrevious(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    setValue(item, n)
    assert getPrevious(item) == 0

    # Test the case where they are the same
    item = StatusItem('test0')
    setValue(item, n)
    setValue(item, n)
    assert getPrevious(item) == None

    item = StatusItem('test0', 0)
    setValue(item, n)
    setValue(item, n)
    assert getPrevious(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    setValue(item, n)
    setValue(item, n)
    assert getPrevious(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    setValue(item, n)
    setValue(item, n)
    assert getPrevious(item) == 0


def test_StatusItem_getTitle():
    def getTitle(thisItem):
        return thisItem.title

    item = StatusItem('test0')
    assert getTitle(item) == 'test0'

    item = StatusItem('test0', 0)
    assert getTitle(item) == 'test0'

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    assert getTitle(item) == 'Testing Object Number 0'

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    assert getTitle(item) == 'Testing Object Number 0'


def test_StatusItem_setTitle():
    n = 2

    def setTitle(thisItem, n):
        thisItem.title = 'Testing Object Number %i' % (n + 2)

    def getTitle(thisItem):
        return thisItem.title

    item = StatusItem('test0')
    setTitle(item, n)
    assert getTitle(item) == 'Testing Object Number %i' % (n + 2)

    item = StatusItem('test0', 0)
    setTitle(item, n)
    assert getTitle(item) == 'Testing Object Number %i' % (n + 2)

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    setTitle(item, n)
    assert getTitle(item) == 'Testing Object Number %i' % (n + 2)

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    setTitle(item, n)
    assert getTitle(item) == 'Testing Object Number %i' % (n + 2)


def test_StatusItem_hasPrevious():
    def getHasPrevious(thisItem):
        return thisItem.hasPrevious

    def setValue(thisItem, value):
        thisItem.value = value

    item = StatusItem('test0')
    assert getHasPrevious(item) == False
    setValue(item, 0)
    setValue(item, 1)
    assert getHasPrevious(item) == False
    item.setReturn(True)
    item.title = 'test0 Previous'
    item.setReturn(False)
    assert getHasPrevious(item) == True

    item = StatusItem('test0', 0)
    assert getHasPrevious(item) == False
    setValue(item, 1)
    assert getHasPrevious(item) == False
    item.setReturn(True)
    item.title = 'test0 Previous'
    item.setReturn(False)
    assert getHasPrevious(item) == True

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    assert getHasPrevious(item) == False
    setValue(item, 1)
    assert getHasPrevious(item) == False
    item.setReturn(True)
    item.title = 'test0 Previous'
    item.setReturn(False)
    assert getHasPrevious(item) == True

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    assert getHasPrevious(item) == False
    setValue(item, 1)
    assert getHasPrevious(item) == False
    item.setReturn(True)
    item.title = 'test0 Previous'
    item.setReturn(False)
    assert getHasPrevious(item) == True


def test_StatusItem_previousTitle():
    def setValue(thisItem, value):
        thisItem.value = value

    def getValue(thisItem):
        return thisItem.value

    def getTitle(thisItem):
        return thisItem.title

    item = StatusItem('test0')
    setValue(item, 0)
    setValue(item, 1)
    item.setReturn(True)
    item.title = 'test0 Previous'
    assert getTitle(item) == 'test0 Previous'
    assert getValue(item) == 0

    item = StatusItem('test0', 0)
    setValue(item, 1)
    item.setReturn(True)
    item.title = 'test0 Previous'
    assert getTitle(item) == 'test0 Previous'
    assert getValue(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    setValue(item, 1)
    item.setReturn(True)
    item.title = 'test0 Previous'
    assert getTitle(item) == 'test0 Previous'
    assert getValue(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    setValue(item, 1)
    item.setReturn(True)
    item.title = 'test0 Previous'
    assert getTitle(item) == 'test0 Previous'
    assert getValue(item) == 0


def test_StatusItem_previousName():

    def setValue(thisItem, value):
        thisItem.value = value

    def getValue(thisItem):
        return thisItem.value

    def getName(thisItem):
        return thisItem.name

    item = StatusItem('test0')
    setValue(item, 0)
    setValue(item, 1)
    item.setReturn(True)
    item.title = 'test0 Previous'
    assert getName(item) == 'test0_previous'
    assert getValue(item) == 0

    item = StatusItem('test0', 0)
    setValue(item, 1)
    item.setReturn(True)
    item.title = 'test0 Previous'
    assert getName(item) == 'test0_previous'
    assert getValue(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0')
    setValue(item, 1)
    item.setReturn(True)
    item.title = 'test0 Previous'
    assert getName(item) == 'test0_previous'
    assert getValue(item) == 0

    item = StatusItem('test0', 0, 'Testing Object Number 0', 1)
    setValue(item, 1)
    item.setReturn(True)
    item.title = 'test0 Previous'
    assert getName(item) == 'test0_previous'
    assert getValue(item) == 0


## TESTS FOR STATUSLIST
def createStatusList(n):
    thisList = []
    for i in range(n):
        thisList.append(StatusItem('test%i' % i, i, 'Testing Object Number %i' % i))
    return StatusList(thisList), thisList


def test_empty_StatusList_creation():
    thisList = StatusList()
    assert len(thisList) == 0


def test_item_StatusList_creation():
    item1 = StatusItem('test1', 1, 'Testing Object Number 1')
    item2 = StatusItem('test2', 2, 'Testing Object Number 2')
    item3 = StatusItem('test3', 3, 'Testing Object Number 3')

    oldList = [item1, item2]
    thisList = StatusList(oldList)

    assert len(thisList) == 2
    assert (item1 in thisList) == True
    assert (item3 in thisList) == False

    # Note that the current implementation cant do `i, item in thisList:`
    i = 0
    for item in thisList:
        assert item == oldList[i]
        i += 1


@pytest.mark.parametrize("n", range(3))
def test_StatusList_getItem(n):
    thisList, oldList = createStatusList(n)
    for i in range(n):
        item = thisList.getItem('test%i' % i)
        assert item == oldList[i]

    assert thisList.getItem('test%i' % (n + 2)) is None


@pytest.mark.parametrize("n", range(4))
def test_StatusList_getItemValue(n):
    thisList, oldList = createStatusList(n)
    for i in range(n):
        value = thisList.getItemValue('test%i' % i)
        assert value == i


def test_StatusList_setItemValue():
    n = 4
    thisList, oldList = createStatusList(n)

    for i in range(n):
        thisList.setItemValue('test2', n + 2)
        assert thisList.getItemValue('test2') == n + 2

    with pytest.raises(KeyError):
        thisList.setItemValue('test%i' % (n + 1), n + 1)


def test_StatusList_getItems():
    n = 4
    thisList, oldList = createStatusList(n)
    assert len(set(thisList.getItems()).intersection(set(oldList))) == n


def test_StatusList_add():
    n = 3
    thisList, oldList = createStatusList(n)
    n_new = n + 1
    newItem = StatusItem('test%i' % n_new, n_new, 'Testing Object Number %i' % n_new)
    thisList.add(newItem)

    assert len(thisList) == n_new


def test_StatusList_discard():
    n = 3
    thisList, oldList = createStatusList(n)

    # Remove an item via remove
    rmItem = n - 2
    thisItem = thisList.getItem('test%i' % rmItem)
    thisList.remove(thisItem)
    assert len(thisList) == n - 1
    for i in range(n):
        if i == rmItem:
            assert thisList.getItem('test%i' % i) == None
        else:
            assert thisList.getItem('test%i' % i).value == i
    # Remove an item via discard
    rmItem = n - 1
    thisItem = thisList.getItem('test%i' % rmItem)
    thisList.discard(thisItem)
    assert len(thisList) == n - 2
    for i in range(n):
        if (i == (n - 2)) or (i == (n - 1)):
            assert thisList.getItem('test%i' % i) == None
        else:
            assert thisList.getItem('test%i' % i).value == i

    # Remove a non existent item.
    with pytest.raises(KeyError):
        thisList.discard(thisItem)

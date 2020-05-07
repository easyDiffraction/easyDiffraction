from PySide2.QtCore import Signal, QThread


class Refiner(QThread):
    """
    Simple wrapper for calling a function in separate thread
    """
    failed = Signal(str)
    finished = Signal(dict)

    def __init__(self, obj, method_name, parent=None):
        QThread.__init__(self, parent)
        self._obj = obj
        self.method_name = method_name

    def run(self):
        res = {}
        if hasattr(self._obj, self.method_name):
            func = getattr(self._obj, self.method_name)
            try:
                res = func()
            except Exception as ex:
                self.failed.emit(str(ex))
                return str(ex)
        self.finished.emit(res)
        return res

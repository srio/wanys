from orangecontrib.wanys.drivers.srw.SRWDriver import SRWDriver
from orangecontrib.wanys.drivers.shadow.ShadowDriver import ShadowDriver

class ActiveDriver:
    class __ActiveDriver:
        def __init__(self):
            self._driver = None

        def setDriver(self, driver):
            self._driver = driver

        def driver(self):
            return self._driver

        def __str__(self):
            return repr(self) + self.driver()

    _instance = None
    def __init__(self):
        if not ActiveDriver._instance:
            ActiveDriver._instance = ActiveDriver.__ActiveDriver()
            self.setDriver(SRWDriver())
            #self.setDriver(ShadowDriver())

    def setDriver(self, driver):
        self._instance.setDriver(driver)

    def driver(self):
        return self._instance.driver()

    def __getattr__(self, name):
        return getattr(self._instance, name)
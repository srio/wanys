import unittest

from orangecontrib.wanys.tests.utils.OpticalElementTest import OpticalElementTest
from orangecontrib.wanys.tests.utils.OpticalRouteTest import OpticalRouteTest
from orangecontrib.wanys.tests.drivers.DriverSettingsTest import DriverSettingsTest
from orangecontrib.wanys.tests.drivers.AbstractDriverDataTest import AbstractDriverDataTest
from orangecontrib.wanys.tests.drivers.AbstractDriverTest import AbstractDriverTest
from orangecontrib.wanys.tests.drivers.DriverSettingAttributeTest import DriverSettingAttributeTest
from orangecontrib.wanys.tests.drivers.srw.SRWDriverTest import SRWDriverTest


def suite():
    suites = (
        unittest.makeSuite(OpticalElementTest, 'test'),
        unittest.makeSuite(OpticalRouteTest, 'test'),

        unittest.makeSuite(DriverSettingsTest, 'test'),
        unittest.makeSuite(AbstractDriverDataTest, 'test'),
        unittest.makeSuite(AbstractDriverTest, 'test'),
        unittest.makeSuite(DriverSettingAttributeTest, 'test'),
        unittest.makeSuite(SRWDriverTest, 'test'),
    )
    return unittest.TestSuite(suites)


if __name__ == "__main__":
    unittest.main(defaultTest="suite")


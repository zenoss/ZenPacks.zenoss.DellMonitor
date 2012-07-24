##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import logging
from cPickle import loads

from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.DataCollector.ApplyDataMap import ApplyDataMap
from ZenPacks.zenoss.DellMonitor.modeler.plugins.DellDeviceMap \
    import DellDeviceMap

log = logging.getLogger("zen.testcases")


class TestDellDeviceMap(BaseTestCase):
    def afterSetUp(self):
        super(TestDellDeviceMap, self).afterSetUp()
        self.adm = ApplyDataMap()
        self.ddmap = DellDeviceMap()
        self.device = self.dmd.Devices.createInstance('testDevice')


    def testWin2003Server(self):
        results = loads("((dp1\nS'setHWSerialNumber'\np2\nS'DTG4C91'\np3\nsS'setHWProductKey'\np4\nS'PowerEdge 850'\np5\nsS'setOSProductKey'\np6\nS'Microsoft Windows Server 2003, Enterprise Edition'\np7\ns(dtp8\n.")
        
        # Verify that the modeler plugin processes the data properly.
        om = self.ddmap.process(self.device, results, log)
        self.assertEquals(om.setHWSerialNumber, 'DTG4C91')
        self.assertEquals(om.setHWProductKey.args[0], 'PowerEdge 850')
        self.assertEquals(om.setHWProductKey.args[1], 'Dell')
        self.assertEquals(om.setOSProductKey.args[0],
            'Microsoft Windows Server 2003, Enterprise Edition')
        self.assertEquals(om.setOSProductKey.args[1], 'Microsoft')
        
        # Verify that the data made it into the model properly.
        self.adm._applyDataMap(self.device, om)
        self.assertEquals(self.device.getHWSerialNumber(), 'DTG4C91')
        self.assertEquals(self.device.getHWManufacturerName(), 'Dell')
        self.assertEquals(self.device.getHWProductName(), 'PowerEdge 850')
        self.assertEquals(self.device.getOSManufacturerName(), 'Microsoft')
        self.assertEquals(self.device.getOSProductName(),
            'Microsoft Windows Server 2003, Enterprise Edition')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDellDeviceMap))
    return suite

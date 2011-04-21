###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import logging
from cPickle import loads

from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.DataCollector.ApplyDataMap import ApplyDataMap
from ZenPacks.zenoss.DellMonitor.modeler.plugins.DellDeviceMap \
    import DellDeviceMap

log = logging.getLogger("zen.testcases")


class TestDellDeviceMap(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
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

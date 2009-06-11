###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class DellPCIMap(SnmpPlugin):
    """Map Dell Open Manage PCI table to model."""

    maptype = "DellPCIMap"
    modname = "Products.ZenModel.ExpansionCard"
    relname = "cards"
    compname = "hw"

    columns = {'.6': 'slot','.8': '_manuf','.9': '_model',}

    snmpGetTableMaps = (
        GetTableMap('pciTable', '.1.3.6.1.4.1.674.10892.1.1100.80.1', columns),
    )
    
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        pcitable = tabledata.get("pciTable")
        if not pcitable: return
        rm = self.relMap()
        for card in pcitable.values():
            try:
                om = self.objectMap(card)
                om.id = self.prepId("%s" % om.slot)
                om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                continue
            rm.append(om)
        return rm

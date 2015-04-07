#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dokanHeader import *
from dokanClass import *

class ExempleFS(DokanAPI):
	
	def __init__(self, DriverMountPoint, DriverOption):
		DokanAPI.__init__(self, DriverMountPoint, DriverOption)
		
	
DriverOption = DOKAN_OPTION_DEBUG | DOKAN_OPTION_STDERR | DOKAN_OPTION_KEEP_ALIVE
exemplefs = ExempleFS("Y:\\", DriverOption)
exemplefs.main()

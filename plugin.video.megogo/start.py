#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, sys, urllib2, re

addon           = xbmcaddon.Addon()
addon_name		= addon.getAddonInfo('name')
addon_version	= addon.getAddonInfo('version')
addon_path 		= xbmc.translatePath(addon.getAddonInfo('path'))
language        = addon.getLocalizedString

sys.path.append(os.path.join(addon_path, 'resources', 'lib'))
from Utils import fetch_data

xbmc.log('[%s]: Start plugin! Version: %s' % (addon_name, addon_version))
####################################		Start Splash	#########################################
splash = xbmcgui.WindowXML('splash.xml', addon_path)
splash.show()

if fetch_data(page='configuration'):    # Get config from MEGOGO
    import default
    default.Main(splash=splash)
else:
    dialog = xbmcgui.Dialog()
    dialog.ok(language(1025), language(1031), language(1032))
    dialog.close()
    
splash.close()

xbmc.log('[%s]: Close plugin! Version: %s' % (addon_name, addon_version))
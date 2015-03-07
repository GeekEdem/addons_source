#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, sys, urllib2, re

addon           = xbmcaddon.Addon()
addon_name		= addon.getAddonInfo('name')
addon_version	= addon.getAddonInfo('version')
addon_path 		= xbmc.translatePath(addon.getAddonInfo('path'))
language        = addon.getLocalizedString

source = 'https://raw.githubusercontent.com/GeekEdem/plugin.video.megogo/master/'
path_to_addon_on_github = os.path.join(source, 'addon.xml')

sys.path.append(os.path.join(addon_path, 'resources', 'lib'))
from Utils import fetch_data

xbmc.log('[%s]: Start plugin! Version: %s' % (addon_name, addon_version))

####################################		Start Splash	#########################################
splash = xbmcgui.WindowXML('splash.xml', addon_path)
splash.show()

xbmc.log('[%s]: Trying to get new version...' % addon_name)
try:
    request = urllib2.Request(url=path_to_addon_on_github, headers={'User-Agent': 'MEGOGO Addon for XBMC/Kodi'})
    request = urllib2.urlopen(request)
    http = request.read()
    request.close()

    p = re.compile('name="MEGOGO\WNET"\W.*?version="([^"]*?)"')
    branch_release = re.search(p, http).group(1)

    if addon_version != branch_release:
        xbmc.log(addon_path)
except:
    xbmc.log('[%s]: No new version addon available.' % addon_name)
    pass

if fetch_data(page='configuration'): # Get config from MEGOGO
    import default
    default.Main(splash=splash)
else:
    dialog = xbmcgui.Dialog()
    dialog.ok(language(1025), language(1031), language(1032))
    del dialog
    del splash
    
dialog.close()
splash.close()

xbmc.log('[%s]: Close plugin. Version: %s' % (addon_name, addon_version))
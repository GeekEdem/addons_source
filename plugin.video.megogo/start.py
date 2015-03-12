#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, sys, urllib2, re

__addon__       = xbmcaddon.Addon(id='plugin.video.megogo')
addon_name		= __addon__.getAddonInfo('name')
addon_version	= __addon__.getAddonInfo('version')
addon_path 		= xbmc.translatePath(__addon__.getAddonInfo('path'))
language        = __addon__.getLocalizedString
source          = 'http://raw.github.com/GeekEdem/zip/master/plugin.video.megogo/__addon__.xml'

sys.path.append(os.path.join(addon_path, 'resources', 'lib'))
from megogo2xbmc import getconfiguration
from sqlite import DataBase
db = DataBase()

xbmc.log('[%s]: Start plugin! Version: %s' % (addon_name, addon_version))

# ##################################	  Start Splash	    ####################################### #
splash = xbmcgui.WindowXML('splash.xml', addon_path)
splash.show()

# ##################################		First run		####################################### #
if __addon__.getSetting('firstrun') == '0' or __addon__.getSetting('firstrun') == '':
    __addon__.openSettings()
    __addon__.setSetting(id='firstrun', value='1')

usr = __addon__.getSetting('login')
pwd = __addon__.getSetting('password')
if not usr and not pwd:
    db.clear_table('account')
else:
    db.login_data_to_db(usr, pwd)
    db.cookie_to_db("")

#xbmc.executebuiltin("XBMC.UpdateAddonRepos()")

xbmc.log('[%s]: Trying to get new version...' % addon_name)
try:
    request = urllib2.Request(url=source, headers={'s-Agent': 'MEGOGO Addon for XBMC/Kodi'})
    request = urllib2.urlopen(request)
    http = request.read()
    request.close()

    p = re.compile('name="MEGOGO\WNET"\W.*?version="([^"]*?)"')
    branch_release = re.search(p, http).group(1)
    xbmc.log('[%s]: Branch version - %s' % (addon_name, branch_release))

    if addon_version != branch_release:
        dialog = xbmcgui.Dialog()
        dialog.ok(language(1033), language(1034))
        del dialog
except:
    xbmc.log('[%s]: No new version addon available.' % addon_name)
    pass

if getconfiguration():    # Get config from MEGOGO
    import Screens
    Screens.Main(splash=splash)
else:
    dialog = xbmcgui.Dialog()
    dialog.ok(language(1025), language(1031), language(1032))
    del dialog

splash.close()

dic = db.get_login_from_db()
__addon__.setSetting(id='login', value=dic['login'])
__addon__.setSetting(id='password', value=dic['password'])
xbmc.log('[%s]: Close plugin. Version: %s' % (addon_name, addon_version))
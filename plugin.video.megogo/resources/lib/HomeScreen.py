# -*- coding: utf-8 -*- 
#############################################################################
#
#	Copyright (C) 2015 Studio-Evolution
#
#	Home Screen of MEGOGO.NET for XBMC
#
#############################################################################

import xbmc, xbmcgui, xbmcaddon
import VideoInfo, VideoList, megogo2xbmc, urllib
from Utils import *

addon			= xbmcaddon.Addon()
addon_name		= addon.getAddonInfo('name')
addon_path		= addon.getAddonInfo('path').decode("utf-8")
language	    = addon.getLocalizedString

busydialog		= xbmcgui.Window(10138)

class Homescreen(xbmcgui.WindowXMLDialog):
    ACTION_PREVIOUS_MENU    = [92, 9]
    ACTION_EXIT_SCRIPT      = [13, 10]
    ACTION_CONTEX_MENU      = [117]
    ACTION_RIGHT_CLICK      = [101]
    MENU_IDS                = [7001, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010]

    def __init__(self, *args, **kwargs):
        self.splash = kwargs.get('win')
        self.usr = kwargs.get('usr')
        self.pwd = kwargs.get('pwd')
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        self.logged_in = megogo2xbmc.checkLogin(usr=self.usr,  pwd=self.pwd)
        fetch_data(page='tarification')						# Get tarification from MEGOGO
        self.listitems = update_content(page='Main', section='slider')
        self.slider_len = len(self.listitems)
        xbmcgui.WindowXMLDialog.__init__(self)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def onInit(self):
        if self.splash: self.splash.close()
        #self.windowid = xbmcgui.getCurrentWindowDialogId()
        #self.window = xbmcgui.Window(self.windowid)

        self.getControl(500).reset()
        self.getControl(500).addItems(self.listitems)

        item = CreateListItems(fetch_data(page='Main', section='recommended'))
        self.getControl(501).reset()
        self.getControl(501).addItems(item)

        control = getids()
        if control:
            try:
                if control.isnumeric:
                     xbmc.log('SELECT control.isnumeric %s' % control)
                     xbmc.executebuiltin("Control.SetFocus(%s)" % control)
            except:
                try:
                    selectedId, _, item = control.partition(', ')
                    xbmc.log('SELECT %s %s' % (int(selectedId), int(item)))
                    self.setFocusId(int(selectedId))
                    self.getControl(int(selectedId)).selectItem(int(item))
                except:
                    self.setFocusId(6000)

    def onAction(self, action):
        focusid = self.getFocusId()
        #xbmc.log('[%s]: HomeScreen focusid id - %s' % (addon_name, focusid))
        if action in self.ACTION_PREVIOUS_MENU:
            xbmc.log('[%s]: HomeScreen PREVIOUS_MENU' % addon_name)
            xbmc.log('[%s]: HomeScreen PREVIOUS_MENU focusid - %s' % (addon_name, focusid))
            if focusid in [6000, 7001, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010]:
                xbmc.executebuiltin("Control.SetFocus(6000)")
            else:
                xbmc.executebuiltin("Control.SetFocus(6000)")
                xbmc.log('[%s]: Try to kill script' % addon_name)
                self.close()
                PopWindowStack(self)
                xbmc.log('[%s]: script not killed' % addon_name)

        elif action in self.ACTION_EXIT_SCRIPT:
            xbmc.executebuiltin("Control.SetFocus(6000)")
            self.close()

        elif action in self.ACTION_RIGHT_CLICK:
            xbmc.log('[%s]: HomeScreen ACTION_RIGHT_CLICK' % addon_name)
            xbmc.log('[%s]: HomeScreen ACTION_RIGHT_CLICK focusid - %s' % (addon_name, focusid))
            if focusid in [6000, 7001, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010]:
                xbmc.executebuiltin("Control.SetFocus(6000)")
            else:
                xbmc.log('[%s]: Try to kill script' % addon_name)
                self.close()
                PopWindowStack(self)
                xbmc.log('[%s]: script not killed' % addon_name)

        elif action in self.ACTION_CONTEX_MENU:
            item_id = self.getControl(focusid).getSelectedItem().getProperty("id")
            xbmc.log('[%s]: ACTION_CONTEX_MENU item id - %s' % (addon_name, item_id))


    def onClick(self, controlID):
        #self.windowid = xbmcgui.getCurrentWindowDialogId()
        #xbmc.log('[%s]: WindowID - %s' % (addon_name, self.windowid))
        #self.window = xbmcgui.Window(self.windowid)
        if controlID in [500]:
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            pos = self.getControl(controlID).getSelectedPosition()		# In slider first item is last in listitems, so need -1
            AddToWindowStack(self, "%d, %d" % (controlID, pos))
            self.close()
            if (pos-1) < 0:
                pos = self.slider_len-1
            else:
                pos -= 1

            video_id = self.getControl(controlID).getListItem(pos).getProperty("id")
            video_type = self.getControl(controlID).getListItem(pos).getProperty("type")

            xbmc.log('[%s]: 500 id - %s, type - %s' % (addon_name, video_id, video_type))

            if video_type == 'video':
                dialog = VideoInfo.VideoInfo(u'VideoInfo.xml', addon_path, id=video_id, vtype=video_type)
                dialog.doModal()
            elif video_type == 'collection':
                link = 'video/collection?id=%s' % video_id
                dialog = VideoList.VideoList(u'VideoList.xml', addon_path, page=link)
                dialog.doModal()

        elif controlID in [501]:
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            AddToWindowStack(self, "%d, %d" % (controlID, self.getControl(controlID).getSelectedPosition()))
            self.close()
            video_id = self.getControl(controlID).getSelectedItem().getProperty("id")
            video_type = self.getControl(controlID).getSelectedItem().getProperty("type")
            xbmc.log('[%s]: 501 id - %s, type - %s' % (addon_name, video_id, video_type))

            if video_type == 'video':
                dialog = VideoInfo.VideoInfo(u'VideoInfo.xml', addon_path, id=video_id, vtype=video_type)
                dialog.doModal()
            elif video_type == 'collection':
                link = 'video/collection?id=%s' % video_id
                dialog = VideoList.VideoList(u'VideoList.xml', addon_path, page=link)
                dialog.doModal()

        elif controlID in [5001, 5002]:
            pos = self.getControl(500).getSelectedPosition()
            if controlID == 5001:
                if (pos-1) < 0:
                    pos = self.slider_len-1
                else:
                    pos -= 1
            else:
                if (pos+1) > (self.slider_len-1):
                    pos = 0
                else:
                    pos += 1
            self.getControl(500).selectItem(pos)

        elif controlID in [6000]:
            xbmc.executebuiltin("Control.SetFocus(7000)")

        elif controlID in [8000]:
            search = open_keyboard('search')
            link = 'search?text=%s' % urllib.quote_plus(search)
            AddToWindowStack(self, controlID)
            self.close()
            dialog = VideoList.VideoList(u'VideoList.xml', addon_path, page=link)
            dialog.doModal()

        elif controlID in self.MENU_IDS:
            if controlID == 7001:
                self.login()
                return

            elif controlID == 7002:
                page_name = language(1010)
                link = 'subscription'

            elif controlID == 7003:
                page_name = language(1011)
                link = 'premieres'

            elif controlID == 7004:
                page_name = language(1012)
                link = 'video?category_id=%d&limit=100' % megogo2xbmc.get_category_from_db_by_name("'Фильмы'")

            elif controlID == 7005:
                page_name = language(1013)
                link = 'video?category_id=%d&limit=100' % megogo2xbmc.get_category_from_db_by_name("'Сериалы'")

            elif controlID == 7006:
                page_name = language(1014)
                link = 'video?category_id=%d&limit=100' % megogo2xbmc.get_category_from_db_by_name("'TV'")

            elif controlID == 7007:
                page_name = language(1015)
                link = 'collections'

            elif controlID == 7008:
                page_name = language(1016)
                link = 'video?category_id=%d&limit=100' % megogo2xbmc.get_category_from_db_by_name("'Мультфильмы'")

            elif controlID == 7009:
                page_name = language(1017)
                link = 'video?category_id=%d&limit=100' % megogo2xbmc.get_category_from_db_by_name("'Передачи и шоу'")

            elif controlID == 7010:
                if self.logged_in:
                    page_name = language(1018)
                    link = 'user/favorites'
                else:
                    self.login()

            xbmc.executebuiltin("Control.SetFocus(6000)")
            AddToWindowStack(self, controlID)
            self.close()
            dialog = VideoList.VideoList(u'VideoList.xml', addon_path, page=link, name=page_name, wid=controlID)
            dialog.doModal()

    def login(self):
        if self.logged_in:
            xbmc.executebuiltin("Control.SetFocus(9999)")
        else:
            xbmc.executebuiltin("Control.SetFocus(6000)")
            dialog = xbmcgui.Dialog()
            if dialog.yesno(language(1025), language(1026)) == 1:
                usr = open_keyboard('user')
                pwd = open_keyboard('password')
                if not megogo2xbmc.checkLogin(usr=usr, pwd=pwd):
                    self.login()
            else:
                xbmc.executebuiltin("Control.SetFocus(7001)")
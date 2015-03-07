# -*- coding: utf-8 -*-
#############################################################################
#
#	Copyright (C) 2015 Studio-Evolution
#
#	Show video list from MEGOGO.NET for XBMC
#
#############################################################################

import xbmc, xbmcgui, xbmcaddon
from Utils import *
import VideoInfo

addon			= xbmcaddon.Addon()
addon_name		= addon.getAddonInfo('name')
addon_path		= addon.getAddonInfo('path').decode("utf-8")
language		= addon.getLocalizedString

busydialog		= xbmcgui.Window(10138)

class VideoList(xbmcgui.WindowXMLDialog):
    ACTION_PREVIOUS_MENU    = [92, 9]
    ACTION_EXIT_SCRIPT      = [13, 10]
    ACTION_CONTEX_MENU      = [117]
    ACTION_RIGHT_CLICK      = [101]
    MENU_IDS                = [7001, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010]

    def __init__(self, *args, **kwargs):
        self.page = kwargs.get('page')
        self.offset = kwargs.get('offset', 0)
        self.name = kwargs.get('name')
        self.old_id = kwargs.get('wid')
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        self.listitems = update_content(page=self.page, offset=self.offset)
        xbmcgui.WindowXMLDialog.__init__(self)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def onInit(self):
        self.windowid = xbmcgui.getCurrentWindowDialogId()
        self.window = xbmcgui.Window(self.windowid)
        self.window.setProperty("NAME", self.name)

        self.getControl(500).reset()
        self.getControl(500).addItems(self.listitems)

        control = getids()
        if control:
            try:
                if control.isnumeric:
                     xbmc.log('SELECT control.isnumeric %s' % control)
                     xbmc.executebuiltin("Control.SetFocus(%s)" % control)
            except:
                selectedId, _, item = control.partition(', ')
                xbmc.log('SELECT %s %s' % (int(selectedId), int(item)))
                self.setFocusId(int(selectedId))
                self.getControl(int(selectedId)).selectItem(int(item))

    def onAction(self, action):
        focusid = self.getFocusId()
        if action in self.ACTION_PREVIOUS_MENU:
            self.close()
            PopWindowStack(self)

        elif action in self.ACTION_EXIT_SCRIPT:
            self.close()

        elif action in self.ACTION_RIGHT_CLICK:
            self.close()
            PopWindowStack(self)

        elif action in self.ACTION_CONTEX_MENU:
            if self.name == language(1018):
                list_id = self.getControl(focusid).getSelectedItem().getProperty("id")
                xbmc.log("SELECTED CONTEX MENU IN VIDEO LIST, id - %s" % list_id)

                #listitems = language(1030)
                #xbmc.executebuiltin("ActivateWindow(contextmenu)")
                #context_menu = ContextMenu.ContextMenu(u'script-globalsearch-contextmenu.xml', addon_path, labels=listitems)
                #context_menu.doModal()
                #if context_menu.selection == 0:
                #Notify(list_id)
                #selection = xbmcgui.Dialog().select(addon.getLocalizedString(32151), listitems)

    def onClick(self, controlID):
        if controlID in [500]:
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            AddToWindowStack(self, "%d, %d" % (controlID, self.getControl(controlID).getSelectedPosition()))
            self.close()
            video_id = self.getControl(controlID).getSelectedItem().getProperty("id")
            video_type = self.getControl(controlID).getSelectedItem().getProperty("type")
            xbmc.log('[%s]: id - %s, type - %s' % (addon_name, video_id, video_type))
            if video_type == 'video':
                dialog = VideoInfo.VideoInfo(u'VideoInfo.xml', addon_path, id=video_id, vtype=video_type)
                dialog.doModal()

        elif controlID in [8000]:
            search = open_keyboard('search')
            link = 'search?text=%s' % urllib.quote_plus(search)
            AddToWindowStack(self, controlID)
            self.close()
            dialog = VideoList.VideoList(u'VideoList.xml', addon_path, page=link)
            dialog.doModal()

        elif controlID in [6000]:
            xbmc.executebuiltin("Control.SetFocus(7000)")

        elif controlID in self.MENU_IDS and controlID != self.old_id:
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
                page_name = language(1018)
                link = 'user/favorites'

            xbmc.executebuiltin("Control.SetFocus(6000)")
            AddToWindowStack(self, controlID)
            self.close()
            dialog = VideoList(u'VideoList.xml', addon_path, page=link, name=page_name, wid=controlID)
            dialog.doModal()
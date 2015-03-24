# -*- coding: utf-8 -*- 
#############################################################################
#
# Copyright (C) 2015 Studio-Evolution
#
# All screens of addon MEGOGO.NET for XBMC
#
#############################################################################

import xbmc, xbmcgui, xbmcaddon
import urllib, time, re, megogo2xbmc
from sqlite import DataBase
from Utils import *

db = DataBase()

__addon__			    = xbmcaddon.Addon(id='plugin.video.megogo')
addon_id                = __addon__.getAddonInfo('id')
addon_name		        = __addon__.getAddonInfo('name')
addon_path		        = __addon__.getAddonInfo('path').decode("utf-8")
addon_version	        = __addon__.getAddonInfo('version')
language		        = __addon__.getLocalizedString
SkinFolder		        = os.path.join(addon_path, 'resources', 'skins', 'Default', '1080i')
MediaFolder		        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media')
LibFolder		        = os.path.join(addon_path, 'resources', 'lib')
quality_logo	        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'icons', 'FullHD_logo.png')
icon_svod		        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'icons', 'megogo_plus.png')
icon_tvod		        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'icons', 'megogo_payment.png')
unknown_person	        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'unknown_person.png')
credit_card             = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'dialogs', 'Credit_card.png')
flag_en			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'en.png')
flag_ru			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'ru.png')
flag_ua			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'ua.png')
flag_lv			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'lv.png')
flag_lt			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'lt.png')
flag_ee			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'ee.png')
flag_ge			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'ge.png')
flag_kz			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'kz.png')
flag_be			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'be.png')
flag_kg			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'kg.png')
flag_cz			        = os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'cz.png')

ACTION_PREVIOUS_MENU    = [9, 92]
ACTION_EXIT_SCRIPT      = [10, 13]
ACTION_CONTEX_MENU      = [117]
ACTION_MOUSE_RIGHT_CLICK= [101]
MENU_IDS                = [7000, 7001, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010]
country_array           = ['en', 'ru', 'ua', 'lv', 'lt', 'ee', 'ge', 'kz', 'be', 'kg', 'cz']
busydialog		        = xbmcgui.Window(10138)

MovieID = db.get_category_from_db_by_name("'%s'" % language(1012))
SerialID = db.get_category_from_db_by_name("'%s'" % language(1013))
TVID = db.get_category_from_db_by_name("'%s'" % language(1014))
CartoonsID = db.get_category_from_db_by_name("'%s'" % language(1016))
ProgramsID = db.get_category_from_db_by_name("'%s'" % language(1017))

#####################################################################################################
# ##################################	  MAIN   SCREEN		####################################### #
#####################################################################################################
class Main:

    # Initialization
    def __init__(self, **kwargs):
        splash = kwargs.get('splash')

        from Utils import FileDoOpen, FileDoSave

        # ##################################	Work with colors	####################################### #
        if __addon__.getSetting('last-text-color') == '':
            __addon__.setSetting(id='last-text-color', value='FFFAFAFA')

        value = __addon__.getSetting('text-color')
        try:
            TextColor = value.split(']', 1)[0].split(' ')[1]
            ColorName = value.split(']', 1)[1].split('[')[0]

            # re_current_color_diffuse 	= re.compile(ur'<colordiffuse>0x([^<]*)</colordiffuse>')
            # try: current_color_diffuse 	= re.search(re_current_color_diffuse, File).group(1)
            # except: current_color_diffuse= ''
            # if (current_color_diffuse!=SkinColor and current_color_diffuse!=''):
            #	File=File.replace('<colordiffuse>0x%s</colordiffuse>' % current_color_diffuse, '<colordiffuse>0x%s</colordiffuse>' % SkinColor)	# Find and replace color diffuse in skin
            #	xbmc.log('[%s]: diffuse color changed' % addon_name)
        except:
            TextColor = 'FFFAFAFA'
            ColorName = 'Original'

        if __addon__.getSetting('last-text-color') != TextColor:
            xbmc.log('[%s]: chosen new text color - %s (%s)' % (addon_name, TextColor, ColorName))
            try:
                for name in os.listdir(SkinFolder):
                    if name.endswith('.xml'):
                        Fil = FileDoOpen(os.path.join(SkinFolder, name))

                        re_current_color_text = re.compile(ur'<textcolor>([^<]*)</textcolor>')
                        try:
                            current_color_text = re.search(re_current_color_text, Fil).group(1)
                        except:
                            current_color_text = ''

                        if current_color_text != TextColor.upper() and current_color_text != '':
                            Fil = Fil.replace('<textcolor>%s</textcolor>' % current_color_text, '<textcolor>%s</textcolor>' % TextColor.upper())		# Find and replace color text in skin
                            __addon__.setSetting(id='last-text-color', value=TextColor.upper())
                            xbmc.log('[%s]: text color changed' % addon_name)
                        FileDoSave(os.path.join(SkinFolder, name), Fil)
            except:
                xbmc.log('[%s]: cannot change skin colors!' % addon_name)
        else:
            xbmc.log('[%s]: colors settings not changed' % addon_name)

        # ##################################	Start Home Screen	####################################### #
        home = Homescreen('HomeScreen.xml', addon_path, win=splash)
        home.doModal()

        del home


#####################################################################################################
# ##################################	  HOME   SCREEN		####################################### #
#####################################################################################################
class Homescreen(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        self.splash = kwargs.get('win', None)
        megogo2xbmc.checkLogin()
        fetch_data(page='tarification')						                        # Get tarification from MEGOGO
        self.listitems = update_content(page='Main', section='slider')
        self.slider_len = len(self.listitems)
        xbmcgui.WindowXMLDialog.__init__(self)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def onInit(self):
        if self.splash:
            self.splash.close()

        self.getControl(500).reset()
        self.getControl(500).addItems(self.listitems)

        item = CreateListItems(fetch_data(page='Main', section='recommended'))
        self.getControl(501).reset()
        self.getControl(501).addItems(item)

        control = getids()
        if control:
            xbmc.log('!!! CONTROL !!! %s' % control)
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
        if action in ACTION_PREVIOUS_MENU:
            xbmc.log('[%s]: HomeScreen PREVIOUS_MENU' % addon_name)
            xbmc.log('[%s]: HomeScreen PREVIOUS_MENU focusid - %s' % (addon_name, focusid))
            if focusid in MENU_IDS:
                xbmc.executebuiltin("Control.SetFocus(6000)")
            else:
                # xbmc.executebuiltin("Control.SetFocus(6000)")
                xbmc.log('[%s]: Try to kill script' % addon_name)
                closer(self)
                return

        elif action in ACTION_EXIT_SCRIPT:
            # xbmc.executebuiltin("Control.SetFocus(6000)")
            closer(self)
            return

        elif action in ACTION_MOUSE_RIGHT_CLICK:
            xbmc.log('[%s]: HomeScreen ACTION_MOUSE_RIGHT_CLICK' % addon_name)
            xbmc.log('[%s]: HomeScreen ACTION_MOUSE_RIGHT_CLICK focusid - %s' % (addon_name, focusid))
            if focusid in MENU_IDS:
                xbmc.executebuiltin("Control.SetFocus(6000)")
            else:
                xbmc.log('[%s]: Try to kill script' % addon_name)
                closer(self)
                return

        elif action in ACTION_CONTEX_MENU:
            item_id = self.getControl(focusid).getSelectedItem().getProperty("id")
            xbmc.log('[%s]: ACTION_CONTEXT_MENU item id - %s' % (addon_name, item_id))
            # closer(self)

    def onClick(self, controlID):
        if controlID in [500]:
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            pos = self.getControl(controlID).getSelectedPosition()		# In slider first item is last in listitems, need -1
            AddToWindowStack(self, "%d, %d" % (controlID, pos))
            self.close()
            if (pos-1) < 0:
                pos = self.slider_len-1
            else:
                pos -= 1

            video_id = self.getControl(controlID).getListItem(pos).getProperty("id")
            video_type = self.getControl(controlID).getListItem(pos).getProperty("type")
            if video_type == 'video':
                dialog = VideoInfo(u'VideoInfo.xml', addon_path, id=video_id, vtype=video_type)
                dialog.doModal()
            elif video_type == 'collection':
                link = 'video/collection?id=%s' % video_id
                dialog = VideoList(u'VideoList.xml', addon_path, page=link)
                dialog.doModal()

        elif controlID in [501]:
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            AddToWindowStack(self, "%d, %d" % (controlID, self.getControl(controlID).getSelectedPosition()))
            self.close()
            video_id = self.getControl(controlID).getSelectedItem().getProperty("id")
            video_type = self.getControl(controlID).getSelectedItem().getProperty("type")
            if video_type == 'video':
                dialog = VideoInfo(u'VideoInfo.xml', addon_path, id=video_id, vtype=video_type)
                dialog.doModal()

                del dialog

            elif video_type == 'collection':
                link = 'video/collection?id=%s' % video_id
                dialog = VideoList(u'VideoList.xml', addon_path, page=link)
                dialog.doModal()

                del dialog

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
            open_search(self)

        elif controlID in MENU_IDS:
            menu_chooser(self, controlID)


#####################################################################################################
# ###################################	  VIDEO    LISTS	####################################### #
#####################################################################################################
class VideoList(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        self.page = kwargs.get('page', '')
        self.offset = kwargs.get('offset', 0)
        self.name = kwargs.get('name', '')
        self.old_id = kwargs.get('wid')
        if self.page.startswith('video/collection'):
            self.name = get_title(self.page)
        if self.page.startswith('subscription'):
            self.newpage = "%s&category_id=%d" % (self.page, MovieID)
        else:
            self.newpage = self.page
        self.listitems = update_content(force=True, page=self.newpage, offset=self.offset)
        self.items_len = len(self.listitems)
        xbmcgui.WindowXMLDialog.__init__(self)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def onInit(self):
        self.windowid = xbmcgui.getCurrentWindowDialogId()
        self.window = xbmcgui.Window(self.windowid)
        self.window.setProperty("NAME", "%s (%s %d)" % (self.name, language(1042), self.offset/100+1))
        xbmc.log('[%s]: offset - %s, len - %s' % (addon_name, self.offset, self.items_len))

        if self.items_len == 0:
            self.window.setProperty("EMPTY", 'True')
        if self.offset == 0 and self.items_len == 100:
            self.window.setProperty("FIRST_PAGE", 'True')
        elif self.offset > 0 and self.items_len == 100:
            self.window.setProperty("PAGE", 'True')
        elif self.offset > 0 and self.items_len < 100:
            self.window.setProperty("LAST_PAGE", 'True')

        self.getControl(500).reset()
        self.getControl(500).addItems(self.listitems)
        xbmc.executebuiltin("Control.SetFocus(500, 1)")

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

    # def onFocus(self, control):
    #    if control == 6002 and self.window.getProperty('LAST_PAGE') == 'True':
    #        xbmc.executebuiltin('Control.SetFocus(6001)')

    def onFocus(self, control):
        # ###### VideoList.xml ###### #
        if control == 7011 and self.newpage != self.page:
            self.newpage = self.page
            items = self.listitems
            self.getControl(500).reset()
            self.getControl(500).addItems(items)
        elif control == 7012 and self.newpage.find('sort=add') == -1:
            self.newpage = "%s&sort=add" % self.page
            items = update_content(force=False, page=self.newpage, offset=self.offset)
            self.getControl(500).reset()
            self.getControl(500).addItems(items)
        elif control == 7013 and self.newpage.find('sort=popular') == -1:
            self.newpage = "%s&sort=popular" % self.page
            items = update_content(force=False, page=self.newpage, offset=self.offset)
            self.getControl(500).reset()
        # ###### SubscribeList.xml ###### #
        elif control == 7014 and self.newpage.find('category_id=%d' % SerialID) == -1:
            self.newpage = "%s&category_id=%d" % (self.page, SerialID)
            items = update_content(force=False, page=self.newpage, offset=self.offset)
            self.getControl(500).reset()
            self.getControl(500).addItems(items)


    def onAction(self, action):
        actions = action.getId()
        xbmc.log('[%s]: ACTION! buttonCODE - %s, id - %s' % (addon_name, action.getButtonCode(), action.getId()))
        focusid = self.getFocusId()
        if actions in ACTION_PREVIOUS_MENU:
            xbmc.log('[%s]: VideoList PREVIOUS_MENU focusid - %s' % (addon_name, focusid))
            if focusid in MENU_IDS:
                xbmc.executebuiltin("Control.SetFocus(6000)")
            elif focusid in [500]:
                xbmc.log('!! SELF.PAGE !!! %s' % self.page)
                if self.newpage.find('sort=add') > 0:
                    button_id = 7012
                elif self.newpage.find('sort=popular') > 0:
                    button_id = 7013
                else:
                    button_id = 7011
                xbmc.executebuiltin("Control.SetFocus(%d)" % button_id)
            else:
                xbmc.executebuiltin("Control.SetFocus(6000)")
                self.close()
                PopWindowStack(self)

        elif actions in ACTION_EXIT_SCRIPT:
            exit_to_main(self)

        elif actions in ACTION_CONTEX_MENU or action in ACTION_MOUSE_RIGHT_CLICK:
            if self.name == language(1018):
                item_id = self.getControl(focusid).getSelectedItem().getProperty("id")
                xbmc.log('[%s]: VideoList ACTION_CONTEXT_MENU item id - %s' % (addon_name, item_id))

        # listitems = language(1030)
        # xbmc.executebuiltin("ActivateWindow(contextmenu)")
        # context_menu = ContextMenu.ContextMenu(u'script-globalsearch-contextmenu.xml', addon_path, labels=listitems)
        # context_menu.doModal()
        # if context_menu.selection == 0:
        # Notify(list_id)
        # selection = xbmcgui.Dialog().select(__addon__.getLocalizedString(32151), listitems)

    def onClick(self, controlID):
        if controlID in [500]:
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            AddToWindowStack(self, "%d, %d" % (controlID, self.getControl(controlID).getSelectedPosition()))
            self.close()
            video_id = self.getControl(controlID).getSelectedItem().getProperty("id")
            video_type = self.getControl(controlID).getSelectedItem().getProperty("type")
            xbmc.log('[%s]: id - %s, type - %s' % (addon_name, video_id, video_type))
            if video_type == 'video' and self.page != 'collections':
                dialog = VideoInfo(u'VideoInfo.xml', addon_path, id=video_id, vtype=video_type)
            elif self.page == 'collections':
                link = 'video/collection?id=%s' % video_id
                dialog = VideoList(u'VideoList.xml', addon_path, page=link)

            dialog.doModal()
            del dialog

        elif controlID in [8000]:
            open_search(self)

        elif controlID in [6000]:
            xbmc.executebuiltin("Control.SetFocus(7000)")

        elif controlID in MENU_IDS and controlID != self.old_id:
            menu_chooser(self, controlID)

        elif controlID in [7011, 7012, 7013]:
            xbmc.executebuiltin("Control.SetFocus(500)")

        elif controlID in [6001, 6002]:
            if controlID == 6001:
                offset = self.offset - 100
            elif controlID == 6002:
                offset = self.offset + 100
            AddToWindowStack(self, controlID)
            self.close()
            dialog = VideoList(u'VideoList.xml', addon_path, page=self.page, offset=offset, name=self.name, wid=self.old_id)
            dialog.doModal()
            del dialog


#####################################################################################################
# ###################################	  SEASONS  LISTS	####################################### #
#####################################################################################################
class SeasonList(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        self.movieplayer = VideoPlayer(popstack=True)
        self.thumb = kwargs.get('thumb', None)
        self.name = kwargs.get('name')
        self.seasons = kwargs.get('seasons', None)
        self.episode_list = kwargs.get('episodes', None)
        self.listitems = []
        self.series = []
        if self.seasons:
            for (counter, season) in enumerate(sorted(self.seasons, key=lambda k: k['title'])):
                item = xbmcgui.ListItem('%s' % (str(counter)))
                if season['title_original']:
                    label = '%s (%s)' % (season['title'], season['title_original'])
                else:
                    label = season['title']
                item.setLabel(label)
                item.setThumbnailImage(self.thumb)
                item.setProperty('id', unicode(season['id']))
                self.listitems.append(item)
        if self.episode_list:
            for (counter, episode) in enumerate(self.episode_list):
                episode_item = xbmcgui.ListItem('%s' % (str(counter)))
                if episode['title_original']:
                    label = '%s (%s)' % (episode['title'], episode['title_original'])
                else:
                    label = episode['title']
                episode_item.setLabel(label)
                Get_File(episode['image'])
                episode_item.setThumbnailImage(episode['image'])
                episode_item.setProperty('id', unicode(episode['id']))
                self.series.append(episode_item)
        xbmcgui.WindowXMLDialog.__init__(self)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def onInit(self):
        self.windowid = xbmcgui.getCurrentWindowDialogId()
        self.window = xbmcgui.Window(self.windowid)
        self.window.setProperty("NAME", self.name)

        if self.seasons:
            self.getControl(500).reset()
            self.getControl(500).addItems(self.listitems)
        elif self.episode_list:
            self.getControl(501).reset()
            self.getControl(501).addItems(self.series)

        control = getids()
        if control:
            try:
                if control.isnumeric:
                    xbmc.log('SELECT control.isnumeric %s' % control)
                    xbmc.executebuiltin("Control.SetFocus(%s)" % control)
            except:
                xbmc.log('[%s]: !!!CONTROL!!! %s' % (addon_name, control))
                selectedId, _, item = control.partition(', ')
                xbmc.log('SELECT %s %s' % (int(selectedId), int(item)))
                self.setFocusId(int(selectedId))
                self.getControl(int(selectedId)).selectItem(int(item))

    def onAction(self, action):
        focusid = self.getFocusId()
        if action in ACTION_PREVIOUS_MENU:
            xbmc.log('[%s]: SeasonList PREVIOUS_MENU' % addon_name)
            xbmc.log('[%s]: SeasonList PREVIOUS_MENU focusid - %s' % (addon_name, focusid))
            if focusid in MENU_IDS:
                xbmc.executebuiltin("Control.SetFocus(6000)")
            else:
                xbmc.executebuiltin("Control.SetFocus(6000)")
                xbmc.log('[%s]: Try to kill script' % addon_name)
                self.close()
                PopWindowStack(self)

        elif action in ACTION_EXIT_SCRIPT:
            exit_to_main(self)

        elif action in ACTION_CONTEX_MENU or action in ACTION_MOUSE_RIGHT_CLICK:
            if self.name == language(1018):
                item_id = self.getControl(focusid).getSelectedItem().getProperty("id")
                xbmc.log('[%s]: SeasonList ACTION_CONTEXT_MENU item id - %s' % (addon_name, item_id))

        # listitems = language(1030)
        # xbmc.executebuiltin("ActivateWindow(contextmenu)")
        # context_menu = ContextMenu.ContextMenu(u'script-globalsearch-contextmenu.xml', addon_path, labels=listitems)
        # context_menu.doModal()
        # if context_menu.selection == 0:
        # Notify(list_id)
        # selection = xbmcgui.Dialog().select(__addon__.getLocalizedString(32151), listitems)

    def onClick(self, controlID):
        if controlID in [500]:
            pos = self.getControl(500).getSelectedPosition()
            label = self.getControl(500).getListItem(pos).getLabel()
            if pos == 0:
                episodes = self.seasons[0]['episode_list']
            else:
                xbmc.executebuiltin("ActivateWindow(busydialog)")
                sid = self.getControl(500).getListItem(pos).getProperty("id")
                episodes = fetch_data(page='video/episodes?id=%s' % sid)
            AddToWindowStack(self, "%d, %d" % (controlID, pos))
            self.close()
            dialog = SeasonList(u'EpisodeList.xml', addon_path, episodes=episodes, name='%s (%s)' % (self.name, label.decode('utf-8')), thumb=self.thumb)
            dialog.doModal()
            del dialog

        elif controlID in [501]:
            pos = self.getControl(501).getSelectedPosition()
            sid = self.getControl(501).getListItem(pos).getProperty("id")
            label = self.getControl(501).getListItem(pos).getLabel()
            link, audio, subtitle = megogo2xbmc.get_stream(sid)
            listitem = xbmcgui.ListItem(label, iconImage=self.thumb, thumbnailImage=self.thumb)
            listitem.setInfo('video', {'Title': '%s, %s)' % (self.name[:-1], label.decode('utf-8'))})
            AddToWindowStack(self, "%d, %d" % (controlID, pos))
            self.close()
            self.movieplayer.play_item(link, listitem, subtitle)
            self.movieplayer.WaitForVideoEnd()
            PopWindowStack(self)

        elif controlID in [8000]:
            open_search(self)

        elif controlID in [6000]:
            xbmc.executebuiltin("Control.SetFocus(7000)")

        elif controlID in MENU_IDS and controlID != self.old_id:
            menu_chooser(self, controlID)


#####################################################################################################
# ##################################	  VIDEO    INFO		####################################### #
#####################################################################################################
class VideoInfo(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        self.movieplayer = VideoPlayer(popstack=True)
        self.vid = kwargs.get('id', None)
        self.vtype = kwargs.get('vtype', None)
        self.data = fetch_data(page=self.vid, section=self.vtype)
        try:
            self.screenshots = self.data['screenshots']
            del self.data['screenshots']
        except:
            self.screenshots = None
        try:
            self.actors = self.data['crew']
            del self.data['crew']
            # xbmc.log('CREW: - %s' % self.actors)
        except:
            self.actors = None
        try:
            self.season = self.data['season_list']
            del self.data['season_list']
        except:
            self.season = None

        self.bitrates, self.audio_list, self.subtitles = megogo2xbmc.data_from_stream(self.data["id"])

        xbmcgui.WindowXMLDialog.__init__(self)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def onInit(self):
        self.windowid = xbmcgui.getCurrentWindowDialogId()
        self.window = xbmcgui.Window(self.windowid)
        if self.data['quality'] != '':
            self.window.setProperty("Quality", quality_logo)
        else:
            self.window.setProperty("Quality", '')
        if self.data['imdb_rating'] != '':
            self.window.setProperty("imdb_rating", self.data["imdb_rating"])
        else:
            self.window.setProperty("imdb_rating", '')
        if self.data['rating'] != '':
            self.window.setProperty("kinopoisk_rating", self.data["rating"])
        else:
            self.window.setProperty("kinopoisk_rating", '')
        if self.data['exclusive'] in ['True', 'true']:
            self.window.setProperty("exclusive", 'True')
        else:
            self.window.setProperty("exclusive", '')
        if self.data['series'] in ['True', 'true']:
            self.window.setProperty("series", 'True')
        else:
            self.window.setProperty("series", '')
        if self.data["delivery_rules"] != '':
            for delivery in self.data["delivery_rules"].split(', '):
                if delivery == 'svod':
                    self.window.setProperty("Price", "%s %s" % (language(1000), megogo2xbmc.get_price('svod')))
                elif delivery == 'tvod':
                    self.window.setProperty("Price", "%s %s %s" % (language(1001), self.data['price'], self.data['currency']))
                try:
                    self.window.setProperty("%s" % delivery.upper(), globals()['icon_%s' % delivery])
                except:
                    pass
        if self.audio_list:
            for audio in self.audio_list:
                try:
                    self.window.setProperty("Audio_Language_%s" % audio.upper(), globals()['flag_%s' % audio])
                except:
                    pass
        if self.subtitles:
            for subtitle in self.subtitles:
                try:
                    self.window.setProperty("Subtitle_Language_%s" % subtitle.upper(), globals()['flag_%s' % subtitle])
                except:
                    pass
        if self.data['originaltitle'] != '':
            title = '%s (%s)' % (self.data["title"], self.data['originaltitle'])
        else:
            title = self.data["title"]

        self.getControl(33000).setText(title)
        self.getControl(33001).setImage(self.data["poster"])
        self.getControl(33002).setText("%s, %s, %s" % (self.data["year"], self.data["country"], self.data["genre"]))
        self.getControl(33004).setText(self.data["plot"])
        self.getControl(33005).setText(self.data["duration"])
        self.getControl(33006).setText(self.data["like"])
        self.getControl(33007).setText(self.data["dislike"])
        self.getControl(33008).setText('%s: %s+' % (language(1005), self.data["mpaa"].encode('utf-8')))

        control = getids()
        if control:
            xbmc.executebuiltin("Control.SetFocus(%s)" % control)

    def onAction(self, action):
        focusid = self.getFocusId()
        xbmc.log('[%s]: VideoInfo onAction id - %s' % (addon_name, action.getId()))
        # action_id = action.getId()
        if action in ACTION_PREVIOUS_MENU:
            if focusid in [17050, 17051, 17000, 17001, 17002, 17003]:
                xbmc.executebuiltin("Control.SetFocus(33012)")
            elif focusid in [5000]:
                xbmc.executebuiltin("Control.SetFocus(17001)")
            elif focusid in [5001]:
                xbmc.executebuiltin("Control.SetFocus(17002)")
            elif focusid in [5002]:
                xbmc.executebuiltin("Control.SetFocus(17003)")
            else:
                self.close()
                PopWindowStack(self)

        elif action in ACTION_EXIT_SCRIPT:
            exit_to_main(self)

        elif action in ACTION_CONTEX_MENU or action in ACTION_MOUSE_RIGHT_CLICK:
            if focusid in [17050, 17051, 17000, 17001, 17002, 17003]:
                xbmc.executebuiltin("Control.SetFocus(33012)")

            #item_id = self.getControl(focusid).getSelectedItem().getProperty("id")
            #xbmc.log('[%s]: VideoInfo ACTION_CONTEXT_MENU item id - %s' % (addon_name, item_id))

        # elif action in ACTION_MOUSE_RIGHT_CLICK:
        #    # xbmc.log('[%s]: HomeScreen ACTION_MOUSE_RIGHT_CLICK' % addon_name)
        #    if focusid in [17050, 17051, 17000, 17001, 17002, 17003]:
        #        xbmc.executebuiltin("Control.SetFocus(33012)")
        #    elif focusid in [5000]:
        #        xbmc.executebuiltin("Control.SetFocus(17001)")
        #    elif focusid in [5001]:
        #        xbmc.executebuiltin("Control.SetFocus(17002)")
        #    elif focusid in [5002]:
        #        xbmc.executebuiltin("Control.SetFocus(17003)")
        #    else:
        #        self.close()
        #        PopWindowStack(self)

    def onClick(self, controlID):
        if (self.window.getProperty('SVOD') or self.window.getProperty('TVOD')) and controlID in [33003]:
            image = xbmcgui.ControlImage(100, 100, 1720, 880, credit_card)
            self.window.addControl(image)
        elif controlID in [33003]:
            AddToWindowStack(self, controlID)
            self.close()
            if self.window.getProperty("series") == 'True':
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playlist.clear()
                for (position, episode) in enumerate(self.season[0]['episode_list']):
                    link, audio, subtitle = megogo2xbmc.get_stream(episode["id"])
                    if episode['title_original']:
                        label = '%s (%s, %s)' % (self.data['title'], episode['title'], episode['title_original'])
                    else:
                        label = '%s (%s)' % (self.data['title'], episode['title'])
                    episode_item = xbmcgui.ListItem(label, iconImage=self.data["poster"], thumbnailImage=self.data["poster"])
                    episode_item.setInfo('video', {'Title': label})
                    playlist.add(url=link, listitem=episode_item, index=position)
                # listitem = xbmcgui.ListItem(self.data['title'], iconImage=self.data["poster"], thumbnailImage=self.data["poster"])
                # listitem.setInfo('video', {'Title': self.data['title']})
                # self.movieplayer.play_item(playlist, listitem)
                xbmc.Player().play(playlist)
            else:
                link, audio, subtitle = megogo2xbmc.get_stream(self.data["id"])
                listitem = xbmcgui.ListItem(self.data['title'], iconImage=self.data["poster"], thumbnailImage=self.data["poster"])
                listitem.setInfo('video', {'Title': self.data['title']})
                self.movieplayer.play_item(link, listitem, subtitle)
            self.movieplayer.WaitForVideoEnd()
            PopWindowStack(self)

        elif controlID in [33012]:
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            item = CreateActorListItems(self.actors)
            self.getControl(5000).reset()
            self.getControl(5000).addItems(item)

            item = CreateCommentList(self.data["id"])
            self.getControl(5001).reset()
            self.getControl(5001).addItems(item)

            item = CreateListItems(megogo2xbmc.HandleMainPage(self.data["recommended"]))
            self.getControl(5002).reset()
            self.getControl(5002).addItems(item)
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            time.sleep(0.5)
            xbmc.executebuiltin("Control.SetFocus(17000)")

        elif controlID in [33013]:
            AddToWindowStack(self, controlID)
            self.close()
            dialog = SeasonList(u'SeasonList.xml', addon_path, seasons=self.season, thumb=self.data["poster"], name=self.data["title"])
            dialog.doModal()

            del dialog

        elif controlID in [5002]:
            xbmc.log('[%s]: Selected related video - %s' % (addon_name, self.getControl(controlID).getSelectedItem().getProperty("Label")))
            video_id = self.getControl(controlID).getSelectedItem().getProperty("id")
            video_type = self.getControl(controlID).getSelectedItem().getProperty("type")
            if video_type == 'video':
                xbmc.executebuiltin("Control.SetFocus(33012)")
                AddToWindowStack(self, controlID)
                self.close()
                dialog = VideoInfo(u'VideoInfo.xml', addon_path, win=self, id=video_id, vtype=video_type)
                dialog.doModal()

                del dialog

        elif controlID in [17050]:
            xbmc.executebuiltin("Control.SetFocus(33012)")

        elif controlID in [17001]:
            xbmc.executebuiltin("Control.SetFocus(5000)")

        elif controlID in [17002]:
            xbmc.executebuiltin("Control.SetFocus(5001)")

        elif controlID in [17003]:
            xbmc.executebuiltin("Control.SetFocus(5002)")


#####################################################################################################
# ##################################	  ACCOUNT  INFO	    ####################################### #
#####################################################################################################
class Account(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        dic = db.get_login_from_db()
        account_data = megogo2xbmc.log_in(dic['login'], dic['password'])
        if account_data['result'] == 'ok':
            self.user_id = account_data['data']['user_id']
            # self.credit_card = account_data['data']['credit_card']
            # self.card_type = account_data['data']['card_type']
            self.avatar = account_data['data']['avatar']
            self.nickname = account_data['data']['nickname']
            self.email = account_data['data']['email']
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok(language(1025), language(1031))
            del dialog
            self.close()
            PopWindowStack(self)

        if not self.avatar:
            self.avatar = unknown_person
        else:
            Get_File(self.avatar)

        xbmcgui.WindowXMLDialog.__init__(self)
        xbmc.executebuiltin("Dialog.Close(busydialog)")

    def onInit(self):
        self.windowid = xbmcgui.getCurrentWindowDialogId()
        self.window = xbmcgui.Window(self.windowid)

        self.getControl(33000).setText(language(1009))
        self.getControl(33001).setImage(self.avatar)
        self.getControl(33002).setText(self.nickname)
        self.getControl(33003).setText(self.email)
        self.getControl(33004).setText('Megogo ID: %s' % self.user_id)

        # control = getids()
        # if control:
        #    xbmc.executebuiltin("Control.SetFocus(%s)" % control)

    def onAction(self, action):
        xbmc.log('[%s]: Account onAction id - %s' % (addon_name, action.getId()))
        if action in ACTION_PREVIOUS_MENU:
            self.close()
            PopWindowStack(self)

        elif action in ACTION_EXIT_SCRIPT:
            exit_to_main(self)

    def onClick(self, controlID):
        if controlID in [33005]:
            db.clear_table('account')
            __addon__.setSetting(id='login', value='')
            __addon__.setSetting(id='password', value='')
            self.close()
            PopWindowStack(self)

        elif controlID in [33006]:
            listitems = [language(201), language(202), language(203), language(204), language(205), language(206)]
            index = xbmcgui.Dialog().select(language(24), listitems)
            if index == -1:
                pass
            elif index == 0:
                __addon__.setSetting(id='quality', value="0")
            elif index == 1:
                __addon__.setSetting(id='quality', value="1")
            elif index == 2:
                __addon__.setSetting(id='quality', value="2")
            elif index == 3:
                __addon__.setSetting(id='quality', value="3")
            elif index == 4:
                __addon__.setSetting(id='quality', value="4")
            elif index == 5:
                __addon__.setSetting(id='quality', value="5")

        elif controlID in [33007]:
            listitems = [language(300), language(301), language(302), language(303), language(304), language(305),
                         language(306), language(307), language(308), language(309), language(310)]
            index = xbmcgui.Dialog().select(language(25), listitems)
            if index == -1:
                pass
            elif index == 0:
                __addon__.setSetting(id='audio_language', value="0")
            elif index == 1:
                __addon__.setSetting(id='audio_language', value="1")
            elif index == 2:
                __addon__.setSetting(id='audio_language', value="2")
            elif index == 3:
                __addon__.setSetting(id='audio_language', value="3")
            elif index == 4:
                __addon__.setSetting(id='audio_language', value="4")
            elif index == 5:
                __addon__.setSetting(id='audio_language', value="5")
            elif index == 6:
                __addon__.setSetting(id='audio_language', value="6")
            elif index == 7:
                __addon__.setSetting(id='audio_language', value="7")
            elif index == 8:
                __addon__.setSetting(id='audio_language', value="8")
            elif index == 9:
                __addon__.setSetting(id='audio_language', value="9")

        elif controlID in [33008]:
            listitems = [language(400), language(300), language(301), language(302), language(303), language(304),
                         language(305), language(306), language(307), language(308), language(309), language(310)]
            index = xbmcgui.Dialog().select(language(26), listitems)
            if index == -1:
                pass
            elif index == 0:
                __addon__.setSetting(id='subtitle_language', value="0")
            elif index == 1:
                __addon__.setSetting(id='subtitle_language', value="1")
            elif index == 2:
                __addon__.setSetting(id='subtitle_language', value="2")
            elif index == 3:
                __addon__.setSetting(id='subtitle_language', value="3")
            elif index == 4:
                __addon__.setSetting(id='subtitle_language', value="4")
            elif index == 5:
                __addon__.setSetting(id='subtitle_language', value="5")
            elif index == 6:
                __addon__.setSetting(id='subtitle_language', value="6")
            elif index == 7:
                __addon__.setSetting(id='subtitle_language', value="7")
            elif index == 8:
                __addon__.setSetting(id='subtitle_language', value="8")
            elif index == 9:
                __addon__.setSetting(id='subtitle_language', value="9")
            elif index == 10:
                __addon__.setSetting(id='subtitle_language', value="10")


#####################################################################################################
# ##################################	    FUNCTIONS		####################################### #
#####################################################################################################
def login():
    if megogo2xbmc.checkLogin():
        return True
    else:
        xbmc.executebuiltin("Control.SetFocus(6000)")
        dialog = xbmcgui.Dialog()
        if dialog.yesno(language(1025), language(1026)) == 1:
            open_keyboard('login')
            open_keyboard('password')
            if not megogo2xbmc.checkLogin():
                login()
            else:
                return True
        else:
            return False


def open_keyboard(name):
    if name == 'login':
        header = language(1027)
        default_value = __addon__.getSetting(name)
    elif name == 'password':
        header = language(1028)
        default_value = ''
    else:
        header = language(1020)
        default_value = ''

    kbd = xbmc.Keyboard()
    kbd.setHeading(header)
    kbd.setDefault(default_value)
    if name == 'password':
        kbd.setHiddenInput(True)
    kbd.doModal()
    if kbd.isConfirmed():
        text = kbd.getText()
        del kbd
        if text == '':
            dialog = xbmcgui.Dialog()
            dialog.ok(header, language(1029))
            del dialog
            open_keyboard(name)
        elif name != 'search':
            db.update_account_in_db(field=name, data=text)

        return text


def menu_chooser(window, controlID):
    link = ''
    page_name = ''
    xml = None

    if controlID == 7001:
        if login():
            xbmc.executebuiltin("Control.SetFocus(6000)")
            AddToWindowStack(window, controlID)
            window.close()
            dialog = Account(u'Account.xml', addon_path)
            dialog.doModal()
            del dialog
            xbmc.executebuiltin("Control.SetFocus(7001)")
            return
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok(language(1025), language(1031))
            del dialog
            xbmc.executebuiltin("Control.SetFocus(7001)")
            return

    if controlID == 7002:
        page_name = language(1010)
        link = 'subscription?limit=100'
        xml = u'SubscribeList.xml'

    elif controlID == 7003:
        page_name = language(1011)
        link = 'premieres?limit=100'

    elif controlID == 7004:
        page_name = language(1012)
        link = 'video?category_id=%d&limit=100' % MovieID

    elif controlID == 7005:
        page_name = language(1013)
        link = 'video?category_id=%d&limit=100' % SerialID

    elif controlID == 7006:
        page_name = language(1014)
        link = 'video?category_id=%d&limit=100' % TVID

    elif controlID == 7007:
        page_name = language(1015)
        link = 'collections'

    elif controlID == 7008:
        page_name = language(1016)
        link = 'video?category_id=%d&limit=100' % CartoonsID

    elif controlID == 7009:
        page_name = language(1017)
        link = 'video?category_id=%d&limit=100' % ProgramsID

    elif controlID == 7010:
        if login():
            link = 'user/favorites'
            page_name = language(1018)
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok(language(1025), language(1031))
            del dialog
            xbmc.executebuiltin("Control.SetFocus(7010)")
            return

    if not xml:
        xml = u'VideoList.xml'
    xbmc.executebuiltin("Control.SetFocus(6000)")
    AddToWindowStack(window, controlID)
    window.close()
    dialog = VideoList(xml, addon_path, page=link, name=page_name, wid=controlID)
    dialog.doModal()


def open_search(window):
    search = open_keyboard('search')
    link = 'search?text=%s' % urllib.quote_plus(search)
    AddToWindowStack(window, 8000)
    window.close()
    dialog = VideoList(u'VideoList.xml', addon_path, page=link)
    dialog.doModal()
    del dialog


def exit_to_main(window):
    xbmc.executebuiltin("Control.SetFocus(6000)")
    window.close()
    DelWindowStack()
    home = Homescreen('HomeScreen.xml', addon_path)
    home.doModal()
    del home

def closer(window):
    dialog = xbmcgui.Dialog()
    if dialog.yesno(language(1035), language(1036)) == 1:
        del dialog
        db.close_db()
        window.close()
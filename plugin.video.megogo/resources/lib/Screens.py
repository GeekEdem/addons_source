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
from sqlite import DataBase as db
from Utils import *

a = db()

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

ACTION_PREVIOUS_MENU    = [10, 92]
ACTION_EXIT_SCRIPT      = [9, 13]
ACTION_CONTEX_MENU      = [117]
ACTION_MOUSE_RIGHT_CLICK= [101]
MENU_IDS                = [7000, 7001, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010]
country_array           = ['en', 'ru', 'ua', 'lv', 'lt', 'ee', 'ge', 'kz', 'be', 'kg', 'cz']
busydialog		        = xbmcgui.Window(10138)


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
        self.splash = kwargs.get('win')
        xbmc.executebuiltin("ActivateWindow(busydialog)")
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
                xbmc.executebuiltin("Control.SetFocus(6000)")
                xbmc.log('[%s]: Try to kill script' % addon_name)
                closer(self)

        elif action in ACTION_EXIT_SCRIPT:
            xbmc.executebuiltin("Control.SetFocus(6000)")
            closer(self)

        elif action in ACTION_MOUSE_RIGHT_CLICK:
            xbmc.log('[%s]: HomeScreen ACTION_MOUSE_RIGHT_CLICK' % addon_name)
            xbmc.log('[%s]: HomeScreen ACTION_MOUSE_RIGHT_CLICK focusid - %s' % (addon_name, focusid))
            if focusid in MENU_IDS:
                xbmc.executebuiltin("Control.SetFocus(6000)")
            else:
                xbmc.log('[%s]: Try to kill script' % addon_name)
                closer(self)

        elif action in ACTION_CONTEX_MENU:
            item_id = self.getControl(focusid).getSelectedItem().getProperty("id")
            xbmc.log('[%s]: ACTION_CONTEXT_MENU item id - %s' % (addon_name, item_id))

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
            elif video_type == 'collection':
                link = 'video/collection?id=%s' % video_id
                dialog = VideoList(u'VideoList.xml', addon_path, page=link)
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
            dialog = VideoList(u'VideoList.xml', addon_path, page=link)
            dialog.doModal()

        elif controlID in MENU_IDS:
            if controlID == 7001:
                focus = login()
                xbmc.executebuiltin("Control.SetFocus(%s)" % focus)
                return
            else:
                menu_chooser(self, controlID)


#####################################################################################################
# ###################################	  VIDEO    LISTS	####################################### #
#####################################################################################################
class VideoList(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        self.page = kwargs.get('page')
        self.offset = kwargs.get('offset', 0)
        self.name = kwargs.get('name', '')
        self.old_id = kwargs.get('wid')
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        if self.page.startswith('video/collection'):
            self.name = get_title(self.page)
        self.listitems = update_content(force=True, page=self.page, offset=self.offset)
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
        if action in ACTION_PREVIOUS_MENU:
            xbmc.log('[%s]: VideoList PREVIOUS_MENU' % addon_name)
            xbmc.log('[%s]: VideoList PREVIOUS_MENU focusid - %s' % (addon_name, focusid))
            if focusid in MENU_IDS:
                xbmc.executebuiltin("Control.SetFocus(6000)")
            else:
                xbmc.executebuiltin("Control.SetFocus(6000)")
                xbmc.log('[%s]: Try to kill script' % addon_name)
                self.close()
                PopWindowStack(self)

        elif action in ACTION_EXIT_SCRIPT:
            xbmc.executebuiltin("Control.SetFocus(6000)")
            closer(self)

        elif action in ACTION_CONTEX_MENU or action in ACTION_MOUSE_RIGHT_CLICK:
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
                dialog.doModal()
            elif self.page == 'collections':
                link = 'video/collection?id=%s' % video_id
                dialog = VideoList(u'VideoList.xml', addon_path, page=link)
                dialog.doModal()

        elif controlID in [8000]:
            search = open_keyboard('search')
            link = 'search?text=%s' % urllib.quote_plus(search)
            AddToWindowStack(self, controlID)
            self.close()
            dialog = VideoList(u'VideoList.xml', addon_path, page=link)
            dialog.doModal()

        elif controlID in [6000]:
            xbmc.executebuiltin("Control.SetFocus(7000)")

        elif controlID in MENU_IDS and controlID != self.old_id:
            if controlID == 7001:
                focus = login()
                xbmc.executebuiltin("Control.SetFocus(%s)" % focus)
                return
            else:
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

        # xbmc.log('[%s]: data - %s' % (addon_name, data))
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
            xbmc.executebuiltin("Control.SetFocus(33003)")
            closer(self)

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
        #if self.window.getProperty('SVOD'):
        #    xbmc.log('!!![SVOD]: %s' % self.window.getProperty('SVOD'))
        #if self.window.getProperty('TVOD'):
        #    xbmc.log('!!![TVOD]: %s' % self.window.getProperty('TVOD'))

        if controlID in [33003]:
            link, audio, subtitle = megogo2xbmc.get_stream(self.data["id"])
            listitem = xbmcgui.ListItem(self.data['title'], iconImage=self.data["poster"], thumbnailImage=self.data["poster"])
            listitem.setInfo('video', {'Title': self.data['title']})
            AddToWindowStack(self, controlID)
            self.close()
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

        elif controlID in [17050]:
            xbmc.executebuiltin("Control.SetFocus(33012)")

        elif controlID in [17001]:
            xbmc.executebuiltin("Control.SetFocus(5000)")

        elif controlID in [17002]:
            xbmc.executebuiltin("Control.SetFocus(5001)")

        elif controlID in [17003]:
            xbmc.executebuiltin("Control.SetFocus(5002)")


#####################################################################################################
# ##################################	    FUNCTIONS		####################################### #
#####################################################################################################
def login():
    if megogo2xbmc.checkLogin():
        return 9999
    else:
        xbmc.executebuiltin("Control.SetFocus(6000)")
        dialog = xbmcgui.Dialog()
        if dialog.yesno(language(1025), language(1026)) == 1:
            open_keyboard('login')
            open_keyboard('password')
            if not megogo2xbmc.checkLogin():
                login()
        else:
            return 7001


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
            a.update_account_in_db(field=name, data=text)

        return text


def menu_chooser(window, controlID):
    link = ''
    page_name = ''

    if controlID == 7002:
        page_name = language(1010)
        link = 'subscription'

    elif controlID == 7003:
        page_name = language(1011)
        link = 'premieres'

    elif controlID == 7004:
        page_name = language(1012)
        link = 'video?category_id=%d&limit=100' % a.get_category_from_db_by_name("'Фильмы'")

    elif controlID == 7005:
        page_name = language(1013)
        link = 'video?category_id=%d&limit=100' % a.get_category_from_db_by_name("'Сериалы'")

    elif controlID == 7006:
        page_name = language(1014)
        link = 'video?category_id=%d&limit=100' % a.get_category_from_db_by_name("'TV'")

    elif controlID == 7007:
        page_name = language(1015)
        link = 'collections'

    elif controlID == 7008:
        page_name = language(1016)
        link = 'video?category_id=%d&limit=100' % a.get_category_from_db_by_name("'Мультфильмы'")

    elif controlID == 7009:
        page_name = language(1017)
        link = 'video?category_id=%d&limit=100' % a.get_category_from_db_by_name("'Передачи и шоу'")

    elif controlID == 7010:
        if not megogo2xbmc.checkLogin():
            login()
        link = 'user/favorites'
        page_name = language(1018)

    xbmc.executebuiltin("Control.SetFocus(6000)")
    AddToWindowStack(window, controlID)
    window.close()
    dialog = VideoList(u'VideoList.xml', addon_path, page=link, name=page_name, wid=controlID)
    dialog.doModal()


def closer(window):
    dialog = xbmcgui.Dialog()
    if dialog.yesno(language(1035), language(1036)) == 1:
        a.close_db()
        window.close()
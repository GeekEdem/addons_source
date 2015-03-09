# -*- coding: utf-8 -*- 
#############################################################################
#
#	Copyright (C) 2015 Studio-Evolution
#
#	Default information of video MEGOGO.NET for XBMC
#
#############################################################################

import xbmc, xbmcgui, xbmcaddon, time
from Utils import *

addon			= xbmcaddon.Addon()
addon_name		= addon.getAddonInfo('name')
addon_path		= addon.getAddonInfo('path').decode("utf-8")
language		= addon.getLocalizedString
quality_logo	= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'icons', 'FullHD_logo.png')
icon_svod		= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'icons', 'megogo_plus.png')
icon_tvod		= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'icons', 'megogo_payment.png')
flag_en			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'en.png')
flag_ru			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'ru.png')
flag_ua			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'ua.png')
flag_lv			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'lv.png')
flag_lt			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'lt.png')
flag_ee			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'ee.png')
flag_ge			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'ge.png')
flag_kz			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'kz.png')
flag_be			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'be.png')
flag_kg			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'kg.png')
flag_cz			= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'flags', 'cz.png')

country_array = ['en', 'ru', 'ua', 'lv', 'lt', 'ee', 'ge']

busydialog		= xbmcgui.Window(10138)

class VideoInfo(xbmcgui.WindowXMLDialog):
    ACTION_PREVIOUS_MENU    = [92, 9]
    ACTION_EXIT_SCRIPT      = [13, 10]
    ACTION_CONTEX_MENU      = [117]
    ACTION_RIGHT_CLICK      = [101]

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
            #xbmc.log('CREW: - %s' % self.actors)
        except:
            self.actors = None
        try:
            self.season = self.data['season_list']
            del self.data['season_list']
        except:
            self.season = None

        self.bitrates, self.audio_list, self.subtitles = megogo2xbmc.data_from_stream(self.data["id"])

        #xbmc.log('[%s]: data - %s' % (addon_name, data))
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
        #action_id = action.getId()
        if action in self.ACTION_PREVIOUS_MENU:
            if focusid in [7050, 7051, 7000, 7001, 7002, 7003]:
                xbmc.executebuiltin("Control.SetFocus(33012)")
            elif focusid in [5000]:
                xbmc.executebuiltin("Control.SetFocus(7001)")
            elif focusid in [5001]:
                xbmc.executebuiltin("Control.SetFocus(7002)")
            elif focusid in [5002]:
                xbmc.executebuiltin("Control.SetFocus(7003)")
            else:
                self.close()
                PopWindowStack(self)

        elif action in self.ACTION_RIGHT_CLICK:
            xbmc.log('[%s]: HomeScreen ACTION_RIGHT_CLICK' % addon_name)
            if focusid in [7050, 7051, 7000, 7001, 7002, 7003]:
                xbmc.executebuiltin("Control.SetFocus(33012)")
            elif focusid in [5000]:
                xbmc.executebuiltin("Control.SetFocus(7001)")
            elif focusid in [5001]:
                xbmc.executebuiltin("Control.SetFocus(7002)")
            elif focusid in [5002]:
                xbmc.executebuiltin("Control.SetFocus(7003)")
            else:
                self.close()
                PopWindowStack(self)

        elif action in self.ACTION_EXIT_SCRIPT:
            self.close()

    def onClick(self, controlID):
        #if self.window.getProperty('SVOD'):
        #    xbmc.log('!!![SVOD]: %s' % self.window.getProperty('SVOD'))
        #if self.window.getProperty('TVOD'):
        #    xbmc.log('!!![TVOD]: %s' % self.window.getProperty('TVOD'))

        if controlID in [33003]:
            link, subtitle = megogo2xbmc.get_stream(self.data["id"])
            listitem = xbmcgui.ListItem(self.data['title'], iconImage = self.data["poster"], thumbnailImage = self.data["poster"])
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

            xbmc.executebuiltin("Control.SetFocus(7000)")

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

        elif controlID in [7050]:
            xbmc.executebuiltin("Control.SetFocus(33012)")

        elif controlID in [7001]:
            xbmc.executebuiltin("Control.SetFocus(5000)")

        elif controlID in [7002]:
            xbmc.executebuiltin("Control.SetFocus(5001)")

        elif controlID in [7003]:
            xbmc.executebuiltin("Control.SetFocus(5002)")

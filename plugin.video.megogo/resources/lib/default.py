# -*- coding: utf-8 -*- 
#############################################################################
#
#	Copyright (C) 2015 Studio-Evolution
#
#	Plugin made for service MEGOGO.NET
#
#############################################################################

import xbmc, xbmcgui, xbmcaddon
import re, os, sys

addon			= xbmcaddon.Addon()
addon_id        = addon.getAddonInfo('id')
addon_name		= addon.getAddonInfo('name')
addon_path		= addon.getAddonInfo('path').decode("utf-8")
addon_version	= addon.getAddonInfo('version')
language		= addon.getLocalizedString
SkinFolder		= os.path.join(addon_path, 'resources', 'skins', 'Default', '1080i')
MediaFolder		= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media')
LibFolder		= os.path.join(addon_path, 'resources', 'lib')

sys.path.append(xbmc.translatePath(LibFolder).decode("utf-8"))
import HomeScreen


class Main:

    # Initialization
    def __init__(self, **kwargs):
        splash = kwargs.get('splash')

        from Utils import SettingS, FileDoOpen, FileDoSave

        ####################################		First run		#########################################
        if addon.getSetting('firstrun') == '0' or addon.getSetting('firstrun') == '':
            addon.openSettings()
            SettingS('firstrun', '1')

        ####################################		User name		#########################################
        if addon.getSetting('user') == '':
            SettingS('user', '')

        ####################################		Password		#########################################
        if addon.getSetting('password') == '':
            SettingS('password', '')

        ####################################	 Cookie	Update		#########################################
        SettingS('cookie', '')

        ####################################  Get quality settings  #########################################
        if addon.getSetting('quality') == '':
            SettingS('quality', language(206))

        ####################################    Get audio language	#########################################
        if addon.getSetting('audio_language') == '':
            SettingS('audio_language', language(300))

        ####################################  Get subtitle language #########################################
        if addon.getSetting('subtitle_language') == '':
            SettingS('subtitle_language', language(400))

        ####################################	Work with colors	#########################################
        if addon.getSetting('last-text-color') == '':
            SettingS('last-text-color', 'FFFAFAFA')

        value = addon.getSetting('text-color')
        try:
            TextColor = value.split(']', 1)[0].split(' ')[1]
            ColorName = value.split(']', 1)[1].split('[')[0]

            #re_current_color_diffuse 	= re.compile(ur'<colordiffuse>0x([^<]*)</colordiffuse>')
            #try: current_color_diffuse 	= re.search(re_current_color_diffuse, File).group(1)
            #except: current_color_diffuse= ''
            #if (current_color_diffuse!=SkinColor and current_color_diffuse!=''):
            #	File=File.replace('<colordiffuse>0x%s</colordiffuse>' % current_color_diffuse, '<colordiffuse>0x%s</colordiffuse>' % SkinColor)	# Find and replace color diffuse in skin
            #	xbmc.log('[%s]: diffuse color changed' % addon_name)
        except:
            TextColor = 'FFFAFAFA'
            ColorName = 'Original'

        if addon.getSetting('last-text-color') != TextColor:
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
                            SettingS('last-text-color', TextColor.upper())
                            xbmc.log('[%s]: text color changed' % addon_name)
                        FileDoSave(os.path.join(SkinFolder, name), Fil)
            except:
                xbmc.log('[%s]: cannot change skin colors!' % addon_name)
        else:
            xbmc.log('[%s]: colors settings not changed' % addon_name)

        ####################################	Parse arguments		#########################################
        #arg = parse_argv()

        #try: xbmc.log('[%s]: arg %s' % (addon_name, arg))
        #except: pass

        ####################################	Start Home Screen	#########################################
        home = HomeScreen.Homescreen('HomeScreen.xml', addon_path, win=splash, usr=addon.getSetting('user'), pwd=addon.getSetting('password'))
        home.doModal()

        del home
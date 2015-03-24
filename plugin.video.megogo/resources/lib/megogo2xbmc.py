# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (C) 2015 Studio-Evolution
#
# Library to work with MEGOGO.NET api for XBMC
#
#############################################################################

import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import simplejson, requests
import urllib, time, urllib2, hashlib, os, re, base64
from sqlite import DataBase as DB
from Utils import get_quality, get_language, get_subtitle

addon 			= xbmcaddon.Addon()
language		= addon.getLocalizedString
addon_path		= addon.getAddonInfo('path').decode('utf-8')
addon_id		= addon.getAddonInfo('id')
addon_author	= addon.getAddonInfo('author')
addon_name		= addon.getAddonInfo('name')
addon_version	= addon.getAddonInfo('version')
unknown_person	= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'unknown_person.png')

API_Private_Key_MEGOGO  = '63ee38849d'
API_Public_Key_MEGOGO   = '_kodi_j1'
API_URL                 = 'http://api.megogo.net/v1'
MEGOGO_URL              = 'http://megogo.net'
UA                      = 'Plugin/%s %s/%s' % (addon_id, urllib.quote_plus(addon_author), addon_version)

slider_images_resolution = ['image_1920x300', 'image_1600x520', 'image_1350x510']

a = DB()

# Function to get cached JSON response from db or 
# set response from MEGOGO to db
def Get_JSON_response(url="", cache_days=7):
    xbmc.log('[%s]: Trying to get %s' % (addon_name, url))
    now = time.time()
    hashed_url = hashlib.md5(url).hexdigest()
    cache_seconds = int(cache_days * 86400)
    response = a.get_page_from_db(hashed_url, cache_seconds)
    # xbmc.log('[%s]: JSON response - %s' % (addon_name, response.encode('utf-8')))
    if not response:
        xbmc.log("[%s]: %s is not in cache, trying download data" % (addon_name, url))
        response = GET(url)
        #try:
        result = simplejson.loads(response)
        xbmc.log("[%s]: %s download  in %f seconds" % (addon_name, url, time.time() - now))
        a.set_page_to_db(hashed_url, int(time.time()), response)
        #except:
        #    xbmc.log("[%s]: Exception: Could not get new JSON data. %s" % (addon_name, response))
        #    result = []
    else:
        result = simplejson.loads(response)
        xbmc.log("[%s]: %s loaded from cache in %f seconds" % (addon_name, url, time.time() - now))

    #xbmc.log('[%s]: JSON responce - %s' % (addon_name, result))
    return result


# Function for sending GET requsts to megogo.net
# req_p1 used for keeping urlencoded parameters
# req_p2 used for keeping md5-sign of parameters+API_Public_Key_MEGOGO, that send in end of each request 
def GET(url, old_url=None, login=False):
    #try:
    dicParams = {}
    linkParams = []
    hashParams = []
    dic = a.get_login_from_db()
    if dic['cookie']:
        cookie = simplejson.loads(base64.b64decode(dic['cookie']))
    else:
        cookie = None
    usr = dic['login']
    pwd = dic['password']

    page, _, params = url.partition('?')

    if params:
        params = params.split('&')
        for param in params:
            key, _, value = param.partition('=')
            dicParams[key] = value

        for keys in dicParams:
            linkParams.append('%s=%s' % (keys, urllib.quote_plus(dicParams[keys])))
            hashParams.append('%s=%s' % (keys, dicParams[keys]))

        linkParams = '&'.join(linkParams)
        hashParams = ''.join(hashParams)
    else:
        hashParams = ''
        linkParams = ''

    m = hashlib.md5()
    m.update('%s%s'%(hashParams, API_Private_Key_MEGOGO))
    target = '%s/%s?%s&sign=%s' % (API_URL, page, linkParams, '%s%s' % (m.hexdigest(), API_Public_Key_MEGOGO))

    xbmc.log('[%s]: GET\nUSR - %s\nPASS - %s\nCookie - %s\nTarget - %s' % (addon_name, usr, pwd, cookie, target))

    if cookie and not old_url:
        request = requests.get(target, cookies=cookie)
        http = request.text
        xbmc.log('[%s]: GET cookie and not old_url, http - %s' % (addon_name, http.encode('utf-8')))
        return http.encode('utf-8')

    # log in account in megogo.net
    elif usr and pwd and login:
        xbmc.log('[%s]: GET elif usr and pwd and login, url - %s' % (addon_name, url))
        if not url.startswith('auth/login?login='):
            GET('auth/login?login=%s&password=%s&remember=1' % (usr, pwd), old_url=url, login=True)
        else:
            session = requests.session()
            request = session.get(target)
            http = request.text
            if http.startswith('{"result":"ok"'):
                cookies = requests.utils.dict_from_cookiejar(session.cookies)
                xbmc.log('[%s]: NEW COOKIE - %s' % (addon_name, cookies))
                a.cookie_to_db(base64.b64encode(str(cookies).replace("'", '"')))
                if old_url:
                    xbmc.log('[%s]: GET elif usr and pwd, old_url - %s' % (addon_name, old_url))
                    GET(old_url)
                else:
                    xbmc.log('[%s]: return GET elif usr and pwd, http - %s' % (addon_name, http.encode('utf-8')))
                    return http.encode('utf-8')
            else:
                return None

    else:
        try:
            request = urllib2.Request(url=target, data=None, headers={'User-Agent': UA})
            request = urllib2.urlopen(request)
            http = request.read()
            request.close()
            xbmc.log('[%s]: GET else, http - %s' % (addon_name, http))
            return http
        except:
            return ''


def checkLogin():
    dic = a.get_login_from_db()
    if dic['cookie']:
        xbmc.log('[%s]: Log in success. Cookie - %s' % (addon_name, dic['cookie']))
        return True
    else:
        if dic['login'] and dic['password']:
            if log_in(dic['login'], dic['password']):
                return True
            else:
                return False
        else:
            xbmc.log('[%s]: Cannot log in account! login and pass EMPTY.' % addon_name)
            return False


def log_in(usr, pwd):
    xbmc.log('[%s]: Try to login with {usr: %s, pass: %s}' % (addon_name, usr, pwd))
    data = GET('auth/login?login=%s&password=%s&remember=1' % (usr, pwd), login=True)
    xbmc.log('[%s]: login, if usr and pwd, data - %s' % (addon_name, data))
    if data:
        return simplejson.loads(data)
    else:
        xbmc.log('[%s]: Cannot log in account! Error retrieving data.' % addon_name)
        return False


# Clear user, password and session_id from addon settings
def logout():
    # TODO: LOGOUT FROM MEGOGO.NET
    addon.setSetting('login', '')
    addon.setSetting('password', '')
    xbmc.log('[%s]: logout successful' % addon_name)


def HandleMainPage(responce, types = None):
    info = []
    if types:
        array = responce[types]
    else:
        array = responce

    for item in array:
        info.append(HandleVideoResult(item))
    return info


# Function that get information about video-file from json-answer
def HandleVideoResult(item):
    try: video = item['video']
    except: video = item

    try: title = video['title']
    except: title = ''

    try: vid = video['object_id']
    except: vid = video['id']

    try:
        if video["slider_type"] == "feature":
            video_type = 'collection'
        elif video["slider_type"] == "object":
            video_type = 'video'
    except:
        video_type = 'video'

    #try:
    #	if video["slider_type"]=="feature":
    #		try: path = '%s://%s/?do=open&type=collection&id=%s' % (addon_type, addon_id, video['object_id'])
    #		except:
    #			try: path = '%s://%s/?do=open&type=collection&id=%s' % (addon_type, addon_id, video['id'])
    #			except: pass
    #	else:
    #		try: path = '%s://%s/?do=open&type=video&id=%s' % (addon_type, addon_id, video['object_id'])
    #		except:
    #			try: path = '%s://%s/?do=open&type=video&id=%s' % (addon_type, addon_id, video['id'])
    #			except: pass
    #except:
    #	try: path = '%s://%s/?do=open&type=video&id=%s' % (addon_type, addon_id, video['object_id'])
    #	except:
    #		try: path = '%s://%s/?do=open&type=video&id=%s' % (addon_type, addon_id, video['id'])
    #		except: pass

    try: original_title = video['title_original']
    except: original_title = ''

    try:
        poster = video['image']['big']
        if poster.count(':') > 1:
            poster = ':'.join(poster.split(':')[:-1])[:-1]+'2:'+poster.split(':')[-1]
    except: poster = ''

    try: country = video['country']
    except: country = ''

    try: year = video['year']
    except: year = ''

    try: description = video['description'].replace('<p>','').replace('</p>','').replace('<i>','').replace('</i>','').replace('\r\n\r\n','\r\n').replace('&#151;','-').replace('&raquo;','"').replace('&laquo;','"').replace('<BR>','').replace('<br>','')
    except: description = ''

    try: genre = a.get_genres_from_db(video['genres'])
    except: genre = ''

    try: category = a.get_category_from_db(video['categories'])
    except: category = ''

    try: delivery = ', '.join(video['delivery_rules'])
    except: delivery = ''

    for resolution in slider_images_resolution:
        try: image = item[resolution]
        except: image = None
        if image and image!='':
            poster = image
            break

    try: poster = item["image"]["image_vertical"]
    except: pass

    try:
        rating = "%.2f" % float(item['rating_kinopoisk'])
    except: rating = ''

    try:
        rating_imdb = "%.2f" % float(item['rating_imdb'])
    except: rating_imdb = ''

    try: age_limit = item['age_limit']
    except: age_limit = ''

    try: like = item['like']
    except: like = ''

    try: dislike = item['dislike']
    except: dislike = ''

    try: duration = int(item['duration'] / 60)
    except: duration = ''

    try:
        crew = a.crew_info(item['people'])
    except: crew = ''

    try: favourite = item['is_favorite']
    except: favourite = None

    try: vote = item['vote']
    except: vote = ''

    try:
        screenshots = []
        for picture in item['screenshots']:
            screenshots.append(picture['big'])
    except: screenshots = None

    try: quality = item['quality']
    except: quality = ''

    try: season_list = item['season_list']		# TODO SEASONS!
    except: season_list = None

    try: available = item['is_available']
    except: available = False

    try:
        purchase = item["purchase_info"]
        currency = purchase['tvod']['subscriptions'][0]['currency']
        price = int(purchase['tvod']['subscriptions'][0]['tariffs'][0]['price'])
    except:
        currency = None
        price = None

    try: recommended_videos = item["recommended_videos"]
    except: recommended_videos = []

    try: exclusive = '%s' % item["is_exclusive"]
    except: exclusive = 'false'

    try: series = '%s' % item["is_series"]
    except: series = 'false'

    locInfo = { 'title'			: title,
                'id'			: unicode(vid),
                'type'			: video_type,
                'originaltitle'	: original_title,
                'country'		: country,
                'year'			: year,
                'plot'			: description,
                'genre'			: genre,
                'categories'	: category,
                'poster'		: poster,
                'delivery_rules': delivery,
                'rating'		: rating,
                'imdb_rating'	: rating_imdb,
                'mpaa'			: age_limit,
                'like'			: unicode(like),
                'dislike'		: unicode(dislike),
                'duration'		: unicode(duration),
                'crew'			: crew,
                'favourite'		: favourite,
                'vote'			: vote,
                'screenshots'	: screenshots,
                'quality'		: quality,
                'season_list'	: season_list,
                'available'		: available,
                'currency'		: currency,
                'price'			: price,
                'recommended'	: recommended_videos,
                'exclusive'		: exclusive,
                'series'		: series,
              }

    #xbmc.log('[%s]: HandleVideoResult parses data - %s' % (addon_name, locInfo))
    return locInfo


# Get configuration
def getconfiguration():
    xbmc.log('[%s]: Try to get configuration' % addon_name)
    data = GET('configuration')
    #try:
    # xbmc.log('data - %s' % data)
    data = simplejson.loads(data)

    if data['result'] == 'ok':
        a.set_genres_to_db(data['data']['genres'])
        a.set_categories_to_db(data['data']['categories'])
        a.set_member_types_to_db(data['data']['member_types'])
        xbmc.log('[%s]: Successful get configuration' % addon_name)
        return True
    else:
        return False
    #except:
    #    return False
    


# Get tarifications
def gettarification():
    xbmc.log('[%s]: Try to get tarification' % addon_name)
    data = Get_JSON_response('subscription/info')
    if data['result'] == 'ok':
        xbmc.log('[%s]: Successful get tarification' % addon_name)
        return data['data']
    else:
        return False


# Get prise from tarif
def get_price(title):
    if title == 'svod':
        title = 'MEGOGO+'

    data = gettarification()
    for arr in data:
        if arr['title'] == title:
            currency = arr['currency']
            month_price = arr['tariffs'][0]['price']
            break

    return "%s %s" % (month_price, currency)


# Get recommended materials
def main_page(cache_days=1):
    data = Get_JSON_response('digest', cache_days)
    if data['result'] == 'ok':
        return data
    else:
        return []


# Get video data
def getvideodata(section, page):
    xbmc.log('[%s]: Try to get getvideodata' % addon_name)
    if section == 'collection':
        data = Get_JSON_response('collection?id=%s' % page)
    elif section == 'video':
        data = Get_JSON_response('video/info?id=%s' % page)
    if data['result'] == 'ok':
        return data
    else:
        return []


# Get stream
def data_from_stream(video_id):
    xbmc.log('[%s]: Try to data from stream' % addon_name)
    bitrates = []
    audios = []
    subtitles = []

    data = Get_JSON_response('stream?video_id=%s' % video_id, cache_days=1)
    if data['result'] == 'ok':
        try:
            for bit in data['data']['bitrates']:
                bitrates.append(bit['bitrate'])
        except:
            bitrates = None

        try:
            for audio in data['data']['audio_tracks']:
                audios.append(audio['lang'])
        except:
            audios = None

        try:
            for subtitle in data['data']['subtitles']:
                subtitles.append(subtitle['lang'])
        except:
            subtitles = None

        return bitrates, audios, subtitles

    else:
        return None, None, None


def get_stream(video_id):
    bitrate = None
    audio_lang = None
    subtitle_lang = None

    xbmc.log('[%s]: Try to get stream' % addon_name)

    p = re.compile(ur'(\d+)')		# REGEXP TO GET VIDEO QUALITY FROM SETTINGS

    data = Get_JSON_response('stream?video_id=%s' % video_id, cache_days=1)
    if data['result'] == 'ok':
        if data['data']['is_wvdrm']:
            xbmc.log('[%s]: NEED TO DO DRM FOR THIS VIDEO (%s, %s)' % (addon_name, data['data']['title'], data['data']['id']))

    preset_bitrate = get_quality(addon.getSetting('quality'))
    xbmc.log('[%s]: PRESET BITRATE - %s' % (addon_name, preset_bitrate.encode('utf-8')))
    for bit in data['data']['bitrates']:
        if bit['bitrate'] == int(re.search(p, preset_bitrate).group(0)):
            bitrate = bit['bitrate']
            break
        else:
            bitrate = None
    if not bitrate:
        bitrate = data['data']['bitrates'][-1]['bitrate']
    xbmc.log('[%s]: BITRATE IN MOVIE - %s' % (addon_name, bitrate))

    preset_language = get_language(addon.getSetting('audio_language'))
    xbmc.log('[%s]: PRESET LANGUAGE - %s' % (addon_name, preset_language.encode('utf-8')))
    for audio in data['data']['audio_tracks']:
        if audio['lang'] == preset_language[-3:-1]:
            audio_lang = audio['lang']
            break
        else:
            audio_lang = None
    if not audio_lang:
        try:
            audio_lang = data['data']['audio_tracks'][0]['lang']
            xbmc.log('[%s]: LANGUAGE IN MOVIE - %s' % (addon_name, audio_lang.encode('utf-8')))
        except:
            audio_lang = None

    preset_subtitle = get_subtitle(addon.getSetting('subtitle_language'))
    xbmc.log('[%s]: PRESET SUBTITLE - %s' % (addon_name, preset_subtitle.encode('utf-8')))
    if preset_subtitle.endswith(')'):
        try:
            for subtitle in data['data']['subtitles']:
                if subtitle['lang'] == addon.getSetting('subtitle_language')[-3:-1]:
                    subtitle_lang = subtitle['url']
                    break
                else:
                    subtitle_lang = None
            if not subtitle_lang:
                subtitle_lang = data['data']['subtitles'][0]['url']
        except:
            subtitle_lang = None
    else:
        subtitle_lang = None
    try:
        xbmc.log('[%s]: SUBTITLE IN MOVIE - %s' % (addon_name, subtitle_lang.encode('utf-8')))
    except:
        pass

    new_data = Get_JSON_response('stream?video_id=%s&bitrate=%s&lang=%s' % (video_id, bitrate, audio_lang), cache_days=1)

    if new_data['result'] == 'ok':
        return new_data['data']['src'], audio_lang, subtitle_lang


# Get comments to video
def getcomments(video_id):
    data = Get_JSON_response('comment/list?video_id=%s' % video_id, cache_days=1)
    if data['result'] == 'ok':
        return data['data']['comments']
    else:
        return None


def get_page(force, page, offset=0):
    if offset != 0:
        url = '%s&offset=%d' % (page, offset)
    else:
        url = page
    if force:
        cache = 0
    else:
        cache = 1
    data = Get_JSON_response(url, cache_days=cache)

    return data


def addFav(params):
    data = Get_JSON_response('addfavorite?video=%s' % params['id'])
    if data['result'] == 'ok':
        return True
    else:
        return False


# Delete video from favorites
def delFav(params):
    data = Get_JSON_response('removefavorite?video=%s' % params['id'])
    if data['result'] == 'ok':
        return True
    else:
        return False


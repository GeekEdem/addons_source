##########################################################################
#
#	Copyright (C) 2015 Studio-Evolution
#
#	Library to work with MEGOGO.NET api v1 for XBMC
#
#############################################################################

import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import simplejson, requests
import urllib, time, urllib2, hashlib, os, re, sys

addon 			= xbmcaddon.Addon()
language		= addon.getLocalizedString
addon_icon		= addon.getAddonInfo('icon')
addon_fanart	= addon.getAddonInfo('fanart')
addon_path		= addon.getAddonInfo('path').decode('utf-8')
addon_type		= addon.getAddonInfo('type')
addon_id		= addon.getAddonInfo('id')
addon_author	= addon.getAddonInfo('author')
addon_name		= addon.getAddonInfo('name')
addon_version	= addon.getAddonInfo('version')
unknown_person	= os.path.join(addon_path, 'resources', 'skins', 'Default', 'media', 'unknown_person.png')

MAX_DELAY               = 2592000		    # 30 days
API_Private_Key_MEGOGO  = '63ee38849d'
API_Public_Key_MEGOGO   = '_kodi_j1'
API_URL                 = 'http://api.megogo.net/v1'
MEGOGO_URL              = 'http://megogo.net'

slider_images_resolution = ['image_1920x300', 'image_1600x520', 'image_1350x510']

try:
    import sqlite3 as db
except ImportError:
    xbmc.log('[%s]: Error import sqlite3. Uses module pysqlite2' % addon_id)
    try:
        import pysqlite2 as db
    except ImportError:
        xbmc.log('[%s]: Error import pysqlite2. Sorry' % addon_id)

db_name = os.path.join(addon_path, "resources", "requests.db")
c = db.connect(database =db_name)
cu = c.cursor()

UA = '%s/%s %s/%s' % (addon_type, addon_id, urllib.quote_plus(addon_author), addon_version)


# Check existing of table in db
def table_exist(name):
    cu.execute("PRAGMA table_info(%s)" % name)
    if len(cu.fetchall()) > 0:
        return True
    else:
        return False


# Clear table in db
def clear_table(name):
    cu.execute("DELETE FROM %s" % name)
    cu.execute("VACUUM")
    c.commit()
    xbmc.log('[%s]: "%s" table was cleared' % (addon_name, name))


# Function that get cached requests from DB when time is < cache_time
def get_page_from_db(url, cache_seconds):
    xbmc.log('[%s]: trying get %s from db' % (addon_name, url))
    if table_exist('cache'):
        cu.execute("SELECT time FROM cache WHERE link = '%s'" % url)
        c.commit()
    else:
        cu.execute("CREATE TABLE cache (link, time int, data)")
        c.commit()

    try:
        time_in_db = cu.fetchone()[0]
    except:
        xbmc.log('[%s]: No records in db with link %s, return empty line' % (addon_name, url))
        return ''

    now = time.time()
    difference = int(now-time_in_db)
    xbmc.log('[%s]: time_in_db - %d; time now - %d; difference - %d' % (addon_name, time_in_db, now, difference))
    if difference>cache_seconds:
        cu.execute("DELETE FROM cache WHERE link = '%s'" % url)
        cu.execute("VACUUM")
        c.commit()
        xbmc.log('[%s]: Cached object in db is too old, deleting it. Return empty string.' % addon_name)
        return ''
    else:
        cu.execute("SELECT data FROM cache WHERE link = '%s'" % url)
        c.commit()
        info = cu.fetchone()[0]
        return info


# Function that cached all requests to DB and delete all that older MAX_DELAY
def set_page_to_db(url, time, result):
    try:
        xbmc.log('[%s]: Try to delete old records' % addon_name)
        old_response =[]
        for row in cu.execute('SELECT time FROM cache ORDER BY time'):
            time_in_db = row[0]
            delay = int(time.time()) - time_in_db
            if int(delay) > MAX_DELAY:
                old_response.append(time_in_db)
        for dels in old_response:
            cu.execute("DELETE FROM cache WHERE time = '%s'" % dels)
            c.commit()
        if len(old_response)>0: xbmc.log('[%s]: %d record(s) was deleted from db' % (addon_name, len(old_response)))
        else:
            xbmc.log('[%s]: No old records. Nothing to delete.' % addon_name)
    except:
        pass
    xbmc.log('[%s]: trying write %s to db' % (addon_name, url))
    if not table_exist('cache'):
        cu.execute("CREATE TABLE cache (link, time int, data)")
        c.commit()
        xbmc.log('[%s]: table "CACHE" was created' % addon_name)
    try:
        cu.execute("INSERT INTO cache(link, time, data) VALUES (?, ?, ?)", (url, time, result.decode('utf-8')))
        c.commit()
        xbmc.log('[%s]: %s was writen to db' % (addon_name, url))
    except:
        xbmc.log('[%s]: Cannot write data from %s to db' % (addon_name, url))


# Write to db list of genres
def set_genres_to_db(genres):
    if table_exist('genres'):
        clear_table('genres')
    else:
        cu.execute("CREATE TABLE genres (id int, title)")
        c.commit()
        xbmc.log('[%s]: table "GENRES" was created' % addon_name)

    if len(genres) != 0:
        for genre in genres:
            gId = genre['id']
            gName = genre['title']
            cu.execute("INSERT INTO genres(id, title) VALUES (?, ?)", (gId, gName))
        c.commit()
        xbmc.log('[%s]: %d new genres was writen to db' % (addon_name, len(genres)))


# Get from db list of genres
def get_genres_from_db(genre_list):
    genres = []
    for genre in genre_list:
        cu.execute("SELECT title FROM genres WHERE id = %d" % genre)
        try:
            var = cu.fetchone()[0]
        except:
            var = None
        if var:
            genres.append(var)
    return ', '.join(genres)


# Write to db all categories
def set_categories_to_db(categories):
    if table_exist('categories'):
        clear_table('categories')
    else:
        cu.execute("CREATE TABLE categories (id int, title, genres)")
        c.commit()
        xbmc.log('[%s]: table "CATEGORIES" was created' % addon_name)

    if len(categories) != 0:
        for category in categories:
            cId = category['id']
            cName = category['title']
            cGenres = ', '.join(str(x) for x in category['genres'])
            cu.execute("INSERT INTO categories(id, title, genres) VALUES (?, ?, ?)", (cId, cName, cGenres))
        c.commit()
        xbmc.log('[%s]: %d new categories was writen to db' % (addon_name, len(categories)))


# Get from db list of categories
def get_category_from_db(categories):
    categoris = []
    for category in categories:
        cu.execute("SELECT title FROM categories WHERE id = %d" % category)
        try:
            var = cu.fetchone()[0]
        except:
            var = None
        if var:
            categoris.append(var)
    return ', '.join(categoris)

# Get from db id of category by name
def get_category_from_db_by_name(name):
    cu.execute("SELECT id FROM categories WHERE title = %s" % name)
    try:
        var = cu.fetchone()[0]
    except:
        var = None
    return var

# Write to db all MemberTypes
def set_member_types_to_db(types):
    if table_exist('MemberTypes'):
        clear_table('MemberTypes')
    else:
        cu.execute("CREATE TABLE MemberTypes (type, title)")
        c.commit()
        xbmc.log('[%s]: table "MemberTypes" was created' % addon_name)

    if len(types) != 0:
        for memberType in types:
            mType = memberType['type']
            mName = memberType['title']
            cu.execute("INSERT INTO MemberTypes(type, title) VALUES (?, ?)", (mType, mName))
        c.commit()
        xbmc.log('[%s]: %d new MemberTypes was writen to db' % (addon_name, len(types)))


# Get from db MemberType
def get_member_types_from_db(typ):
    cu.execute("SELECT title FROM MemberTypes WHERE type = '%s'" % typ)
    try:
        var = cu.fetchone()[0]
    except:
        var = None
    if var:
        return var
    else:
        return ''


# Get crew information
def crew_info(peoples):
    info = []
    for man in peoples:
        crew_id = man['id']
        crew_type = get_member_types_from_db(man['type'])
        try:
            crew_name = man['name']
        except:
            crew_name = None
        try:
            crew_origin_name = man['name_original']
        except:
            crew_origin_name = None
        try:
            picture = man['avatar']['image_360x360']
        except:
            picture = None
        if not picture:
            try:
                picture = man['avatar']['image_240x240']
            except:
                picture = unknown_person
        info.append({'id': crew_id, 'type': crew_type, 'name': crew_name, 'name_original': crew_origin_name, 'thumb': picture})
    c.commit()
    return info


# Function to get cached JSON response from db or 
# set response from MEGOGO to db
def Get_JSON_response(url="", cache_days=7):
    xbmc.log('[%s]: Trying to get %s' % (addon_name, url))
    now = time.time()
    hashed_url = hashlib.md5(url).hexdigest()
    cache_seconds = int(cache_days * 86400)
    response = get_page_from_db(hashed_url, cache_seconds)
    #xbmc.log('[%s]: JSON responce - %s' % (addon_name, response.encode('utf-8')))
    if not response:
        xbmc.log("[%s]: %s is not in cache, trying download data" % (addon_name, url))
        response = GET(url)
        try:
            result = simplejson.loads(response)
            xbmc.log("[%s]: %s download  in %f seconds" % (addon_name, url, time.time() - now))
            set_page_to_db(hashed_url, int(time.time()), response)
        except:
            xbmc.log("[%s]: Exception: Could not get new JSON data. %s" % (addon_name, response))
            result = []
    else:
        result = simplejson.loads(response.encode('utf-8'))
        xbmc.log("[%s]: %s loaded from cache in %f seconds" % (addon_name, url, time.time() - now))

    #xbmc.log('[%s]: JSON responce - %s' % (addon_name, result))
    return result


# Function for sending GET requsts to megogo.net
# req_p1 used for keeping urlencoded parameters
# req_p2 used for keeping md5-sign of parameters+API_Public_Key_MEGOGO, that send in end of each request 
def GET(url, usr=addon.getSetting('user'), pwd=addon.getSetting('password')):
    try:
        dicParams = {}
        linkParams = []
        hashParams = []
        cookie = None

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

        xbmc.log('[%s]: target - %s' % (addon_name, target))								# LOG URL
        xbmc.log('[%s]: cookie - %s' % (addon_name, addon.getSetting('cookie')))		    # LOG SESSION ID

        if addon.getSetting('cookie'):								                        # GET COOKIE TO AUTHORISATION
            cookie = simplejson.loads(addon.getSetting('cookie').replace('&apos;', "'"))

        xbmc.log('[%s]: usr - %s \n pwd - %s \n cookie - %s \n' % (addon_name, usr, pwd, cookie))

        if cookie:
            request = requests.get(target, cookies=cookie)
            http = request.text
            return http

        # log in account in megogo.net
        elif usr and pwd:
            if not url.startswith('auth/login?login='):
                GET('auth/login?login=%s&password=%s&remember=1' % (usr, pwd))
            else:
                session = requests.session()
                request = session.get(target)
                http = request.text
                if http.startswith('{"result":"ok"'):
                    cookies = requests.utils.dict_from_cookiejar(session.cookies)
                    addon.setSetting('cookie', "%s" % str(cookies).replace("'", '"'))
                    xbmc.log('[%s]: NEW COOKIE - %s' % (addon_name, cookies))
                    return http
                else:
                    return ''

        else:
            request = urllib2.Request(url=target, data=None, headers={'User-Agent': UA})
            request = urllib2.urlopen(request)
            http = request.read()
            request.close()

            return http
    except:
        return ''


def checkLogin(usr=addon.getSetting('user'), pwd=addon.getSetting('password')):
    if addon.getSetting('cookie'):
        xbmc.log('[%s]: Check_login cookie - %s' % (addon_name, addon.getSetting('cookie')))
        return True
    else:
        if usr and pwd:
            xbmc.log('[%s]: Try to login with {usr: %s, pass: %s}' % (addon_name, usr, pwd))
            data = GET('auth/login?login=%s&password=%s&remember=1' % (usr, pwd), usr, pwd)
            if data:
                return True
            else:
                xbmc.log('[%s]: Check_login usr, pass NOT EMPTY, but GET false. data - %s' % (addon_name, data))
                return False
        else:
            xbmc.log('[%s]: Check_login usr, pass EMPTY.\n USR - %s \n PWD - %s' % (addon_name, usr, pwd))
            return False


# Clear user, password and session_id from addon settings
def logout():
    # TODO: LOGOUT FROM MEGOGO.NET
    addon.setSetting('session', '')
    addon.setSetting('user', '')
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
        if video["slider_type"]=="feature":
            video_type = 'collection'
        elif video["slider_type"]=="object":
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
        poster = ':'.join(poster.split(':')[:-1])[:-1]+'2:'+poster.split(':')[-1]
    except: poster = ''

    try: country = video['country']
    except: country = ''

    try: year = video['year']
    except: year = ''

    try: description = video['description'].replace('<p>','').replace('</p>','').replace('<i>','').replace('</i>','').replace('\r\n\r\n','\r\n').replace('&#151;','-').replace('&raquo;','"').replace('&laquo;','"')
    except: description = ''

    try: genre = get_genres_from_db(video['genres'])
    except: genre = ''

    try: category = get_category_from_db(video['categories'])
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
        crew = crew_info(item['people'])
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

    try:
        recommended_videos = item["recommended_videos"]
    except:
        recommended_videos = []


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
                'recommended'   : recommended_videos
              }

    #xbmc.log('[%s]: HandleVideoResult parses data - %s' % (addon_name, locInfo))
    return locInfo


# Get configuration
def getconfiguration():
    xbmc.log('[%s]: Try to get configuration' % addon_name)
    data = GET('configuration')
    try:
        data = simplejson.loads(data)

        if data['result'] == 'ok':
            set_genres_to_db(data['data']['genres'])
            set_categories_to_db(data['data']['categories'])
            set_member_types_to_db(data['data']['member_types'])
            xbmc.log('[%s]: Successful get configuration' % addon_name)
            return True
        else:
            return False
    except:
        return None
    


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
    xbmc.log('[%s]: Try to get stream' % addon_name)

    p = re.compile(ur'(\d+)')		# REGEXP TO GET VIDEO QUALITY FROM SETTINGS

    data = Get_JSON_response('stream?video_id=%s' % video_id, cache_days=1)
    if data['result'] == 'ok':
        if data['data']['is_wvdrm']:
            xbmc.log('[%s]: NEED TO DO DRM FOR THIS VIDEO (%s, %s)' % (addon_name, data['data']['title'], data['data']['id']))

    for bit in data['data']['bitrates']:
        if bit['bitrate'] == re.search(p, addon.getSetting('quality')).group(0):
            bitrate = bit['bitrate']
            break
        else:
            bitrate = None
    if not bitrate:
        bitrate = data['data']['bitrates'][-1]['bitrate']

    for audio in data['data']['audio_tracks']:
        if audio['lang'] == addon.getSetting('audio_language')[-3:-1]:
            audio_lang = audio['lang']
            break
        else:
            audio_lang = None
    if not audio_lang:
        audio_lang = data['data']['audio_tracks'][0]['lang']

    if addon.getSetting('subtitle_language').endswith(')'):
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

    new_data = Get_JSON_response('stream?video_id=%s&bitrate=%s&lang=%s' % (video_id, bitrate, audio_lang), cache_days=1)

    if new_data['result'] == 'ok':
        return new_data['data']['src'], subtitle_lang


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


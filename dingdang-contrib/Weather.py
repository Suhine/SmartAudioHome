# -*- coding: utf-8-*-
# 天气插件
import logging
import requests
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Standard module stuff
WORDS = ["TIANQI"]
SLUG = "weather"

def analyze_today(weather_code, suggestion):
    """ analyze today's weather """
    weather_code = int(weather_code)
    if weather_code <= 8:
        if u'适宜' in suggestion:
            return u'今天天气不错，空气清新，适合出门运动哦'
        else:
            return u'空气质量比较一般，建议减少出行'
    elif weather_code in range(10, 16):
        return u'主人，出门记得带伞哦'
    elif weather_code in range(16, 19) or \
    weather_code in range(25, 30) or \
    weather_code in range(34, 37):
        return u'极端天气来临，尽量待屋里陪我玩吧'
    elif weather_code == 38:
        return u'天气炎热，记得多补充水分哦'
    elif weather_code == 37:
        return u'好冷的天，记得穿厚一点哦'
    else:
        return u''


def fetch_weather(api, key, location):
    result = requests.get(api, params={
        'key': key,
        'location': location
    }, timeout=3)
    res = json.loads(result.text, encoding='utf-8')
    return res


def handle(text, mic, profile, wxbot=None):
    """
    Responds to user-input, typically speech text

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
        wxbot -- wechat bot instance
    """
    logger = logging.getLogger(__name__)
    # get config
    if SLUG not in profile or \
       'key' not in profile[SLUG] or \
       (
           'location' not in profile[SLUG] and
           'location' not in profile
       ):
        mic.say('天气插件配置有误，插件使用失败', cache=True)
        return
    key = profile[SLUG]['key']
    if 'location' in profile[SLUG]:
        location = profile[SLUG]['location']
    else:
        location = profile['location']
    WEATHER_API = 'https://api.seniverse.com/v3/weather/daily.json'        
    SUGGESTION_API = 'https://api.seniverse.com/v3/life/suggestion.json'
    city = [u'北京',u'上海',u'崇明',u'石家庄',u'唐山',u'秦皇岛',u'邯郸',u'邢台',u'保定',u'张家口',u'承德',u'沧州',u'廊坊',u'衡水',u'太原',u'大同',u'阳泉',u'长治',u'晋城',u'朔州',u'晋中',u'运城',u'忻州',u'临汾',u'吕梁',u'呼和浩特',u'包头',u'乌海',u'赤峰',u'通辽',u'鄂尔多斯',u'呼伦贝尔',u'巴彦淖尔',u'乌兰察布',u'兴安盟',u'锡林郭勒盟',u'阿拉善盟',u'沈阳',u'大连',u'鞍山',u'抚顺',u'本溪',u'丹东',u'锦州',u'营口',u'阜新',u'辽阳',u'盘锦',u'铁岭',u'朝阳',u'葫芦岛',u'长春',u'吉林',u'四平',u'辽源',u'通化',u'白山',u'松原',u'白城',u'延边朝鲜族自治州',u'哈尔滨',u'齐齐哈尔',u'鸡西',u'鹤岗',u'双鸭山',u'大庆',u'伊春',u'佳木斯',u'七台河',u'牡丹江',u'黑河',u'绥化',u'大兴安岭地区',u'辖区',u'辖县',u'南京',u'无锡',u'徐州',u'常州',u'苏州',u'南通',u'连云港',u'淮安',u'盐城',u'扬州',u'镇江',u'泰州',u'宿迁',u'杭州',u'宁波',u'温州',u'嘉兴',u'湖州',u'绍兴',u'金华',u'衢州',u'舟山',u'台州',u'丽水',u'合肥',u'芜湖',u'蚌埠',u'淮南',u'马鞍山',u'淮北',u'铜陵',u'安庆',u'黄山',u'滁州',u'阜阳',u'宿州',u'六安',u'亳州',u'池州',u'宣城',u'福州',u'厦门',u'莆田',u'三明',u'泉州',u'漳州',u'南平',u'龙岩',u'宁德',u'南昌',u'景德镇',u'萍乡',u'九江',u'新余',u'鹰潭',u'赣州',u'吉安',u'宜春',u'抚州',u'上饶',u'济南',u'青岛',u'淄博',u'枣庄',u'东营',u'烟台',u'潍坊',u'济宁',u'泰安',u'威海',u'日照',u'莱芜',u'临沂',u'德州',u'聊城',u'滨州',u'菏泽',u'郑州',u'开封',u'洛阳',u'平顶山',u'安阳',u'鹤壁',u'新乡',u'焦作',u'濮阳',u'许昌',u'漯河',u'三门峡',u'南阳',u'商丘',u'信阳',u'周口',u'驻马店',u'省直辖县级行政区划',u'武汉',u'黄石',u'十堰',u'宜昌',u'襄阳',u'鄂州',u'荆门',u'孝感',u'荆州',u'黄冈',u'咸宁',u'随州',u'恩施土家族苗族自治州',u'省直辖县级行政区划',u'长沙',u'株洲',u'湘潭',u'衡阳',u'邵阳',u'岳阳',u'常德',u'张家界',u'益阳',u'郴州',u'永州',u'怀化',u'娄底',u'湘西土家族苗族自治州',u'广州',u'韶关',u'深圳',u'珠海',u'汕头',u'佛山',u'江门',u'湛江',u'茂名',u'肇庆',u'惠州',u'梅州',u'汕尾',u'河源',u'阳江',u'清远',u'东莞',u'中山',u'潮州',u'揭阳',u'云浮',u'南宁',u'柳州',u'桂林',u'梧州',u'北海',u'防城港',u'钦州',u'贵港',u'玉林',u'百色',u'贺州',u'河池',u'来宾',u'崇左',u'海口',u'三亚',u'三沙',u'省直辖县级行政区划',u'辖区',u'辖县',u'成都',u'自贡',u'攀枝花',u'泸州',u'德阳',u'绵阳',u'广元',u'遂宁',u'内江',u'乐山',u'南充',u'眉山',u'宜宾',u'广安',u'达州',u'雅安',u'巴中',u'资阳',u'阿坝藏族羌族自治州',u'甘孜藏族自治州',u'凉山彝族自治州',u'贵阳',u'六盘水',u'遵义',u'安顺',u'毕节',u'铜仁',u'黔西南布依族苗族自治州',u'黔东南苗族侗族自治州',u'黔南布依族苗族自治州',u'昆明',u'曲靖',u'玉溪',u'保山',u'昭通',u'丽江',u'普洱',u'临沧',u'楚雄彝族自治州',u'红河哈尼族彝族自治州',u'文山壮族苗族自治州',u'西双版纳傣族自治州',u'大理白族自治州',u'德宏傣族景颇族自治州',u'怒江傈僳族自治州',u'迪庆藏族自治州',u'拉萨',u'昌都地区',u'山南地区',u'日喀则地区',u'那曲地区',u'阿里地区',u'林芝地区',u'西安',u'铜川',u'宝鸡',u'咸阳',u'渭南',u'延安',u'汉中',u'榆林',u'安康',u'商洛',u'兰州',u'嘉峪关',u'金昌',u'白银',u'天水',u'武威',u'张掖',u'平凉',u'酒泉',u'庆阳',u'定西',u'陇南',u'临夏回族自治州',u'甘南藏族自治州',u'西宁',u'海东',u'海北藏族自治州',u'黄南藏族自治州',u'海南藏族自治州',u'果洛藏族自治州',u'玉树藏族自治州',u'海西蒙古族藏族自治州',u'银川',u'石嘴山',u'吴忠',u'固原',u'中卫',u'乌鲁木齐',u'克拉玛依',u'吐鲁番地区',u'哈密地区',u'昌吉回族自治州',u'博尔塔拉蒙古自治州',u'巴音郭楞蒙古自治州',u'阿克苏地区',u'克孜勒苏柯尔克孜自治州',u'喀什地区',u'和田地区',u'伊犁哈萨克自治州',u'塔城地区',u'阿勒泰地区',u'自治区直辖县级行政区划']
    for word in city:
        if word in text:
            location = word
    try:
        weather = fetch_weather(WEATHER_API, key, location)
        logger.debug("Weather report: ", weather)
        if weather.has_key('results'):
            daily = weather['results'][0]['daily']
            days = set([])
            day_text = [u'今天', u'明天', u'后天']
            for word in day_text:
                if word in text:
                    days.add(day_text.index(word))
            if not any(word in text for word in day_text):
                days = set([0, 1, 2])
            responds = u'%s天气：' % location
            analyze_res = ''
            for day in days:
                responds += u'%s：%s，%s到%s摄氏度。' % (day_text[day], daily[day]['text_day'], daily[day]['low'], daily[day]['high'])
                if day == 0:
                    suggestion = fetch_weather(SUGGESTION_API, key, location)
                    if suggestion.has_key('results'):
                        suggestion_text = suggestion['results'][0]['suggestion']['sport']['brief']
                        analyze_res = analyze_today(daily[day]['code_day'], suggestion_text)
            responds += analyze_res
            mic.say(responds, cache=True)
        else:
            mic.say('抱歉，我获取不到天气数据，请稍后再试', cache=True)
    except Exception, e:
        logger.error(e)
        mic.say('抱歉，我获取不到天气数据，请稍后再试', cache=True)
        
    
def isValid(text):
    """
        Returns True if the input is related to weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text for word in [u"天气", u"气温"])

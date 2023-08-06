#!/usr/bin/env python
# encoding:utf-8

import re
import hashlib
import pymysql
import json
import numbers
from yhb.ybasic.yrandom import get_random_string


def generate_abroad_org_no():
    org_no = get_random_string(charset=None, require_length=8) + "F"
    return org_no


def safe_json_loads(raw):
    try:
        return json.loads(raw)
    except:
        return None


def get_md5(raw):
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def valid_string(raw):
    try:
        if raw is None or len(raw.strip()) == 0 or raw.isspace() is True:
            return False
        else:
            return True
    except:
        return False


def trans_escape_character(raw):
    """
    mysql入库转义字符转换
    :param raw:
    :return:
    """
    return pymysql.escape_string(raw).replace("%", "%%") if raw else None


def deblank(raw):
    try:
        pattern = r"[a-zA-Z][\s\t\n\r\f]+[a-zA-Z]"
        if len(re.findall(pattern, raw)):
            return raw.strip()
        else:
            return re.sub(r"[\s\t\n\r\f]", "", raw.strip())
    except:
        return raw


def encode_name(raw, entity_status=False):
    try:
        if entity_status:
            raw = deblank(raw)
        if raw is None:
            return raw
        else:
            return raw.replace("(", "（").replace(")", "）").strip()
    except:
        return None


def decode_name(raw, entity_status=False):
    try:
        if entity_status:
            raw = deblank(raw)
        if raw is None:
            return raw
        else:
            return raw.replace("（", "(").replace("）", ")")
    except:
        return None


def is_tongyixinyong_valid(raw_code):
    tongyixinyong_code = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
        "G": 16,
        "H": 17,
        "J": 18,
        "K": 19,
        "L": 20,
        "M": 21,
        "N": 22,
        "P": 23,
        "Q": 24,
        "R": 25,
        "T": 26,
        "U": 27,
        "W": 28,
        "X": 29,
        "Y": 30,
    }
    tongyixinyong_weight = {
        1: 1,
        2: 3,
        3: 9,
        4: 27,
        5: 19,
        6: 26,
        7: 16,
        8: 17,
        9: 20,
        10: 29,
        11: 25,
        12: 13,
        13: 8,
        14: 24,
        15: 10,
        16: 30,
        17: 28
    }
    try:
        raw_code = raw_code.replace(" ", "").strip()
        if len(raw_code) != 18:
            return False
        num = 31 - sum(
            [tongyixinyong_weight[a[0] + 1] * tongyixinyong_code[a[1]] for a in enumerate(raw_code[:17])]) % 31
        if num == 31:
            num = 0
        current_num = tongyixinyong_code[raw_code[17]]
        if num == current_num:
            return True
        else:
            return False
    except Exception as e:
        return False


def is_zuzhijigou_valid(raw_code):
    zuzhijigou_code = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
        "G": 16,
        "H": 17,
        "I": 18,
        "J": 19,
        "K": 20,
        "L": 21,
        "M": 22,
        "N": 23,
        "O": 24,
        "P": 25,
        "Q": 26,
        "R": 27,
        "S": 28,
        "T": 29,
        "U": 30,
        "V": 31,
        "W": 32,
        "X": 33,
        "Y": 34,
        "Z": 35
    }
    zuzhijigou_weight = {
        1: 3,
        2: 7,
        3: 9,
        4: 10,
        5: 5,
        6: 8,
        7: 4,
        8: 2
    }
    try:
        num = 11 - sum([zuzhijigou_weight[a[0] + 1] * zuzhijigou_code[a[1]] for a in enumerate(raw_code[:8])]) % 11
        current_num = zuzhijigou_code[raw_code[8]]
        if num == 11:
            num = 0
        if num == current_num:
            return True
        else:
            return False
    except Exception as e:
        return False


def clean_country(raw):
    if raw is None or raw.strip() == "":
        return None
    country_code = {
        '阿富汗': '4',
        '阿尔巴尼亚': '8',
        '阿尔及利亚': '12',
        '美属萨摩亚': '16',
        '安道尔': '20',
        '安哥拉': '24',
        '安圭拉': '660',
        '南极洲': '10',
        '安提瓜和巴布达': '28',
        '阿根廷': '32',
        '亚美尼亚': '51',
        '阿鲁巴': '533',
        '澳大利亚': '36',
        '奥地利': '40',
        '阿塞拜疆': '31',
        '巴哈马': '44',
        '巴林': '48',
        '孟加拉国': '50',
        '巴巴多斯': '52',
        '白俄罗斯': '112',
        '比利时': '56',
        '伯利兹': '84',
        '贝宁': '204',
        '百慕大': '60',
        '不丹': '64',
        '玻利维亚': '68',
        '波黑': '70',
        '博茨瓦纳': '72',
        '布维岛': '74',
        '巴西': '76',
        '英属印度洋领地': '86',
        '文莱': '96',
        '保加利亚': '100',
        '布基纳法索': '854',
        '布隆迪': '108',
        '柬埔寨': '116',
        '喀麦隆': '120',
        '加拿大': '124',
        '佛得角': '132',
        '开曼群岛': '136',
        '中非': '140',
        '乍得': '148',
        '智利': '152',
        '中国': '156',
        '香港': '344',
        '澳门': '446',
        '台湾': '158',
        '圣诞岛': '162',
        '科科斯（基林）群岛': '166',
        '哥伦比亚': '170',
        '科摩罗': '174',
        '刚果（布）': '178',
        '刚果（金）': '180',
        '库克群岛': '184',
        '哥斯达黎加': '188',
        '科特迪瓦': '384',
        '克罗地亚': '191',
        '古巴': '192',
        '塞浦路斯': '196',
        '捷克': '203',
        '丹麦': '208',
        '吉布提': '262',
        '多米尼克': '212',
        '多米尼加': '214',
        '东帝汶': '626',
        '厄瓜多尔': '218',
        '埃及': '818',
        '萨尔瓦多': '222',
        '赤道几内亚': '226',
        '厄立特里亚': '232',
        '爱沙尼亚': '233',
        '埃塞俄比亚': '231',
        '福克兰群岛（马尔维纳斯）': '238',
        '法罗群岛': '234',
        '斐济': '242',
        '芬兰': '246',
        '法国': '250',
        '法属圭亚那': '254',
        '法属波利尼西亚': '258',
        '法属南部领地': '260',
        '加蓬': '266',
        '冈比亚': '270',
        '格鲁吉亚': '268',
        '德国': '276',
        '加纳': '288',
        '直布罗陀': '292',
        '希腊': '300',
        '格陵兰': '304',
        '格林纳达': '308',
        '瓜德罗普': '312',
        '关岛': '316',
        '危地马拉': '320',
        '几内亚': '324',
        '几内亚比绍': '624',
        '圭亚那': '328',
        '海地': '332',
        '赫德岛和麦克唐纳岛': '334',
        '洪都拉斯': '340',
        '匈牙利': '348',
        '冰岛': '352',
        '印度': '356',
        '印度尼西亚': '360',
        '伊朗': '364',
        '伊拉克': '368',
        '爱尔兰': '372',
        '以色列': '376',
        '意大利': '380',
        '牙买加': '388',
        '日本': '392',
        '约旦': '400',
        '哈萨克斯坦': '398',
        '肯尼亚': '404',
        '基里巴斯': '296',
        '朝鲜': '408',
        '韩国': '410',
        '科威特': '414',
        '吉尔吉斯斯坦': '417',
        '老挝': '418',
        '拉脱维亚': '428',
        '黎巴嫩': '422',
        '莱索托': '426',
        '利比里亚': '430',
        '利比亚': '434',
        '列支敦士登': '438',
        '立陶宛': '440',
        '卢森堡': '442',
        '前南巴其顿': '807',
        '马达加斯加': '450',
        '马拉维': '454',
        '马来西亚': '458',
        '马尔代夫': '462',
        '马里': '466',
        '马耳他': '470',
        '马绍尔群岛': '584',
        '马提尼克': '474',
        '毛里塔尼亚': '478',
        '毛里求斯': '480',
        '马约特': '175',
        '墨西哥': '484',
        '密克罗尼西亚联邦': '583',
        '摩尔多瓦': '498',
        '摩纳哥': '492',
        '蒙古': '496',
        '蒙特塞拉特': '500',
        '摩洛哥': '504',
        '莫桑比克': '508',
        '缅甸': '104',
        '纳米比亚': '516',
        '瑙鲁': '520',
        '尼泊尔': '524',
        '荷兰': '528',
        '荷属安的列斯': '530',
        '新喀里多尼亚': '540',
        '新西兰': '554',
        '尼加拉瓜': '558',
        '尼日尔': '562',
        '尼日利亚': '566',
        '纽埃': '570',
        '诺福克岛': '574',
        '北马里亚纳': '580',
        '挪威': '578',
        '阿曼': '512',
        '巴基斯坦': '586',
        '帕劳': '585',
        '巴勒斯坦': '275',
        '巴拿马': '591',
        '巴布亚新几内亚': '598',
        '巴拉圭': '600',
        '秘鲁': '604',
        '菲律宾': '608',
        '皮特凯恩': '612',
        '波兰': '616',
        '葡萄牙': '620',
        '波多黎各': '630',
        '卡塔尔': '634',
        '留尼汪': '638',
        '罗马尼亚': '642',
        '俄罗斯联邦': '643',
        '卢旺达': '646',
        '圣赫勒拿': '654',
        '圣基茨和尼维斯': '659',
        '圣卢西亚': '662',
        '圣皮埃尔和密克隆': '666',
        '圣文森特和格林纳丁斯': '670',
        '萨摩亚': '882',
        '圣马力诺': '674',
        '圣多美和普林西比': '678',
        '沙特阿拉伯': '682',
        '塞内加尔': '686',
        '塞舌尔': '690',
        '塞拉利昂': '694',
        '新加坡': '702',
        '斯洛伐克': '703',
        '斯洛文尼亚': '705',
        '所罗门群岛': '90',
        '索马里': '706',
        '南非': '710',
        '南乔治亚岛和南桑德韦奇岛': '239',
        '西班牙': '724',
        '斯里兰卡': '144',
        '苏丹': '736',
        '苏里南': '740',
        '斯瓦尔巴岛和扬马延岛': '744',
        '斯威士兰': '748',
        '瑞典': '752',
        '瑞士': '756',
        '叙利亚': '760',
        '塔吉克斯坦': '762',
        '坦桑尼亚': '834',
        '泰国': '764',
        '多哥': '768',
        '托克劳': '772',
        '汤加': '776',
        '特立尼克和多巴哥': '780',
        '突尼斯': '788',
        '土耳其': '792',
        '土库曼斯坦': '795',
        '特克斯和凯科斯群岛': '796',
        '图瓦卢': '798',
        '乌干达': '800',
        '乌克兰': '804',
        '阿联酋': '784',
        '英国': '826',
        '美国': '840',
        '美国本土外小岛屿': '581',
        '乌拉圭': '858',
        '乌兹别克斯坦': '860',
        '瓦努阿图': '548',
        '梵蒂冈': '336',
        '委内瑞拉': '862',
        '越南': '704',
        '英属维尔京群岛': '92',
        '美属维尔京群岛': '850',
        '瓦利斯和富图纳': '876',
        '西撒哈拉': '732',
        '也门': '887',
        '南斯拉夫': '891',
        '赞比亚': '894',
        '津巴布韦': '716',
        '中国香港': '344',
        '中国台湾': '158',
        '泽西岛(英)': '832',
        '安徽省六安市霍邱县户胡镇街道': '156'
    }
    if raw in country_code:
        return country_code[raw]
    else:
        return raw


def generate_eid(org_no, main_credential_type="13"):
    try:
        if org_no:
            raw = main_credential_type + org_no
            return get_md5(raw)
        else:
            return None
    except Exception as e:
        return None


def dedup_all_field_list_dict(raw):
    try:
        return [dict(t) for t in {tuple(d.items()) for d in raw}]
    except Exception as e:
        return raw


def float_format(num, dig=6):
    try:
        if isinstance(num, str):
            return format(float(num), '.{0}f'.format(dig))
        elif isinstance(num, numbers.Number):
            return format(num, '.{0}f'.format(dig))
        else:
            return num
    except Exception as e:
        return None

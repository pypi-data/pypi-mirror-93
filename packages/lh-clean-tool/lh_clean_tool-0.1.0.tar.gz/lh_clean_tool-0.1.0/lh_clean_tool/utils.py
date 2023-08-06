#!/usr/bin/env python
# encoding:utf-8

import re
import time
from yhb.ydb.ymysql import MysqlWrapper
from .universal_utils import trans_escape_character, encode_name, valid_string, get_md5


def get_area_code_from_area_name(areaname, database_credit_user, database_credit_password, database_credit_name,
                                 database_credit_host, database_credit_port):
    with MysqlWrapper(user=database_credit_user,
                      passwd=database_credit_password,
                      db=database_credit_name,
                      host=database_credit_host,
                      port=database_credit_port) as mw:
        area_raw = mw.select(
            "select area_code from lh_manual_area where area_name = '{0}' and valid = 1 limit 1".format(
                trans_escape_character(areaname)))
    if len(area_raw) == 0:
        return "000000"
    else:
        return area_raw[0].get("area_code")


def is_exist(comp_name, database_entity_user, database_entity_password, database_entity_name, database_entity_host,
             database_entity_port):
    """
    主体名称是否在name表中存在
    :param comp_name:
    :return:
    """
    with MysqlWrapper(user=database_entity_user,
                      passwd=database_entity_password,
                      db=database_entity_name,
                      host=database_entity_host,
                      port=database_entity_port) as tgt:
        sql = "select id from lh_bond_entity_name where valid = 1 and entity_name_rel='{0}'".format(
            trans_escape_character(encode_name(comp_name, entity_status=True)))
        res = tgt.select(sql)
        if len(res) > 0:
            return True
        else:
            return False


def whether_gov_entity(entity_name,
                       database_credit_user, database_credit_password, database_credit_name, database_credit_host,
                       database_credit_port,
                       database_entity_user, database_entity_password, database_entity_name, database_entity_host,
                       database_entity_port,
                       subfix=True, is_core=0):
    """
    人民政府主体相关信息
    :param entity_name:
    :param subfix: 附属主体
    :return:
    """
    status = False
    eid = None
    gov_no = None

    if valid_string(entity_name) and "人民政府" in entity_name and entity_name[-4:] == "人民政府":
        status = True
        area = re.findall(r"(.*?)人民政府", entity_name)
        if len(area):
            area = area[0]
        else:
            area = "中国"
        area = get_area_code_from_area_name(area, database_credit_user, database_credit_password, database_credit_name,
                                            database_credit_host, database_credit_port)
        if area is not None and area != "000000":
            gov_no = "{0}GOV".format(area)
            eid = get_md5("21" + gov_no)
            if subfix:
                if valid_string(entity_name) and not is_exist(entity_name, database_entity_user,
                                                              database_entity_password, database_entity_name,
                                                              database_entity_host, database_entity_port):
                    send_to_entity(database_entity_user, database_entity_password, database_entity_name,
                                   database_entity_host,
                                   database_entity_port, entity_name, eid, None, None, None, gov_no=gov_no,
                                   is_person=False, country="156", is_core=is_core)
            else:
                send_to_entity(database_entity_user, database_entity_password, database_entity_name,
                               database_entity_host,
                               database_entity_port, entity_name, eid, None, None, None, gov_no=gov_no,
                               is_person=False, country="156", is_core=is_core)

    return status, eid, gov_no


def _get_main_credential_type_and_number(credit_no, org_no, country, gov_no=None):
    """
    证件类型与证件号判断
    :param credit_no:
    :param org_no:
    :param reg_no:
    :return:
    """
    # 工商注册号	12
    # 组织机构代码证	13
    # 社会统一信用代码证（三证合一后的营业执照）	15
    # 海外主体联合代码	20

    # 境内
    if country == "156":
        if gov_no is not None:
            return "21", gov_no
        if org_no is not None:
            return "13", org_no
        if credit_no is not None:
            return "15", credit_no
        return None, None
    # 境外
    else:
        return "20", org_no


def save_to_entity(insert_dict, database_entity_user, database_entity_password, database_entity_name,
                   database_entity_host, database_entity_port, src_table_name=None):
    """
    lh_bond_entity 清洗逻辑
    :param insert_dict:
    :param src_table_name:
    :return:
    """
    entity_name = insert_dict.get("entity_name")

    if entity_name is not None and len(entity_name) > 4:

        with MysqlWrapper(user=database_entity_user,
                          passwd=database_entity_password,
                          db=database_entity_name,
                          host=database_entity_host,
                          port=database_entity_port) as tgt:
            sql = "select id,eid,entity_type,reg_administration, entity_name,nationality,main_credential_type,main_credential_number from lh_bond_entity where valid = 1 and eid='{0}'".format(
                insert_dict.get("eid"))
            res = tgt.select(sql)
            if len(res) == 0:
                # 不分公示系统源表

                tgt.insert("lh_bond_entity", **insert_dict)
            else:
                # 公示系统-登记信息表
                if src_table_name is not None:
                    for a in res:
                        old_value = get_md5("".join([str(a.get("eid")),
                                                     str(a.get("entity_type")),
                                                     str(a.get("reg_administration")),
                                                     str(a.get("entity_name")),
                                                     str(a.get("nationality")),
                                                     str(a.get("main_credential_type")),
                                                     str(a.get("main_credential_number"))
                                                     ])
                                            )

                        new_value = get_md5("".join([str(insert_dict.get("eid")),
                                                     str(insert_dict.get("entity_type")),
                                                     str(insert_dict.get("reg_administration")),
                                                     str(insert_dict.get("entity_name")),
                                                     str(insert_dict.get("nationality")),
                                                     str(insert_dict.get("main_credential_type")),
                                                     str(insert_dict.get("main_credential_number"))
                                                     ])
                                            )
                        if old_value == new_value:
                            tgt.update("update lh_bond_entity set update_time =NOW() where id={0}".format(a.get("id")))
                        else:

                            tgt.insert("lh_bond_entity", **insert_dict)
                            tgt.update(
                                "update lh_bond_entity set update_time =NOW(),valid=0 where id={0}".format(a.get("id")))
                # 其他公式系统表-不操作


def save_to_entity_name(insert_dict, database_entity_user, database_entity_password, database_entity_name,
                        database_entity_host, database_entity_port, src_table_name=None):
    """
    lh_bond_entity_name清洗逻辑
    :param insert_dict:
    :param src_table_name:
    :return:
    """
    entity_name = insert_dict.get("entity_name_rel")

    if entity_name is not None and len(entity_name) > 4:

        with MysqlWrapper(user=database_entity_user,
                          passwd=database_entity_password,
                          db=database_entity_name,
                          host=database_entity_host,
                          port=database_entity_port) as tgt:
            sql = "select id ,entity_name_rel from lh_bond_entity_name where valid=1 and eid='{0}' and entity_name_type='01'".format(
                insert_dict.get("eid"))
            res = tgt.select(sql)
            new_name = insert_dict.get("entity_name_rel")
            if len(res) == 0:
                tgt.insert("lh_bond_entity_name", **insert_dict)
            else:
                # 登记信息
                if src_table_name is not None:
                    for a in res:
                        old_name = a.get("entity_name_rel")

                        if old_name != new_name:
                            sql_name = "select id from lh_bond_entity_name where valid=1 and eid='{0}' and entity_name_type='05' and entity_name_rel='{1}' ".format(
                                insert_dict.get("eid"), trans_escape_character(old_name))
                            res_name = tgt.select(sql_name)
                            if len(res_name) == 0:
                                tgt.insert("lh_bond_entity_name", **insert_dict)
                                tgt.update(
                                    "update lh_bond_entity_name set entity_name_type='05',update_time=NOW() where id={0}".format(
                                        a.get("id")))
                            else:
                                tgt.update(
                                    "update lh_bond_entity_name set entity_name_rel='{0}' ,update_time=NOW(),create_time=NOW() where id={1}".format(
                                        trans_escape_character(new_name), a.get("id")))

            tgt.update(
                "update lh_bond_entity_name set valid=0, update_time=NOW() where entity_name_type='05' and entity_name_rel='{0}'".format(
                    trans_escape_character(new_name)))


def save_to_keyword(insert_dict, database_entity_user, database_entity_password, database_entity_name,
                    database_entity_host, database_entity_port):
    """
    lh_bond_entity_keyword更新
    :param insert_dict:
    :return:
    """
    # keyword =pymysql.escape_string(insert_dict.get("keyword")).replace("%","%%")
    if insert_dict.get("keyword") is not None and len(insert_dict.get("keyword").strip().replace(" ", "")) > 4:
        with MysqlWrapper(user=database_entity_user,
                          passwd=database_entity_password,
                          db=database_entity_name,
                          host=database_entity_host,
                          port=database_entity_port) as tgt:
            sql = "select id,keyword from lh_bond_entity_keyword  where valid=1 and keyword='{0}'".format(
                trans_escape_character(insert_dict.get("keyword")))
            res = tgt.select(sql)
            if len(res) == 0:
                tgt.insert("lh_bond_entity_keyword", **insert_dict)


def save_to_credentials(insert_dict, database_entity_user, database_entity_password, database_entity_name,
                        database_entity_host, database_entity_port, src_table_name=None):
    """
    lh_bond_credentials更新
    :param insert_dict:
    :param src_table_name:
    :return:
    """
    with MysqlWrapper(user=database_entity_user,
                      passwd=database_entity_password,
                      db=database_entity_name,
                      host=database_entity_host,
                      port=database_entity_port) as tgt:
        sql = "select id,eid,credential_type,credential_number,issuing_authority,issuing_date,validity_from,expiry_date from lh_bond_credentials where valid=1 and eid='{0}' and credential_type='{1}'".format(
            insert_dict.get("eid"), str(insert_dict.get("credential_type")))
        res = tgt.select(sql)
        if len(res) == 0:
            tgt.insert("lh_bond_credentials", **insert_dict)
        else:
            if src_table_name is not None:
                new_value = get_md5("".join([str(insert_dict.get("eid")),
                                             str(insert_dict.get("credential_type")),
                                             str(insert_dict.get("credential_number")),
                                             str(insert_dict.get("issuing_authority")),
                                             str(insert_dict.get("issuing_date")),
                                             str(insert_dict.get("validity_from")),
                                             str(insert_dict.get("expiry_date"))
                                             ])
                                    )
                old_md5s = [get_md5("".join([str(a.get("eid")),
                                             str(a.get("credential_type")),
                                             str(a.get("credential_number")),
                                             str(a.get("issuing_authority")),
                                             str(a.get("issuing_date")),
                                             str(a.get("validity_from")),
                                             str(a.get("expiry_date"))
                                             ])
                                    ) for a in res]
                if new_value not in old_md5s:
                    tgt.insert("lh_bond_credentials", **insert_dict)


def send_to_entity(database_entity_user, database_entity_password, database_entity_name, database_entity_host,
                   database_entity_port,
                   entity_name, eid, credit_no, org_no, reg_no, gov_no=None, is_person=False, country=None,
                   compcode=None, src_table_name=None, is_core=0):
    """
    公示系统主体库清洗
    :param entity_name:
    :param eid:
    :param credit_no:
    :param org_no:
    :param reg_no:
    :param gov_no:
    :param compcode:
    :param is_person:
    :param country:
    :return:
    """
    valid = 1
    if not valid_string(entity_name):
        return 0

    # 自然人-entity
    if eid is not None and is_person:
        entity_dict = {
            "eid": eid,
            "entity_type": "1",
            "reg_administration": "0",
            "entity_name": encode_name(entity_name, entity_status=True),
            "nationality": country,
            "valid": valid,
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        save_to_entity(entity_dict, database_entity_user, database_entity_password, database_entity_name,
                       database_entity_host, database_entity_port, src_table_name=src_table_name)

    # 机构-entity/entity_name/keyword/credial
    elif eid is not None and not is_person:
        keyword_dict = {"keyword": encode_name(entity_name, entity_status=True),
                        "comp_code": compcode,
                        "comp_reg_address": country,
                        "is_historical_name": 0,
                        "is_core": is_core,
                        "valid": valid,
                        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        }
        save_to_keyword(keyword_dict, database_entity_user, database_entity_password, database_entity_name,
                        database_entity_host, database_entity_port)

        if country is not None:
            main_credential_type, main_credential_number = _get_main_credential_type_and_number(credit_no, org_no,
                                                                                                country, gov_no=gov_no)

            entity_dict = {
                "eid": eid,
                "entity_type": "0",
                "reg_administration": credit_no[0] if credit_no is not None else None,
                "entity_name": encode_name(entity_name, entity_status=True),
                "nationality": country,
                "main_credential_type": main_credential_type,
                "main_credential_number": main_credential_number,
                "valid": valid,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            entity_name_dict = {"eid": eid,
                                "entity_name_type": "01",
                                "entity_name_rel": encode_name(entity_name, entity_status=True),
                                "valid": valid,
                                "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                }
            save_to_entity(entity_dict, database_entity_user, database_entity_password, database_entity_name,
                           database_entity_host, database_entity_port, src_table_name=src_table_name)
            save_to_entity_name(entity_name_dict, database_entity_user, database_entity_password, database_entity_name,
                                database_entity_host, database_entity_port, src_table_name=src_table_name)

            # 境外
            if country != "156":
                credentials_dict = {"eid": eid,
                                    "credential_type": "20",
                                    "credential_number": org_no,
                                    "valid": valid,
                                    "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                    "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                    }

                save_to_credentials(credentials_dict, database_entity_user, database_entity_password,
                                    database_entity_name, database_entity_host, database_entity_port,
                                    src_table_name=src_table_name)
            # 境内
            else:
                # for a, b in [("15", credit_no), ("13", org_no), ("12", reg_no), ("21", gov_no)]:
                for a, b in [("15", credit_no), ("13", org_no), ("21", gov_no)]:
                    if b is None:
                        continue
                    b = b.strip().replace(" ", "")
                    if a == "15" and len(b) != 18:
                        continue
                    if a == "13" and len(b) != 9:
                        continue
                    credentials_dict = {"eid": eid,
                                        "credential_type": a,
                                        "credential_number": b,
                                        "valid": valid,
                                        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                        "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                        }

                    save_to_credentials(credentials_dict, database_entity_user, database_entity_password,
                                        database_entity_name, database_entity_host, database_entity_port,
                                        src_table_name=src_table_name)

    # 机构【没有eid】-keyword
    elif eid is None and not is_person:
        keyword_dict = {"keyword": encode_name(entity_name, entity_status=True),
                        "comp_code": compcode,
                        "comp_reg_address": country,
                        "is_historical_name": 0,
                        "is_core": is_core,
                        "valid": valid,
                        "create_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        }
        save_to_keyword(keyword_dict, database_entity_user, database_entity_password, database_entity_name,
                        database_entity_host, database_entity_port)

    else:
        pass
    return 1

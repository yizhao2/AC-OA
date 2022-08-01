#!/usr/bin/env python

import logging
import traceback

from lib.core import get_init_py_object

from tools import db_tools

from config.box import box_manger

sql_box = box_manger.get('sql')

TAG = 'R'
def add_actions(name, url, view):
    try:
        sql = sql_box.get('interface', 'get_interface_by_url')
        if not db_tools.exec_sql(sql, values=(url), is_query=True):
            sql = sql_box.get('interface', 'insert_interface')
            if hasattr(view, 'get'): db_tools.exec_sql(sql, values=(1, name, name, url, 'GET', 1, 0, ''), is_query=False)
            if hasattr(view, 'post'): db_tools.exec_sql(sql, values=(1, name, name, url, 'POST', 1, 0, ''), is_query=False)
            if hasattr(view, 'delete'): db_tools.exec_sql(sql, values=(1, name, name, url, 'DELETE', 1, 0, ''), is_query=False)
            logging.warning("database register " + url + " interface.")
        else:
            logging.warning("database " + url + " interface  already exist")
    except Exception:
        traceback.print_exc()

def get_api_url(view_name):
    buf_url = ''
    for s in view_name:
        if s.isupper():
            s = '/' + s.lower()
        buf_url += s
    return buf_url

# 注册views
def register_views(api, views):
    global TAG
    views_class_dict = get_init_py_object(views, TAG, -1)
    for name, view in views_class_dict.items():
        url = '/api' + get_api_url(name)
        add_actions(name, url, view)
        # add_actions(name, url1, view)
        api.add_resource(view, url)
#

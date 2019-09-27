#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 下午1:09
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : init_area.py
# 所有脚本必须实现run()方法
# 调用方法 python manage.py runscript init_area
import json
import os

from apps.common.models import Area

FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/area.json')


def run():
    print('begin ...')
    with open(FILE_PATH) as f:
        area_json = json.loads(f.read())
        for province in area_json:
            province_name = province['name']
            province_code = province['code']
            province_obj = Area(name=province_name, code=province_code)
            province_obj.save()
            city_list = province['children']
            for city in city_list:
                city_name = city['name']
                city_code = city['code']
                city_obj = Area(name=city_name, code=city_code, parent=province_obj)
                city_obj.save()
                district_list = city['children']
                for district in district_list:
                    district_name = district['name']
                    district_code = district['code']
                    district_obj = Area(name=district_name, code=district_code, parent=city_obj)
                    district_obj.save()
            print(province_name + 'done')

    print('end')
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 18:14:03 2023

@author: narut
"""

from configparser import ConfigParser


def read_db_config(filename='config.ini', section='mysql'):
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db_config
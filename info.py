"""
:copyright: Copyright (c) 2020 Jeremiah Ikosin (@ziord)
:license: MIT, see LICENSE for more details
"""

import json, os


def get_info():
    fp_lst = os.path.dirname(os.path.abspath(__file__))
    tmp = os.path.sep.join(['assets', "_info.json"])
    pkg_file_path = os.path.join(fp_lst, tmp)
    with open(pkg_file_path) as file:
        json_data = json.load(file)
    return json_data

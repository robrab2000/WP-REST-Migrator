""" Wordpress REST Migrator (WRM) Application.
WRM is a free and open source tool for Wordpress which helps you to export
or migrate your Wordpress site using the Wordpress REST API.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

Copyright 2018, Robert J Homewood
"""
__author__ = "Robert J Homewood"
__contact__ = "rob.homewood@googlemail.com"
__copyright__ = "Copyright 2018, Robert J Homewood"
__credits__ = ["Robert J Homewood"]
__date__ = "2018/01/08"
__deprecated__ = False
__email__ =  "rob.homewood@googlemail.com"
__license__ = "GPLv3"
__maintainer__ = "Robert J Homewood"
__version__ = "0.0.1"

import argparse, importlib, os, sys
from wordpress import API

parser = argparse.ArgumentParser(description='Minecraft Resource Pack Picker.')
parser.add_argument('--config', dest='config', default='default-config', help='specify config library')
args = parser.parse_args()

CFG = importlib.import_module('config.' + args.config)

wpapi1 = API(
    url=CFG.WP1_ADDRESS,
    consumer_key=CFG.WP1_KEY,
    consumer_secret=CFG.WP1_SECRET,
    api="wp-json",
    version="wp/v2",
    wp_user=CFG.WP1_USER_NAME,
    wp_pass=CFG.WP1_PASSWORD,
    oauth1a_3leg=True,
    creds_store="~/.wc-api-creds.json",
    callback=CFG.WP1_ADDRESS + '/oauth1_callback'
)
wpapi2 = API(
    url=CFG.WP2_ADDRESS,
    consumer_key=CFG.WP2_KEY,
    consumer_secret=CFG.WP2_SECRET,
    api="wp-json",
    version="wp/v2",
    wp_user=CFG.WP2_USER_NAME,
    wp_pass=CFG.WP2_PASSWORD,
    basic_auth = True,
    user_auth = True
)

if __name__ == "__main__":

    posts = wpapi2.get("posts")
    for post in posts.json():
        print(post)
    # print(posts.json())
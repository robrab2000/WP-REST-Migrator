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

import argparse, importlib, os, sys, json
from wordpress import API
from bs4 import BeautifulSoup

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



def get_posts():
    """function to gather the posts from  wp1"""
    posts = wpapi2.get("posts")
    return posts

def handle_posts(posts):
    """function to handle the list of posts"""
    for post in posts.json():
        for k, v in post.items():
            if k == 'content':
                handle_post_content(v)
            elif k == 'author':
                handle_post_author(v)
            elif k == 'featured_media':
                handle_post_featured_media(v)
            elif k == 'categories':
                handle_post_categories(v)
            elif k == 'tags':
                handle_post_tags(v)
        break

def handle_post_content(content):
    """function to handle the content of a post"""
    # print("V1", type(content), content)
    soup = BeautifulSoup(content['rendered'], "html.parser")  # , from_encoding="iso-8859-1")
    imgs = soup.findAll('img')
    for img in imgs:
        img_link = str(img).split('src="')[1].split('"')[0]
        if img_link in str(content):
            content = handle_image(img_link, content)
    # print("V2", type(content), content)

def handle_image(image_link, content):
    """function to handle an image"""
    content['rendered'] = content['rendered'].replace(image_link, "NULL_GOES_HERE")
    return content


def handle_post_author(author):
    """function to handle the author of a post"""
    # print("author:", author)
    # users = wpapi2.get("user")
    # user_json = json.loads(users.text)
    # for user in user_json:
    #     print(user)

    pass

def handle_post_featured_media(featured_media):
    """function to handle the featured_media of a post"""
    # print("featured media:", featured_media)

    pass

def handle_post_categories(categories):
    """function to handle the categories of a post"""
    # print("categories:", categories)
    # categories =
    pass

def handle_post_tags(tags):
    """function to handle the tags of a post"""
    # print("tags:", tags)
    tags_object = wpapi2.get("tags")
    # for user in users.text:
    #     print(user)
    tags = json.loads(tags_object.text)
    for tag in tags:
        tag_data = wpapi2.get("tags", id=tag['id'])
        print(tag_data) # TRY CLONING THE API REPO AND THEN EDITING IT TO ADD MY OWN KWARGS MAYBE?
        # print(tag)
        pass
    pass

if __name__ == "__main__":

    posts = get_posts()
    handle_posts(posts)


## composition of post json
# id
# date
# date_gmt
# guid
# modified
# modified_gmt
# slug
# status
# type
# link
# title
# content *
# excerpt
# author *
# featured_media *
# comment_status
# ping_status
# sticky
# template
# format
# meta
# categories *
# tags *
# _links
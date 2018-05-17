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
    creds_store="~/.wc-api-creds-wp-from.json",
    callback= CFG.WP1_CALLBACK_URL # REMEMBER TO DISABLE reCAPCHA
)
wpapi2 = API(
    url=CFG.WP2_ADDRESS,
    consumer_key=CFG.WP2_KEY,
    consumer_secret=CFG.WP2_SECRET,
    api="wp-json",
    version="wp/v2",
    wp_user=CFG.WP2_USER_NAME,
    wp_pass=CFG.WP2_PASSWORD,
    oauth1a_3leg=True,
    creds_store="~/.wc-api-creds-wp-to.json",
    callback=CFG.WP2_CALLBACK_URL  # REMEMBER TO DISABLE reCAPCHA
)

# wp 1 data storage. these should all be in json dict format
post_data = []
author_data = []
media_data = []
category_data = []
tag_data = []
tag_id_data = []

post_data_prepared = []


def get_post_data():
    """function to gather the posts from  wp1"""
    pages = wpapi1.get("posts?per_page=" + str(CFG.ENTRIES_PER_PAGE)).headers['X-WP-TotalPages']
    for page in range(1, int(pages) + 1):
        print(f"attempting to gather {CFG.ENTRIES_PER_PAGE} posts from page ({page}/{pages})")
        posts = wpapi1.get(f"posts?per_page={CFG.ENTRIES_PER_PAGE}&page={page}")
        i = 0
        for post in posts.json():
            i += 1
            post_json_dump = json.dumps(post)
            post_json = json.loads(post_json_dump)
            post_data.append(post_json)
            if i == 1:
                break
        break

def get_author_data():
    """function to gather the authors from  wp1"""
    pages = wpapi1.get("users?per_page=" + str(CFG.ENTRIES_PER_PAGE)).headers['X-WP-TotalPages']
    for page in range(1, int(pages) + 1):
        print(f"attempting to gather {CFG.ENTRIES_PER_PAGE} users from page ({page}/{pages})")
        users = wpapi1.get(f"users?per_page={CFG.ENTRIES_PER_PAGE}&page={page}")
        for user in users.json():
            user_json_dump = json.dumps(user)
            user_json = json.loads(user_json_dump)
            author_data.append(user_json)

def get_category_data():
    """function to gather the categories from  wp1"""
    pages = wpapi1.get("categories?per_page=" + str(CFG.ENTRIES_PER_PAGE)).headers['X-WP-TotalPages']
    for page in range(1, int(pages) + 1):
        print(f"attempting to gather {CFG.ENTRIES_PER_PAGE} categories from page ({page}/{pages})")
        categories = wpapi1.get(f"categories?per_page={CFG.ENTRIES_PER_PAGE}&page={page}")
        for category in categories.json():
            category_json_dump = json.dumps(category)
            category_json = json.loads(category_json_dump)
            category_data.append(category_json)

def get_tag_data():
    """function to gather the tags from  wp1"""
    pages = wpapi1.get("tags?per_page=" + str(CFG.ENTRIES_PER_PAGE)).headers['X-WP-TotalPages']
    for page in range(1, int(pages) + 1):
        print(f"attempting to gather {CFG.ENTRIES_PER_PAGE} tags from page ({page}/{pages})")
        tags = wpapi1.get(f"tags?per_page={CFG.ENTRIES_PER_PAGE}&page={page}")
        for tag in tags.json():
            tag_json_dump = json.dumps(tag)
            tag_json = json.loads(tag_json_dump)
            tag_data.append(tag_json)
            tag_id_data.append(tag_json['id'])


def get_wp1_data():
    """funtion to gather the various data from wp1"""
    get_post_data()
    get_author_data()
    get_category_data()
    get_tag_data()
    # get_menu_data()

def handle_posts():
    """function to handle the list of posts"""

    for post in post_data:
        new_post = {}
        print(post['id'])
        post_media = json.loads(wpapi1.get("media?parent=" + str(post['id'])).content)
        new_post['title'] = handle_post_title(post['title'])
        new_post['content'] = handle_post_content(post['content'], post_media)
        new_post['status'] = handle_post_status(post['status'])
        new_post['excerpt'] = handle_post_excerpt(post['excerpt'])
        # new_post['author'] = handle_post_author(post['author'])
        # new_post['featured_media'] = handle_post_featured_media(post['featured_media'])
        new_post['categories'] = handle_post_categories(post['categories'])
        new_post['tags'] = handle_post_tags(post['tags'])
        post_data_prepared.append(new_post)
    # print(len(post_data))

def handle_post_title(title):
    """function to handle the title of a post"""
    return title['rendered']


def handle_post_content(content, post_media):
    """function to handle the content of a post"""
    # print(f"V1: {type(content)} {content}")
    soup = BeautifulSoup(content['rendered'], "html.parser")  # , from_encoding="iso-8859-1")
    imgs = soup.findAll('img')
    for img in imgs:
        img_link = str(img).split('src="')[1].split('"')[0]
        if img_link in str(content):
            content = handle_image_in_content(img_link, content, post_media)
    # print(f"V2: {type(content)} {content}")
    return content['rendered'].replace("'", '\u0027').replace('"', '\'')

def handle_image_in_content(image_link, content, media_items):
    """function to handle an image"""
    # check that image is an internal link
    if str(CFG.WP1_ADDRESS).split('://')[1] in image_link:
        # retreive meta data about image
        new_media_item = {}
        for media_item in media_items:
            if str(media_item['source_url']).split('://')[1] == image_link.split('://')[1]:
                new_media_item['file'] = media_item['source_url']
                new_media_item['title'] = media_item['title']
                # print(media_item['content-type'])
                # new_media_item['content-type'] = media_item['content-type'] # I don't know if this will work

        # download the linked file

        # upload the new image
        content['rendered'] = content['rendered'].replace(image_link, "NULL_GOES_HERE")


    return content





def handle_featured_media(featured_media_id):
    """function to handle the featured media"""
    # retreive meta data about image

    # download the linked file

    # upload the new image

    # return the new image's id
    pass

def handle_post_excerpt(excerpt):
    """function to handle the post excerpt"""
    return excerpt['rendered'].replace("'", '\u0027').replace('"', '\'')


def handle_post_author(author_id):
    """function to handle the author of a post"""
    for author in author_data:
        # print(author)
        pass

def handle_post_featured_media(featured_media_id):
    """function to handle the featured_media of a post"""
    # print("featured media:", featured_media)

    pass

def handle_post_status(status):
    """function to handle the status of a post"""
    return status

def handle_post_categories(category_ids):
    """function to handle the categories of a post"""
    # for category in category_data:
    #     # print(category)
    #     pass
    wp2_categories = []
    pages = wpapi2.get("categories?per_page=" + str(CFG.ENTRIES_PER_PAGE)).headers['X-WP-TotalPages']
    for page in range(1, int(pages) + 1):
        categories = wpapi2.get(f"categories?per_page={CFG.ENTRIES_PER_PAGE}&page={page}")
        for category in categories.json():
            category_json_dump = json.dumps(category)
            category_json = json.loads(category_json_dump)
            wp2_categories.append(category_json)

    category_ids_to_return = []

    for category_id in category_ids:
        for category in category_data:
            if category['id'] == category_id:
                category_name = category['name']
                no_match = True
                for wp2_category in wp2_categories:
                    if wp2_category['name'] == category['name']:
                        category_ids_to_return.append(wp2_category['id'])
                        no_match = False
                if no_match == True:
                    new_category = wpapi2.post('categories', {'name': str(category_name)})
                    category_ids_to_return.append(json.loads(new_category.content)['id'])
    return category_ids_to_return

def handle_post_tags(tag_ids):
    """function to handle the tags of a post"""
    wp2_tags = []
    pages = wpapi2.get("tags?per_page=" + str(CFG.ENTRIES_PER_PAGE)).headers['X-WP-TotalPages']
    for page in range(1, int(pages) + 1):
        # print(f"attempting to gather {CFG.ENTRIES_PER_PAGE} tags from page ({page}/{pages})")
        tags = wpapi2.get(f"tags?per_page={CFG.ENTRIES_PER_PAGE}&page={page}")
        for tag in tags.json():
            tag_json_dump = json.dumps(tag)
            tag_json = json.loads(tag_json_dump)
            wp2_tags.append(tag_json)

    tag_ids_to_return = []

    for tag_id in tag_ids:
        for tag in tag_data:
            if tag['id'] == tag_id:
                tag_name = tag['name']
                no_match = True
                for wp2_tag in wp2_tags:
                    if wp2_tag['name'] == tag['name']:
                        tag_ids_to_return.append(wp2_tag['id'])
                        no_match = False
                if no_match == True:
                    new_tag = wpapi2.post('tags', {'name':str(tag_name)})
                    tag_ids_to_return.append(json.loads(new_tag.content)['id'])
    return tag_ids_to_return

def push_wp2_data():
    """function to push all the data over to the new wp site"""
    push_wp2_posts()

def push_wp2_posts():
    """function to push the posts over to the new wp site"""
    # for post in post_data:
    #     print(f"pushing post ({post_data.index(post)}/{len(post_data)})")
    #     wpapi2.post('post', post)
    for post in post_data_prepared:
        # new_post = json.dumps(post_data_prepared[0])
        # print(new_post)
        result = wpapi2.post("posts", post)
    # print(result.json())
    # print(wpapi1.get("posts"))
    # print(wpapi2.get("posts"))

if __name__ == "__main__":
    """main function to run the program"""
    get_wp1_data()
    handle_posts()

    push_wp2_data()


## composition of post json
# id
# date
# date_gmt
# guid
# modified
# modified_gmt
# slug
# status *
# type
# link
# title
# content *
# excerpt *
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
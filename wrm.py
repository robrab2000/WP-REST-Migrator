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
        for post in posts.json():
            post_json_dump = json.dumps(post)
            post_json = json.loads(post_json_dump)
            post_data.append(post_json)
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
        new_post['content'] = handle_post_content(post['content'])
        new_post['status'] = handle_post_status(post['status'])
        # new_post['author'] = handle_post_author(post['author'])
        new_post['featured_media'] = handle_post_featured_media(post['featured_media'])
        new_post['categories'] = handle_post_categories(post['categories'])
        new_post['tags'] = handle_post_tags(post['tags'])
        post_data_prepared.append(new_post)
    # print(len(post_data))

def handle_post_content(content):
    """function to handle the content of a post"""
    # print(f"V1: {type(content)} {content}")
    soup = BeautifulSoup(content['rendered'], "html.parser")  # , from_encoding="iso-8859-1")
    imgs = soup.findAll('img')
    for img in imgs:
        img_link = str(img).split('src="')[1].split('"')[0]
        if img_link in str(content):
            content = handle_image(img_link, content)
    # print(f"V2: {type(content)} {content}")

def handle_image(image_link, content):
    """function to handle an image"""
    content['rendered'] = content['rendered'].replace(image_link, "NULL_GOES_HERE")
    return content


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

def handle_post_categories(categories_ids):
    """function to handle the categories of a post"""
    for category in category_data:
        # print(category)
        pass

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

    for tag in tag_data:
        for tag_id in tag_ids:
            if tag['id'] == tag_id:
                tag_name = tag['name']

                for wp2_tag in wp2_tags:
                    if wp2_tag['name'] == tag_name:
                        break #this needs to break from nested loop but not sure how many

        if tag['id'] not in tag_ids:
            # tag_names.append(tag['name'])
            new_tag_data = {'name':tag['name']}
            new_tag = wpapi2.post('tags', new_tag_data)
            tag_ids_to_return.append(new_tag['id'])
        # if tag not in wp2_tags:
        #     new_tag = wpapi2.post('tags', tag)
        #     new_tag_id = new_tag['id']
        #     tag_ids_to_return.append(new_tag_id)
    return tag_ids_to_return

def push_wp2_data():
    """function to push all the data over to the new wp site"""
    push_wp2_posts()

def push_wp2_posts():
    """function to push the posts over to the new wp site"""
    # for post in post_data:
    #     print(f"pushing post ({post_data.index(post)}/{len(post_data)})")
    #     wpapi2.post('post', post)

    new_post = {"title": "Albert Watson: Kaos &#8211; Extended"}
    result = wpapi2.post("posts", new_post)
    print(result.json())
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
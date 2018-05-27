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

import argparse, importlib, os, sys, json, pickle, requests
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

wpapi2_basic = API(
    url=CFG.WP2_ADDRESS,
    consumer_key=CFG.WP2_KEY,
    consumer_secret=CFG.WP2_SECRET,
    api="wp-json",
    version="wp/v2",
    wp_user=CFG.WP2_USER_NAME,
    wp_pass=CFG.WP2_PASSWORD,
    basic_auth = True,
    user_auth = True,
    # oauth1a_3leg=True,
    # creds_store="~/.wc-api-creds-wp-to.json",
    # callback=CFG.WP2_CALLBACK_URL  # REMEMBER TO DISABLE reCAPCHA

    # url="http://example.com",
    # api="wp-json",
    # version='wp/v2',
    # wp_user="XXXX",
    # wp_pass="XXXX",


)

# wp 1 data storage. these should all be in json dict format
post_data = []
author_data = []
media_data = []
category_data = []
tag_data = []
tag_id_data = []

post_data_prepared = []
wp2_media_data = []


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
            # if i == 1:
            #     break
        # break

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

def get_media_data():
    """function to gather the tags from  wp1"""
    pages = wpapi1.get("media?per_page=" + str(CFG.ENTRIES_PER_PAGE)).headers['X-WP-TotalPages']
    for page in range(1, int(pages) + 1):
        print(f"attempting to gather {CFG.ENTRIES_PER_PAGE} media from page ({page}/{pages})")
        media_items = wpapi1.get(f"media?per_page={CFG.ENTRIES_PER_PAGE}&page={page}")
        for media_item in media_items.json():
            media_json_dump = json.dumps(media_item)
            media_json = json.loads(media_json_dump)
            media_data.append(media_json)
            # media_id_data.append(media_json['id'])

def get_wp2_media_data():
    """function to gather the tags from  wp2"""
    pages = wpapi2.get("media?per_page=" + str(CFG.ENTRIES_PER_PAGE)).headers['X-WP-TotalPages']
    for page in range(1, int(pages) + 1):
        # print(f"attempting to gather {CFG.ENTRIES_PER_PAGE} media from page ({page}/{pages}) from wp2")
        media_items = wpapi2.get(f"media?per_page={CFG.ENTRIES_PER_PAGE}&page={page}")
        for media_item in media_items.json():
            media_json_dump = json.dumps(media_item)
            media_json = json.loads(media_json_dump)
            media_data.append(media_json)
            # media_id_data.append(media_json['id'])

def get_wp1_data():
    """funtion to gather the various data from wp1"""
    get_media_data()
    get_post_data()
    get_author_data()
    get_category_data()
    get_tag_data()
    # get_menu_data()

def handle_posts():
    """function to handle the list of posts"""
    for post in post_data:
        new_post = {}
        # post_media = json.loads(wpapi1.get("media?parent=" + str(post['id'])).content)
        new_post['title'] = handle_post_title(post['title'])
        content_and_media_ids = handle_post_content(post['content'])
        new_post['content'] = content_and_media_ids[0]
        new_post['media_ids'] = content_and_media_ids[1]

        new_post['status'] = handle_post_status(post['status'])
        new_post['excerpt'] = handle_post_excerpt(post['excerpt'])
        # new_post['author'] = handle_post_author(post['author'])
        # new_post['featured_media'] = handle_post_featured_media(post['featured_media'])
        new_post['categories'] = handle_post_categories(post['categories'])
        new_post['tags'] = handle_post_tags(post['tags'])
        post_data_prepared.append(new_post)
        break

def handle_post_title(title):
    """function to handle the title of a post"""
    return title['rendered']


def handle_post_content(content):
    """function to handle the content of a post"""
    # print(f"V1: {type(content)} {content}")
    soup = BeautifulSoup(content['rendered'], "html.parser")  # , from_encoding="iso-8859-1")
    imgs = soup.findAll('img')

    media_id = []

    for img in imgs:
        img_link = str(img).split('src="')[1].split('"')[0]
        if img_link in str(content):
            content_with_media_id = handle_image_in_content(img_link, content)
            content = content_with_media_id[0]
            media_id.append(content_with_media_id[1])
    # print(f"V2: {type(content)} {content}")
    return (content['rendered'].replace("'", '\u0027').replace('"', '\''), media_id)

def handle_image_in_content(image_link, content):
    """function to handle an image"""
    new_media_id = None
    new_media_link = None
    # check that image is an internal link
    if str(CFG.WP1_ADDRESS).split('://')[1] in image_link:

        # check if the image is already in the media wp2 library
        get_wp2_media_data()
        for media_item in wp2_media_data:
            if str(media_item['source_url']).split('://')[1] in image_link.split('://')[1]:
                new_media_link = media_item['source_url']
                new_media_id = media_item['id']
        # retreive meta data about image
        new_media_item = {}
        for media_item in media_data:
            # print(str(media_item['source_url']).split('://')[1], image_link.split('://')[1])
            if str(media_item['source_url']).split('://')[1] in image_link.split('://')[1]:
                # new_media_item['file'] = media_item['source_url']
                new_media_item['title'] = media_item['title']
                # new_media_item['status'] = media_item['status']
                new_media_item['meta'] = media_item['meta']
                new_media_item['alt_text'] = media_item['alt_text']
                new_media_item['caption'] = media_item['caption']
                new_media_item['description'] = media_item['description']
                # new_media_item['content-type'] = media_item['content-type'] # I don't know if this will work

                filename = str(media_item['source_url']).rsplit('/', 1)[1]#.split('.')[0]
                extension = str(media_item['source_url']).rsplit('/', 1)[1].split('.')[1]

                # download the media file
                local_image_location = CFG.IMAGE_DUMP + "/" + filename
                # print(local_image_location)
                with open(local_image_location, 'wb') as f:
                    f.write(requests.get(media_item['source_url']).content)

                headers = {
                    'cache-control': 'no-cache',
                    'content-disposition': 'attachment; filename=%s' % filename,
                    'content-type': 'image/%s' % extension
                }

                data = open(local_image_location, 'rb').read()

                # upload the new image
                media_post_return = wpapi2_basic.post("media", data, headers=headers)

                new_media_id = json.loads(media_post_return.content)['id']
                new_media_link = media_item['source_url']


                # delete the dumped image
                os.remove(local_image_location)

                # update the image meta
                wpapi2.post("media/" + str(new_media_id), new_media_item)

        content['rendered'] = content['rendered'].replace(image_link, new_media_link)

        return_tuple = (content, new_media_id)

    #return the content as well as the image id so we can add the post id to it later
    return return_tuple


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

def serialize_wp1_data():
    """function to serialize the data from wp1"""
    data_to_serialize = {}
    data_to_serialize['post_data'] = post_data
    data_to_serialize['author_data'] = author_data
    data_to_serialize['media_data'] = media_data
    data_to_serialize['category_data'] = category_data
    data_to_serialize['tag_data'] = tag_data
    data_to_serialize['tag_id_data'] = tag_id_data

    for file_name, data in data_to_serialize.items():
        with open (CFG.DATA + "/" + file_name + ".txt", 'wb') as dump_file:
            pickle.dump(data, dump_file)

def deserialize_wp1_data():
    """function to serialize the data from wp1"""
    data_to_deserialize = {}
    data_to_deserialize['post_data'] = []
    data_to_deserialize['author_data'] = []
    data_to_deserialize['media_data'] = []
    data_to_deserialize['category_data'] = []
    data_to_deserialize['tag_data'] = []
    data_to_deserialize['tag_id_data'] = []

    for name in data_to_deserialize.keys():
        with open(CFG.DATA + "/" + name + ".txt", 'rb') as read_file:
            data_to_deserialize[name] = pickle.load(read_file)

    global post_data, author_data, media_data, category_data, tag_data, tag_id_data
    post_data = data_to_deserialize['post_data']
    author_data = data_to_deserialize['author_data']
    media_data = data_to_deserialize['media_data']
    category_data = data_to_deserialize['category_data']
    tag_data = data_to_deserialize['tag_data']
    tag_id_data = data_to_deserialize['tag_id_data']

    #  post_data = pickle.load(CFG.DATA + "/post_data.txt")
    # author_data = pickle.load(CFG.DATA + "/author_data.txt")
    # media_data = pickle.load(CFG.DATA + "/media_data.txt")
    # category_data = pickle.load(CFG.DATA + "/category_data.txt")
    # tag_data = pickle.load(CFG.DATA + "/tag_data.txt")
    # tag_id_data = pickle.load(CFG.DATA + "/tag_id_data.txt")

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
        media_ids = post['media_ids']
        del post['media_ids']
        result = wpapi2.post("posts", post)

        update_media_ids_for_post(json.loads(result.content)['id'], media_ids)

    # print(result.json())
    # print(wpapi1.get("posts"))
    # print(wpapi2.get("posts"))

def update_media_ids_for_post(post_id, media_ids):
    for media_id in media_ids:
        media_item_data = json.loads(wpapi2.get('media/' + str(media_id)).content)
        media_item_data['post'] = post_id
        del media_item_data['status']
        wpapi2_basic.post('media/' + str(media_id), media_item_data)

if __name__ == "__main__":
    """main function to run the program"""
    deserialize_wp1_data()
    # get_wp1_data()
    handle_posts()

    # serialize_wp1_data()
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
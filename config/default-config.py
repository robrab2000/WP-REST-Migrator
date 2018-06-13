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

# Entries to scrape per page
ENTRIES_PER_PAGE = 100

# Temp image location
IMAGE_DUMP = "./image_dump"

# serialized data storage
DATA = "./data"

## WP1 : Wordpress address being exported from
## WP2 : Wordpress address being exported to

## WP1 Config details

# Site address
WP1_ADDRESS = "https://example-site-one.com"
# User name
WP1_USER_NAME = "your-user-name"
# Password
WP1_PASSWORD = "your-user-password"
# Consumer key
WP1_KEY = "your-application-key"
# Consumer secret
WP1_SECRET = "your-application-secret"
# Credential storage
WP1_CRED_STORE = "./cred_store/.wc-api-creds-wp-from.json"
# Callback URL
WP1_CALLBACK_URL = WP1_ADDRESS + '/success.html'


## WP2 Config details

# Site address
WP2_ADDRESS = "https://example-site-two.com"
# User name
WP2_USER_NAME = "your-user-name"
# Password
WP2_PASSWORD = "your-user-password"
# Consumer key
WP2_KEY = "your-application-key"
# Consumer secret
WP2_SECRET = "your-application-secret"
# Credential storage
WP2_CRED_STORE = "./cred_store/.wc-api-creds-wp-to.json"
# Callback URL
WP2_CALLBACK_URL = WP2_ADDRESS + '/success.html'
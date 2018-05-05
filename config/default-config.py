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

## WP1 : Wordpress address being exported from
## WP2 : Wordpress address being exported to

## WP1 Config details

# Site address
WP1_ADDRESS = "https://"
# User name
WP1_USER_NAME = ""
# Password
WP1_PASSWORD = ""
# Consumer key
WP1_KEY = ""
# Consumer secret
WP1_SECRET = ""


## WP2 Config details

# Site address
WP2_ADDRESS = "https://"
# User name
WP2_USER_NAME = ""
# Password
WP2_PASSWORD = ""
# Consumer key
WP2_KEY = ""
# Consumer secret
WP2_SECRET = ""

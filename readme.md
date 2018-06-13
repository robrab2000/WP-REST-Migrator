# Wordpress REST Migrator (WRM)

WRM is a free and open source (GPLv3) tool for Wordpress which helps you to export
or migrate your Wordpress site using the Wordpress REST API.

The tool was developed out of my frustration with trying to migrate really big wordpress sites (>5gb) and finding that it was tricky to do using migration plugins. Of course one could always just perform a manual migration copying the database and the files but this can be tricky too (phpmyadmin can struggle with large imports).

This project takes a slightly different approach to migration. Instead of packaging up the whole site and migrating it all (the entire database and all the files), it migrates just the content of the wordpress site. Essentially, it uses the Wordpress REST api (thanks to [derwentx](https://github.com/derwentx/wp-api-python) for the excellent python wrapper) to go through each post on the site, extracting the content/metadata and then uploading them to a second wordpress site one by one. 

Not only does this approach work quite well for sites that are too big for traditional migration but it works does a good job of cleaning your site of bloat. Its a bit like dialysis.. A Wordpress database can get clogged up with old crap (mostly from installing and uninstalling plugins/themes), by migrating just the content that you actually NEED to a fresh Wordpress installation, you are left with a clean database and file system. (of course you will need to still set up everything else like themes and plugins again on the new site)

The package goes through the contents of each post and looks for media content (images), downloading each image and uploading it into the new site so that it gets indexed correctly. 

I built this for my own use but I'm happy to keep working on it if people find it useful.. Let me know :)

## tl;dr
- Use the Wordpress REST api to migrate from one Wordpress installation to another.
- This package is also great for cleaning up your wordpress.
- It extracts the content (posts, pages, comments, tags, media, etc.) and re-inserts all it one by one, replacing tags and media etc as needed so that they all have the correct ids.

<no-wiki> * </no-wiki>Remember to disable reCapcha from your sites before attempting the migration

### To Do:
- [x] Export posts (including media contained)
- [x] Export tags
- [x] Export categories
- [x] Export featured media
- [ ] Export pages (including media contained)
- [ ] Export menus
- [ ] Make wordpress plugin for automating application setup
- [ ] Allow post/page exclusions

## Requirements
- Python 3
- Two Wordpress installations with ftp/ssh access
- python libraries:
- * requests
- * BeautifulSoup4 
- * wordpress-api (a newer version can be found on their [GitHub page](https://github.com/derwentx/wp-api-python)

## Instructions for Use
- To use this tool, you should clone the repository onto your local machine

- `https://github.com/robrab2000/WP-REST-Migrator.git`

- Next you should have two wordpress site set up. One as a host that you will migrate from, the other is the receiver which will be migrated to. (in the config file they will be referred to as WP1 and WP2)

- On Each Wordpress installation you will need the following plugins installed:
- - [WP REST API - Meta Endpoints](https://en-gb.wordpress.org/plugins/rest-api-meta-endpoints/)
- - [WP REST API - OAuth 1.0a Server] (https://en-gb.wordpress.org/plugins/rest-api-oauth1/)
- - [WP REST API Controller] (https://en-gb.wordpress.org/plugins/wp-rest-api-controller/)
- - [JSON Basic Authentication] (https://github.com/WP-API/Basic-Auth) (this needs to be manually installed)

- Check that you have the correct ownership and permissions set for the directory that of the Wordpress installation you are migrating to
- Disable security plugins (including captcha and anything else you think might get in the way)
- Create a file called `success.html` and put a copy in both wp folders (this file can just contain `<p>Success!</p>`. I have included an example of this in the repo))
- Set up an Application found under "Users" menu (you can just use the details included in the Application Template found below)
- Copy and paste credentials into the default config file (or you can make your own config file which is prolly a better idea anyway)

- Run the python script

## Application Template
Title: `WP-REST Migrator`

Description: `Wordpress REST Migrator (WRM) Application.
WRM is a free and open source tool for Wordpress which helps you to export
or migrate your Wordpress site using the Wordpress REST API.`

Callback URL: `https://your-site.com/success.html`

## Notes
- Some hosting providers (basically most shared hosting environments) block ports for security reasons. This might throw a spanner in your works. In this case you will probably just need to speak with them and get them to allow the wordpress api through their firewall.
- I've noticed that sometimes your security plugins could get in the way. For example a Capcha on login will probably prevent it from authenticating. I think Wordfence should be alright but I just disabled it for good measure (of course its probably a good idea to re-enable it as soon as possible once you're done).


This software is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**.  See the GNU General Public License for more details.



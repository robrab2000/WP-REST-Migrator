# Wordpress REST Migrator (WRM)

WRM is a free and open source (GPLv3) tool for Wordpress which helps you to export
or migrate your Wordpress site using the Wordpress REST API.

The tool was developed out of frustration trying to migrate really big wordpress sites (>5gb) or cleaning up old and messy wp databases. 

- REST api export tool for wordpress
- Extract all posts, pages, comments, tags, media, etc. using REST
- Reinserts all posts one by one, replacing tags and media etc as needed so that they all have the correct ids

Remember to disable reCapcha from your sites before attempting the migration


## Instructions for Host:
- Disable security plugins (including captcha and anything else you think might get in the way)
- Install plugins:
- - JSON Basic Authentication (https://github.com/WP-API/Basic-Auth)
- - WP REST API - Meta Endpoints
- - WP REST API - OAuth 1.0a Server
- - WP REST API Controller
- Place a `success.html` in wp folder (this file can just contain `<p>Success!</p>`)
- Set up an Application found under "Users" menu (you can just use the Application template found below))
- Copy and paste credentials into config file

## Instructions for Receiver:
- Create empty wordpress 
- Check correct ownership and permissions
- Install plugins:
- - JSON Basic Authentication (https://github.com/WP-API/Basic-Auth)
- - WP REST API - Meta Endpoints
- - WP REST API - OAuth 1.0a Server
- - WP REST API Controller
- Place a `success.html` in wp folder (this file can just contain `<p>Success!</p>`)
- Set up an Application found under "Users" menu (you can just use the Application template found below))
- Copy and paste credentials into config file
- Run

## Application template
Title: `WP-REST Migrator`

Description: `Wordpress REST Migrator (WRM) Application.
WRM is a free and open source tool for Wordpress which helps you to export
or migrate your Wordpress site using the Wordpress REST API.`

Callback URL: `https://your-site.com/success.html`




## To Do:
[x] Export posts (including media contained)
[x] Export tags
[x] Export categories
[x] Export featured media
[ ] Export pages (including media contained)
[ ] Export menus

#!/usr/bin/env python
# coding: utf-8


#### Wordpress conf
WPURL = "https://wp.example.com"
MENU_NAME = "Top menu"

#### Script conf
BATCH = 50
PELICAN_PATH = "."
HTTP_BASIC_AUTH = ()

# Output folders for content
# Default for posts: $PELICAN_PATH/content
# Default for pages: $PELICAN_PATH/content/pages
OUTPUT_PATH_POSTS = ""
OUTPUT_PATH_PAGES = ""

LINKS_TO_REPLACE = [("https://wp.example.com", "https://pelican.example.com")]

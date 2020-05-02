#!/usr/bin/python3
# coding: utf-8

import requests
import queries
from jinja2 import Environment, FileSystemLoader
import os
import json

import sys, os
sys.path.append(os.curdir)
from wp2pelicanconf import *
from getfromwp import *



if __name__ == "__main__":
    print('Starting')
    posts = Content("posts", queries.get_posts, "post.html")
    posts.get_content()
    pages = Content("pages", queries.get_pages, "post.html")
    pages.get_content()
    menu = Menu(MENU_NAME)
    menu.get_menu()
    menu.write_menu()
    
    

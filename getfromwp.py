#!/usr/bin/env python
# coding: utf-8

import requests
import queries
from jinja2 import Environment, FileSystemLoader
import os
import json
import shutil
from bs4 import BeautifulSoup
import re

import sys, os
sys.path.append(os.curdir)
from wp2pelicanconf import *
import queries

if not HTTP_BASIC_AUTH:
    if "WP_PROXY_ID" in os.environ and "WP_PROXY_PWD" in os.environ:
        print("Setting up proxy identification")
        HTTP_BASIC_AUTH = (os.environ.get('WP_PROXY_ID'), os.environ.get('WP_PROXY_PWD'))
        

def run_query(query, variables={}):
    try:
        auth = HTTP_BASIC_AUTH
    except:
        auth = ""
    request = requests.post(WPURL, json={'query': query, 'variables': variables}, auth=auth)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def fetch_data(type, query):
    if type not in ["posts", "pages"]:
        print("The function fetch_data is not tested to handle anything else than posts or pages")
    print("Fetching the first %i %s" % (BATCH, type))
    data_to_get = {"first": BATCH, "after": ""}
    result = run_query(query, data_to_get)
    data = result["data"][type]["edges"]
    while result["data"][type]["pageInfo"]["hasNextPage"]:
        print("Fetching the next %i %s" % (BATCH, type))
        data_to_get = {"first": BATCH, "after": result["data"]["posts"]["pageInfo"]["endCursor"]}
        result = run_query(queries.get_posts, data_to_get)
        data += result["data"][type]["edges"]
        
    print("%i %s fetched" % (len(data), type))
    return data
    

def replace_link_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    for before, after in LINKS_TO_REPLACE:
        #regex = re.escape(before) + "(?![/?]photos/)"
        regex = re.escape(before)
        for elem in soup.find_all('a', href=re.compile(r'%s' % regex)):
            elem['href'] = elem['href'].replace(before, after)
        for elem in soup.find_all('img', src=re.compile(r'%s' % regex)):
            elem['src'] = elem['src'].replace(before, after)
    return soup.prettify()

def replace_link_string(content):
    for before, after in LINKS_TO_REPLACE:
        #content = re.sub(re.escape(before) + "(?![/?]photos/)", after, content)
        content = re.sub(re.escape(before), after, content)
    return content

class ToHTML():
    def __init__(self, template, output):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(self.root, 'templates')
        self.env = Environment(loader = FileSystemLoader(self.templates_dir), 
                               trim_blocks = True)
        self.template = self.env.get_template(template)
        self.output = output
        try:
            shutil.rmtree(self.output)
        except FileNotFoundError:
            pass
        os.makedirs(output)
 
    def write(self, variables):
        filename = "%s-%s.html" % (variables["meta"]["date"].split("T")[0],
                                   variables["meta"]["slug"])
        filename = os.path.join(self.output, filename)
        with open(filename, 'w') as fh:
            fh.write(self.template.render(variables=variables))


class Content:
    def __init__(self, type, query, template, output=""):
        self.type = type
        self.template = template
        self.content = []
        self.query = query
        self.root = os.path.dirname(os.path.abspath(__file__))
        if type == "posts":
            if OUTPUT_PATH_POSTS:
                self.output = OUTPUT_PATH_POSTS 
            else:
                self.output = os.path.join(PELICAN_PATH, "content")
        elif type == "pages":
            if OUTPUT_PATH_PAGES:
                self.output = OUTPUT_PATH_PAGES
            else:
                self.output = os.path.join(PELICAN_PATH, "content", "pages")
        
    def clean(self):
        for node in self.content:
            node = node["node"]
            title = node["title"]
            content = node["content"]
            content = replace_link_html(content)
            del node["title"]
            del node["content"]
            
            if self.type == "posts":
                try:
                    node["tags"] = "; ".join([tag["name"] for tag in node["tags"]["nodes"]])
                except:
                    node["tags"] = ""
                try:
                    node["category"] = [tag["name"] for tag in node["categories"]["nodes"]][0]
                    del node["categories"]
                except:
                    node["category"] = ""
            
            yield {"title": title, "content": content, "meta": node}
    
    
    def get_content(self):
        self.content = fetch_data(self.type, self.query)
        tohtml = ToHTML(self.template, self.output)
        
        for content in self.clean():
            tohtml.write(content)
        print("All %s have been written as HTML files" % self.type)


class Menu:
    def __init__(self, name=""):
        self.name = name
        self.id = ""
        self.parsed_menu = []
        
    def get_menu(self):
        print("Fetching menu ID")
        self.get_id()
        print("Fetching menu content")
        self.menu = run_query(queries.get_menu, {"id": self.id})
        self.menu = self.menu["data"]["menu"]["menuItems"]["nodes"]
        self.parsed_menu = self.parse(self.menu)
        return self.parsed_menu
        
    def get_id(self):
        menus_id = run_query(queries.get_menu_id)
        menus_id = menus_id["data"]["menus"]["nodes"]
        for menu in menus_id:
            if menu["name"] == self.name:
                self.id = menu["id"]
        
    def parse(self, to_parse):
        parsed_menu = []
        for entry in to_parse:
            if entry["url"]:
                url = replace_link_string(entry["url"])
                parsed_menu += [(entry["label"], url)]
            elif entry["childItems"]["nodes"]:
                parsed_menu += [(entry["label"], self.parse(entry["childItems"]["nodes"]))]
        return parsed_menu 

    def write_menu(self):
        print("Writing menu to file")
        pelican_menu = "MENUITEMS = " + json.dumps(self.parsed_menu, indent=4)
        with open(os.path.join(PELICAN_PATH, "pelicanvar.py"), "w") as f:
            f.write(pelican_menu) 

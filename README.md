# wp2pelican
This script import data from a running Wordpress blog and create a static website using Pelican. It uses GraphQL API to connect to Wordpress. The aim is to keep Wordpress as backend but provide a static website as frontend.

### What it does
  - Imports posts
  - Imports pages, but only the main ones and not the child pages. As Pelican does not use child pages, I don't see any use in importing them.
  - Import one menu and set it as `MENU_ITEMS` to be used by Pelican (the name of the menu has to be set in `wp2pelicanconf.py`). It automatically imports child menus (usefull for drop-down menus).
  - Replace URLs as set in the conf file.

### Why
  - It uses a conf file written in Python: it is not my first choice, but as Pelican works like this I kept it.

# Documentation
This is not really a documentation per se, but more notes that I use.

### Wordpress and GraphQL
I use [wp-graphql plugin](https://www.wpgraphql.com/) in Worpdress to set up the API. It is pretty straightforward as you only need to install the plugin and you're done, but offer no security whatsoever: everyone can connect to the endpoint and then can send request to read/write. I use a HTTP proxy to mitigate that for now, but I'll have to look into that.

#### Wordpress proxy
If Wordpress (or the GraphQL endpoint) is protected by a HTTP authentification, there are two ways of storing the identifcation: 

  - In `wp2pelicanconf.py` with `HTTP_AUTH = ("id", "password")`
  - Use environment variables `WP_PROXY_ID` and `WP_PROXY_PWD`: this allow to not write the password in a file and can be use with Gitlab CI.
  
### Installation
```
git clone git@github.com:shan-x/wp2pelican.git
cp wp2pelican
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pyhton3 wp2pelican.py
```
  
### Setup Pelican
The output of the script will be in $PELICAN_PATH, where the file `pelicaconf.py` should be located. At the end of this file you have to add:
```
import sys, os
sys.path.append(os.curdir)
from pelicanvar import *
```

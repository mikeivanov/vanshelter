import sys, os

site_packages = "/env/lib/python%s/site-packages" % sys.version[:3]

path = os.path.abspath(os.path.dirname(__file__))
sys.path = [path, 
            path + "/env/lib", 
            path + site_packages] + sys.path

import site
site.addsitedir(path + site_packages)

os.chdir(path)

import bottle, vanshelter

vanshelter.start()
application = bottle.default_app()


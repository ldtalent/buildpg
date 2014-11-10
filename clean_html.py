# to be run from ld (root of root repo)
import os,re

# regular expressions in order:
# 1. \{\%([^%]*?)'((\\'|[^'])*?)'([^%]*?)\%\}
# 2. \{\%([^%]*?)"((\\"|[^"])*?)"([^%]*?)\%\}
# 3. \{\%([^%]+)\%\}
# 4. \{\{([^\}]+)\}\}

#print 'here in clean_html'

# clean html
for fn in os.listdir('ldmobile/www'):
    fileName, fileExtension = os.path.splitext(fn)
    #print fn, fileName, fileExtension
    if fileExtension == '.html':
        #print fn
        f = open('ldmobile/www/' + fn, 'r')
        content = f.read()
        #print '-------content-------'
        #print content
        print 'cleaning ' + fn
        cleaned = re.sub(r"\{\%([^%]*?)'((\\'|[^'])*?)'([^%]*?)\%\}", "", content)
        cleaned = re.sub(r'\{\%([^%]*?)"((\\"|[^"])*?)"([^%]*?)\%\}', '', cleaned)
        cleaned = re.sub(r'\{\%([^%]+)\%\}', '', cleaned)
        cleaned = re.sub(r'\{\{([^\}]+)\}\}', '', cleaned)
        # make static imports relative
        cleaned = cleaned.replace('src="/static', 'src="static') # jade always compiles to no spaces and double quotes
        cleaned = cleaned.replace('href="/static', 'href="static')
        #print '-------cleaned-------'
        #print cleaned
        f = open('ldmobile/www/' + fn, 'w')
        f.write(cleaned)

# clean compiled partials
for fn in os.listdir('ldmobile/www/static/compiled-partials'):
    fileName, fileExtension = os.path.splitext(fn)
    #print fn, fileName, fileExtension
    if fileExtension == '.html':
        #print fn
        f = open('ldmobile/www/static/compiled-partials/' + fn, 'r')
        content = f.read()
        #print '-------content-------'
        #print content
        print 'cleaning ' + fn
        cleaned = re.sub(r"\{\%([^%]*?)'((\\'|[^'])*?)'([^%]*?)\%\}", "", content)
        cleaned = re.sub(r'\{\%([^%]*?)"((\\"|[^"])*?)"([^%]*?)\%\}', '', cleaned)
        cleaned = re.sub(r'\{\%([^%]+)\%\}', '', cleaned)
        cleaned = re.sub(r'\{\{([^\}]+)\}\}', '', cleaned)
        # make static imports relative
        cleaned = cleaned.replace('src="/static', 'src="static') # jade always compiles to no spaces and double quotes
        cleaned = cleaned.replace('href="/static', 'href="static')
        #print '-------cleaned-------'
        #print cleaned
        f = open('ldmobile/www/static/compiled-partials/' + fn, 'w')
        f.write(cleaned)

# make static gets relative for js requests
for fn in os.listdir('ldmobile/www/static/js'):
    print 'cleaning ' + fn
    f = open('ldmobile/www/static/js/' + fn, 'r')
    content = f.read()
    cleaned = content.replace('$.get', 'pgget')
    f = open('ldmobile/www/static/js/' + fn, 'w')
    f.write(cleaned)

# make static urls relative for css, note: css url includes are relative to the css file itself
for fn in os.listdir('ldmobile/www/static/css'):
    print 'cleaning ' + fn
    f = open('ldmobile/www/static/css/' + fn, 'r')
    content = f.read()
    cleaned = content.replace('url("/static', 'url("..')
    cleaned = cleaned.replace("url('/static", "url('..")
    f = open('ldmobile/www/static/css/' + fn, 'w')
    f.write(cleaned)

# build phonegap index.html
f = open('ldmobile/www/head.html')
head = '<head>' + f.read() + '<style>.ui-btn.ui-btn-active:hover { background-color: #3388cc !important; } .ui-btn:hover {background-color: #f6f6f6 !important;}</style></head>' # mobile fix for jqm hovers
# use local versions of jquery and jquerymobile
head = re.sub(r'src="(.*?)jquery.min.js"', 'src="static/js/jquery.min.js"', head)
head = re.sub(r'src="(.*?)jquery.mobile.min.js"', 'src="static/js/jquery.mobile.min.js"', head)
#print head
body = '<body><span id="fastclick"><div class="app"><div id="deviceready" class="blink"><div data-role="page" ldid="startPage"><script type="text/javascript" src="cordova.js"></script><script type="text/javascript" src="js/index.js"></script><script type="text/javascript">app.initialize();</script></div></div></div><div id="page_specific_files"></div></span></body>'
html = '<html>' + head + body + '</html>'
f = open('ldmobile/www/index.html', 'w')
f.write(html)

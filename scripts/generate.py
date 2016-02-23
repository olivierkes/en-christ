#!/usr/bin/env python
# --!-- coding: utf8 --!--

from string import Template
import re
import random
import time

# Templates
#------------------------
# base.tpl:
# - PAGE_TITLE
# - BREADCRUMB
# - MENU_TITLE
# - MENU
# - PAGE_CONTENT
# - VERSION
# - COPYRIGHT
#
# column.tpl
# - COLUMN_LEFT
# - COLUMN_RIGHT
#
# circle.tpl
# - TIME
#
# more-infos.tpl
# - TITLE
# - CONTENT
# - ID


VERSION = '<a href="https://github.com/olivierkes/en-christ">0.1 - {}</a> '.format(time.strftime("%d/%m/%Y"))
MENU_TITLE = "En Christ"
COPYRIGHT = "Copyleft (CC-BY-SA) - <a href='http://www.theologeek.ch'>Olivier Keshavjee</a>"
PAGE_TITLE = "De l'identité en crise à l'identité en Christ"
GOOGLE_ANALYTICS_ID = "UA-35562063-1"

templates = {
    "Base":   "templates/base.tpl",
    "Column": "templates/column.tpl",
    "Circle": "templates/circle.tpl",
    "MoreInfos": "templates/more-infos.tpl",
    "Card":     "templates/card.tpl",
    "Thumbnail":    "templates/thumbnail.tpl",
    "GA":       "templates/google-analytics.tpl",
}


class page:
    def __init__(self, title=None, subtitle=None, html=None, slug=None, icon_class=None, icon_title=None):
        self.title = title
        self.subtitle = subtitle
        self.html = html
        self.slug = slug
        self.icon_class = icon_class
        self.icon_title = icon_title

def load_file(f):
    with open(f, "r") as of:
        return of.read()
    
def write_file(f, content):
    with open(f, "w") as of:
        of.write(content)


# Generate menu
def generate_main_menu(pages, current_page, custom_class=""):
    menu = ""
    tpl = """
    <li class="{CLASS}">
        <a href="{SLUG}">
            <span class="icon {ICON_CLASS}">{ICON_TITLE}</span>
            <span class="title">{TITLE}</span>
        </a>
        <span class="badge">{SUBTITLE}</span>
    </li>"""
    for p in pages:
        menu += tpl.format(
            CLASS = ("active" if p == current_page else "") + " " + custom_class,
            SLUG = p.slug,
            TITLE = p.title,
            SUBTITLE = p.subtitle,
            ICON_CLASS = p.icon_class,
            ICON_TITLE = p.icon_title,
            )
    return menu

# Feed
def get_feed(url):
    import feedparser
    import time
    d = feedparser.parse(url)
    r = '<ul class="list-group">'
    i = 0
    for e in reversed(d.entries):
        i += 1
        r += '''<li class="list-group-item">
                    <a href="{URL}" target="_blank">
                        <span class="icon fa fa-play">{n}</span>
                        <span class="title">{TITLE}</span>
                    </a>
                    <span class="badge">{DATE}</span>
                </li>'''.format(
            n = "", #str(i),
            URL = e.link,
            TITLE = e.title,
            DATE = time.strftime('%Y-%m-%d', e.published_parsed)
            
            #"{Y}-{M}-{D}".format(
                #Y=e.published_parsed[
        )
    r += "</ul>"
    return r

def custom_formats(html):
    #return html
    
    patterns = []
    
    # Removes <p></p> around custom tags ([...])
    patterns.append(
        ("<[pP]>\n(\[[^\n]*?\])\n</[pP]>", "\\1")
    )
    
    # Cards (with H2 tags)
    #patterns += [
        #("<H2>(.*?)</H2>(.*?)(?=<H2>|$)",
         #templates["Card"].substitute(
             #TITLE="\\1",
             #BODY="\\2",
             #CARD_CLASS="",
             #HIDDEN="",
             #) + "\n<p></p>\n"
        #),
    #]
    
    # Cards
    patterns.append(
        ("\[card:?([\w\-_]*?|)\](?:\s*?<H3>(.*?|)</H3>|)(.*?)\[\/card]",
         lambda t: templates["Card"].substitute(
            TITLE=t.group(2) if t.group(2) else "",
            BODY=t.group(3),
            SUBHEAD = '<span class="subhead">{}</span>'.format({
                "info": "Information",
                "do": "Pratique",
                "discussion": "Discussion",
                "prayer": "Prière",
                "next-time": "Prochaine fois"}[t.group(1)]) if t.group(1) in [
                    "do", "discussion", "prayer", "next-time"] else "",
            HIDDEN = "hidden" if not t.group(2) else "",
            CARD_CLASS = {
                "info": "",
                "do": "color-left green",
                "discussion": "color-left blue",
                "prayer": "color-left yellow",
                "next-time": "light blue",
                "":""}[t.group(1)]
            )+"<p></p>"
        )
    )
    
    # Titles
    patterns += [
        ("<H3>(.*?)</H3>",
         '<div class="sub-title"><span>\\1</span></div>'
        ),
        ("<H5>(.*?)</H5>",
         '<span class="subhead">\\1</span>'
        ),
    ]    
    
    # Others
    patterns += [
        # More infos
         ("\[\+,*\s*(.*?)\]" + \
          "(.*?)" + \
          "\[/\+\]",
         lambda t: templates["MoreInfos"].substitute(
             TITLE=t.group(1),
             CONTENT=t.group(2),
             ID="mi-{}".format(random.randint(0,999999999)))
        ),
        
        # Menu
        ("\[tpl:menu\]",
        '<ul class="list-group">{}</ul>'.format(generate_main_menu(pages, None, custom_class="list-group-item"))
        ),
        
        # Feed
        ("\[feed:(https?://[\da-z\.-]+\.[a-z\.]{2,6}(?:[\/\w\.-]*?)*?\/?)\]",
        lambda m: get_feed(m.group(1))
        ),
        
        # Thumbnail
        ("\[img:([\w\d\./\-_]*?)\](.*?)\[\/img]",
         lambda t: templates["Thumbnail"].substitute(
            SRC=t.group(1),
            CAPTION=t.group(2)
            )+"<p></p>"
        ),
        
        # Grid
        ("\[row\](.*?)\[/row\]", '<div class="row">\\1</div>'),
        ("\[col:(\d+)\](.*?)\[/col\]", '<div class="no-margin-bottom col-xs-\\1">\\2</div>'),
        ("\[col:(\d+),\s*(\d+)\](.*?)\[/col\]", '<div class="no-margin-bottom col-xs-\\1 col-sm-\\2">\\3</div>'),
        ("\[col:(\d+),\s*(\d+),\s*(\d+)\](.*?)\[/col\]", '<div class="no-margin-bottom col-xs-\\1 col-sm-\\2 col-md-\\3">\\4</div>'),
        
        
    ]
    for p,sub in patterns:
        #while html != re.sub(p, sub, html, flags=re.DOTALL):
        html = re.sub(p, sub, html, flags=re.DOTALL)
    
    return html
    #html = re.sub(pattern, repl, string)
    
# Loading template
for t in templates:
    print("Loading template '{}' ({}): ".format(t, templates[t]), end="")
    templates[t] = Template(load_file(templates[t]))
    print(" OK")

print("Loading TOC (src/TOC.csv): ", end="")
TOC = load_file("src/TOC.csv").split("\n")
TOC = [[i.strip() for i in t.split(",")] for t in TOC if t][1:]
#TOC = [t.strip() for t in TOC if t]
print(" OK")

pages = []

for entry in TOC:
    f = entry[0]
    print("Loading page '{}': ".format(f), end="")
    header = load_file("src/{}.t2t".format(f)).split("\n")[0:3]
    p = page(
        title = header[0],
        subtitle = header[1],
        html = load_file("src/{}.html".format(f)),
        slug = "{}.html".format(f),
        icon_class = entry[1],
        icon_title = entry[2]
        )
    pages.append(p)
    print(" OK")
    
for p in pages:
    print("Custom formatting page '{}': ".format(p.title), end="")
    p.html = custom_formats(p.html)
    print(" OK")

# Generate and write pages
for p in pages:
    c = templates["Base"].substitute(
        PAGE_TITLE = PAGE_TITLE,
        BREADCRUMB = "{} <span class='subtitle'>({})</span>".format(p.title, p.subtitle) if p.subtitle else p.title,
        MENU_TITLE = MENU_TITLE,
        COPYRIGHT = COPYRIGHT,
        VERSION = VERSION,
        GOOGLE_ANALYTICS_ID = templates["GA"].substitute(
            ID = GOOGLE_ANALYTICS_ID
            ) if GOOGLE_ANALYTICS_ID else "",
        MENU = generate_main_menu(pages, p),
        PAGE_CONTENT = p.html)
    write_file("www/{}".format(p.slug), c)


# s = Template('$who likes $what')
# s.substitute(who='tim', what='kung pao')
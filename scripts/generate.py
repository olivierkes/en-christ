#!/usr/bin/env python
# --!-- coding: utf8 --!--

from string import Template
import re
import random

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


VERSION = "0.1"
MENU_TITLE = "En Christ"
COPYRIGHT = "Copyleft (CC-BY-SA)"
PAGE_TITLE = "De l'identité en crise à l'identité en Christ"

templates = {
    "Base":   "templates/base.tpl",
    "Column": "templates/column.tpl",
    "Circle": "templates/circle.tpl",
    "MoreInfos": "templates/more-infos.tpl",
    "Card":     "templates/card.tpl",
}


class page:
    def __init__(self, title=None, html=None, slug=None, icon_class=None, icon_title=None):
        self.title = title
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
            <span class="icon {ICON_CLASS}">{ICON_TITLE}</span><span class="title">{TITLE}</span>
        </a>
    </li>"""
    for p in pages:
        menu += tpl.format(
            CLASS = ("active" if p == current_page else "") + " " + custom_class,
            SLUG = p.slug,
            TITLE = p.title,
            ICON_CLASS = p.icon_class,
            ICON_TITLE = p.icon_title
            )
    return menu

def generate_menu(pages):
    menu = ""
    tpl = '<li class="list-group-item">{TITLE}</li>'
    
    for p in pages:
        menu += tpl.format(TITLE=p.title)
    
    return '<ul class="list-group">{}</ul>'.format(menu)

def custom_formats(html):
    #return html
    
    patterns = []
    
    # Removes <p></p> around custom tags ([...])
    patterns.append(
        ("<[pP]>\n(\[[^\n]*?\])\n</[pP]>", "\\1")
    )
    
    # Cards (with H2 tags)
    patterns += [
        ("<H2>(.*?)</H2>(.*?)(?=<H2>)",
         templates["Card"].substitute(
             TITLE="\\1",
             BODY="\\2",
             ) + "\n<p></p>\n"
        ),
        ("<H2>(.*?)</H2>(.*?)$",
         templates["Card"].substitute(
             TITLE="\\1",
             BODY="\\2",
             ) + "\n<p></p>"
        ),
        ("<H3>(.*?)</H3>",
         '<div class="sub-title"><span>\\1</span></div>'
        ),
    ]
    
    # Circles
    circles = [
        ("info", "fa-info", "blue", "Information"),
        ("do", "fa-wrench", "green", "Mise en pratique"),
        ("discussion", "fa-comments", "yellow", "Discussion"),
    ]
    
    for c in circles:
        patterns.append(
            ("\[row:{}\]".format(c[0]),
             "[row/]"+templates["Circle"].substitute(
                ICON=c[1],
                COLOR=c[2],
                TYPE=c[3]
                )+"[/row/]"
            )
        )
        
    
    patterns += [
        # Close row
        ("\[row/\](.*?)\[/row/\](.*?)\[\/row]",
         templates["Column"].substitute(
            CONTENT_LEFT="\\1",
            CONTENT_RIGHT="\\2"
            )
         ),
         # More infos
         ("\[\+,*\s*(.*?)\]" + \
          "(.*?)" + \
          "\[/\+\]",
         lambda t: templates["MoreInfos"].substitute(
             TITLE=t.group(1),
             CONTENT=t.group(2),
             ID="mi-{}".format(random.randint(0,999999999)))
        ),
         
        ("\[tpl:menu\]",
        '<ul class="list-group">{}</ul>'.format(generate_main_menu(pages, None, custom_class="list-group-item"))
        ),
        
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
    p = page(
        title = load_file("src/{}.t2t".format(f)).split("\n")[0],
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
        BREADCRUMB = p.title,
        MENU_TITLE = MENU_TITLE,
        COPYRIGHT = COPYRIGHT,
        VERSION = VERSION,
        MENU = generate_main_menu(pages, p),
        PAGE_CONTENT = p.html)
    write_file("www/{}".format(p.slug), c)


# s = Template('$who likes $what')
# s.substitute(who='tim', what='kung pao')
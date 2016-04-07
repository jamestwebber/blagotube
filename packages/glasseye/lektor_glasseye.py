# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor.types import Type

import pypandoc as py
from bs4 import BeautifulSoup


def glasseye_to_html(text):
    # Function to wrap with tags
    def wrap(to_wrap, wrap_in):
        contents = to_wrap.replace_with(wrap_in)
        wrap_in.append(contents)

#     # Function to add charts
#     def add_chart(chart_id, code_string):
#         for d in enumerate(soup.findAll(chart_id)):
#             code_string += chart_id + "(" + str(d[1].contents[0]) + ", '#" + chart_id + "_" + str(d[0])
#             if d[1].parent.name == "span":
#                 code_string += "', 'margin'); \n"
#             else:
#                 code_string += "', 'full_page'); \n"
#             d[1].name = "span"
#             d[1].contents = ""
#             d[1]['id'] = chart_id + "_" + str(d[0])
#             tag = soup.new_tag("br")
#             d[1].insert_after(tag)
#         return code_string

    # Get paths and file names
#     user_path = os.getcwd() + "/"
#     input_file = sys.argv[1]
#     glasseye_path = os.path.dirname(os.path.abspath(__file__)) + "/"
#     stem = os.path.splitext(input_file)[0]
#     glasseye_file = stem + ".html"

#    tufte_template = "templates/tufteTemplate.html"

    # Convert markdown to html using pandoc
    converted_html = py.convert(text, 'html', format='md', extra_args=['--mathjax'])

    # soupify it
    soup = BeautifulSoup(converted_html, 'html.parser')

    # Make the changes for the Tufte format

    # marginnotes
    # <label for="mn-demo" class="margin-toggle">&#8853;</label>
    # <input type="checkbox" id="mn-demo" class="margin-toggle"/>
    # <span class="marginnote">
    #   This is a margin note. Notice there isn’t a number preceding the note.
    # </span>

    for i,a in enumerate(soup.findAll('marginnote')):
        lbl = soup.new_tag("label")
        lbl['for'] = "mn-{}".format(i)
        lbl['class'] = "margin-toggle"
        lbl.string = u"⊕"

        chkbox = soup.new_tag("input")
        chkbox['type'] = "checkbox"
        chkbox['id'] = "mn-{}".format(i)
        chkbox['class'] = "margin-toggle"

        a.insert_before(lbl)
        a.insert_before(chkbox)

        a.name = "span"
        a['class'] = "marginnote"

    # sidenotes:
    # <label for="sn-demo" class="margin-toggle sidenote-number"></label>
    # <input type="checkbox" id="sn-demo" class="margin-toggle"/>
    # <span class="sidenote">
    #   This is a sidenote.
    # </span>

    for i,a in enumerate(soup.findAll('sidenote')):
        lbl = soup.new_tag("label")
        lbl['for'] = "sn-{}".format(i)
        lbl['class'] = "margin-toggle sidenote-number"

        chkbox = soup.new_tag("input")
        chkbox['type'] = "checkbox"
        chkbox['id'] = "sn-{}".format(i)
        chkbox['class'] = "margin-toggle"

        a.insert_before(lbl)
        a.insert_before(chkbox)

        a.name = "span"
        a['class'] = "sidenote"

    for a in soup.findAll('checklist'):
        l = a.parent.findNext('ul')
        l['class'] = "checklist"
        a.extract()

    if soup.ol is not None:
        for ol in soup.findAll('ol'):
            if ol.parent.name != 'li':
                wrap(ol, soup.new_tag("div", **{'class': 'list-container'}))

    if soup.ul is not None:
        for ul in soup.findAll('ul'):
            if ul.parent.name != 'li':
                wrap(ul, soup.new_tag("div", **{'class': 'list-container'}))


#     #Process the charts
#     code_string = ""
#
#     #Standard charts
#
#     standard_charts = ["simplot", "treemap", "dot_plot", "gantt", "donut", "barchart", "tree", "force", "venn", "scatterplot", "timeseries"]
#
#     for s in standard_charts:
#         code_string = add_chart(s, code_string)
#
#     #Charts with extra features (will modify the standard charts asap)
#
#     for d in enumerate(soup.findAll('lineplot')):
#         if d[1].parent.name == "span":
#             size = "margin"
#         else:
#             size = "full_page"
#         arguments = str(d[1].contents[0])
#         if "," in arguments and ".csv" in arguments:
#             arguments = arguments.split(",", 1)
#             code_string += "lineplot(" + arguments[0] + ", " + "'#lineplot_" + str(d[0]) + "','" + size + "'," + arguments[1] + "); \n"
#         else:
#             code_string += "lineplot(" + str(d[1].contents[0]) + ", " + "'#lineplot_" + str(d[0]) + "','" + size + "'); \n"
#         d[1].name = "span"
#         d[1].contents = ""
#         d[1]['id'] = "lineplot_" + str(d[0])
#         tag = soup.new_tag("br")
#         d[1].insert_after(tag)

    return unicode(soup)


# Wrapper with an __html__ method prevents
# Lektor from escaping HTML tags.
class HTML(object):
    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html


class GlasseyeDocType(Type):
    widget = 'multiline-text'

    def value_from_raw(self, raw):
        return HTML(glasseye_to_html(raw.value or u''))


class GlasseyePlugin(Plugin):
    name = u'Glasseye'
    description = u'Adds modified Glasseye field type to Lektor.'

    def on_setup_env(self, **extra):
        # Derives type name "Glasseye" from class name.
        self.env.types[self.name] = GlasseyeDocType

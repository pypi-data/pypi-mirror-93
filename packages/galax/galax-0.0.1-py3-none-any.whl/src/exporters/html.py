"""
Copyright 2021 Michael Anckaert

This file is part of Galax.

Galax is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Galax is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Galax.  If not, see <https://www.gnu.org/licenses/>.
"""

import markdown
from jinja2 import Environment, FileSystemLoader


def generate_article_list(link_map):
    loader = FileSystemLoader('templates/html')
    env = Environment(loader=loader)
    template = env.get_template('blog.html')
    return template.render(posts=link_map)


def generate_html_for_source(contents):
    return markdown.markdown(contents)


def save_article_index(link_map):
    html = generate_article_list(link_map)
    with open('output/html/blog.html', 'w') as f:
        f.write(html)


def save_contents(link_map):
    for link in link_map:
        html_content = generate_html_for_source(link['contents'])
        filename = f"output/html/{link['url']}.html"
        with open(filename, 'w') as f:
            f.write(html_content)


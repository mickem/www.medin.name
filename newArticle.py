#!/usr/bin/env python
# encoding: utf-8

import os
import datetime
import subprocess

from pelican.utils import slugify

DEFAULT_CATEGORY = "monitoring"
DATE_FORMAT = "%Y-%m-%d"
BASE_ARTICLE_DIR = os.path.join("content", "blog")

ARTICLE_TEMPLATE = """\
Title: {}
Authors: Michael Medin
Date: {}
Catgory: {}

"""

EDITOR = "notepad {}"

def get_data_from_user():
    print("##########################")
    print("# Creating a new Article #")
    print("##########################")

    title = raw_input("Title []: ")

    default_slug = slugify(title)
    custom_slug = raw_input("Slug [{}]: ".format(default_slug))
    slug = custom_slug if custom_slug else default_slug

    custom_category = raw_input("Category [{}]: ".format(DEFAULT_CATEGORY))
    category = custom_category if custom_category else DEFAULT_CATEGORY

    today = datetime.date.today()
    custom_creation_date = raw_input("Date [{}]: ".format(today.strftime(DATE_FORMAT)))

    if custom_creation_date:
        custom_creation_date = datetime.datetime.strptime(custom_creation_date, DATE_FORMAT)

    creation_date = custom_creation_date if custom_creation_date else today

    return (title, slug, category, creation_date)


def create_article_file(title, slug, category, creation_date):
    date_path = creation_date.strftime(DATE_FORMAT)

    article_dir = os.path.join(BASE_ARTICLE_DIR, category.lower(), date_path, slug)
    os.makedirs(article_dir)

    article_file_path = os.path.join(article_dir, "post.md")

    with open(article_file_path, "w") as article_file:
        article_file.write(ARTICLE_TEMPLATE.format(title, creation_date, category))

    subprocess.call(EDITOR.format(article_file_path), shell=True)


if __name__ == "__main__":
    create_article_file(*get_data_from_user())


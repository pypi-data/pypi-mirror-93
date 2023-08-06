# -*- coding: utf-8 -*-
#
# This file is part of hepcrawl.
# Copyright (C) 2017, 2019 CERN.
#
# hepcrawl is a free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

from __future__ import absolute_import, division, print_function

from scrapyd_api import ScrapydAPI


def get_crawler_instance(crawler_host, *args, **kwargs):
    """Get current crawler instance.

    Args:
        crawler_host(str): the crawler's host name.

    Returns:
        ScrapydAPI: current crawler instance.
    """
    return ScrapydAPI(
        crawler_host,
        *args,
        **kwargs
    )


def deep_sort(element):
    """Dummy deep-sort json dicts (lists, dicts, strings, bools and integers)."""
    if isinstance(element, dict):
        for key, value in element.items():
            element[key] = deep_sort(value)
        return element

    if isinstance(element, list):
        return sorted([deep_sort(item) for item in element])

    return element


def sort_list_of_records_by_record_title(list_to_sort):
    """Sort list of records by record title"""
    return sorted(list_to_sort, key=lambda k: k['titles'][0]['title'])

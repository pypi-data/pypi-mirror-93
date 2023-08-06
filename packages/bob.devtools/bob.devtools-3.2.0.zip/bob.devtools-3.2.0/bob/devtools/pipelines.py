#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pipeline utilities"""

import re

from datetime import datetime

from tabulate import tabulate


def process_log(log):
    """
    Summarizes the execution time of a pipeline given its Job log
    """

    current_package = None
    logs = dict()
    dates = []
    for ll in log:

        # Check which package are we
        if len(re.findall("Building bob/[a-z]*", ll)) > 0:
            logs[current_package] = dates
            dates = []

            current_package = ll[9:-1]
            continue

        # Checking the date
        date = re.findall(
            "[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2} [0-9]{2,2}:[0-9]{2,2}:[0-9]{2,2}", ll
        )
        if len(date) > 0:
            # logs[date[0]]=current_package
            dates.append(date[0])

    # Last log
    if len(dates) > 0:
        logs[current_package] = dates

    table = []
    for k in logs:
        first = datetime.strptime(logs[k][0], "%Y-%m-%d %H:%M:%S")
        last = datetime.strptime(logs[k][-1], "%Y-%m-%d %H:%M:%S")
        delta = ((last - first).seconds) / 60

        table.append([str(k), str(first), str(round(delta, 2)) + "m"])

    print(tabulate(table))

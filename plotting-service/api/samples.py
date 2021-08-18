import logging
import utils

import cachedb

from pyincore.models.fragilitycurveset import FragilityCurveSet
from pyincore.models.fragilitycurverefactored import FragilityCurveRefactored

import json
import traceback
import sys


def format_xy_set(xy_set):
    # hichart format
    new_format = {}
    for xy_key in xy_set.keys():
        xy = xy_set[xy_key]
        xy_list = []
        for i in range(len(xy['x'])):
            xy_list.append([xy['x'][i], xy['y'][i]])
        new_format[xy_key] = xy_list

    return new_format


def get_xy_set(fragility_set, sample_size, refresh):

    #check the database first
    xy_set = None
    if refresh is False:
        xy_set = cachedb.check_cache(fragility_set, sample_size)

    #if there is a match, return the xy_set
    if xy_set is not None:
        return xy_set

    #if there is no match, compute xy_set
    if isinstance(fragility_set.fragility_curves[0], FragilityCurveRefactored):
        xy_set = utils.get_refactored_xy_fragility_set(fragility_set, sample_size=sample_size)
    else:
        xy_set = utils.get_xy_old_fragility_set(fragility_set, sample_size=sample_size)    

    # store the xy_set to cache DB
    cachedb.store_cache(fragility_set, sample_size, xy_set)

    return xy_set


# POST method for samples/{fraglity_set_id}
def post(body, sample_size, refresh):
    try:
        # create fragility_set object from the body of request
        fragility_set_json = json.loads(body)
        fragility_set = FragilityCurveSet(fragility_set_json)

        xy_set = get_xy_set(fragility_set, sample_size=sample_size, refresh=refresh)

        return format_xy_set(xy_set), 200

    except Exception:
        return traceback.format_exc(), 500

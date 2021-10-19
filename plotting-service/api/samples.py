import logging
import utils

import cachedb

from pyincore.models.fragilitycurveset import FragilityCurveSet

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

def format_xyz_set(xyz_set):
    new_format = {}
    for xyz_key in xyz_set.keys():
        xyz = xyz_set[xyz_key]
        xyz_list = []
        for i in range(len(xyz['x'])):
            xyz_list.append([xyz['x'][i], xyz['y'][i], xyz['z'][i]])
        new_format[xyz_key] = xyz_list

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
    xy_set = utils.get_refactored_xy_fragility_set(fragility_set, sample_size=sample_size)

    # store the xy_set to cache DB
    cachedb.store_cache(fragility_set, sample_size, xy_set)

    return xy_set


def get_xyz_set(fragility_set, sample_interval, refresh):
    xyz_set = None
    if refresh is False:
        xyz_set = cachedb.check_cache(fragility_set, sample_interval)

    # if there is a match, return the xyz_set
    if xyz_set is not None:
        return xyz_set

    # if there is no match, compute xyz_set
    xyz_set = utils.get_refactored_xyz_fragility_set(fragility_set, sample_interval=sample_interval)

    # store the xyz_set to cache DB
    cachedb.store_cache(fragility_set, sample_interval, xyz_set)

    return xyz_set


# POST method for samples/{fraglity_set_id}
def post(body, sample_size, sample_interval, refresh):
    try:
        # create fragility_set object from the body of request
        fragility_set_json = json.loads(body)
        fragility_set = FragilityCurveSet(fragility_set_json)

        # check if it's 2d or 3d
        if len(fragility_set.demand_types) == 1:
            xy_set = get_xy_set(fragility_set, sample_size=sample_size, refresh=refresh)
            return format_xy_set(xy_set), 200

        elif len(fragility_set.demand_types) > 1:
            # there is only sample interval that default to 0.5 right now
            xyz_set = get_xyz_set(fragility_set, sample_interval=sample_interval, refresh=refresh)
            return format_xyz_set(xyz_set), 200


    except Exception:
        return traceback.format_exc(), 500

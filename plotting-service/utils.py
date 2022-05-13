import numpy as np
from pyincore_viz.plotutil import PlotUtil

import config


def get_refactored_xy_fragility_set(fragility_set, custom_curve_parameters={}, sample_size: int = 200):
    demand_type_names = []
    for parameter in fragility_set.curve_parameters:
        # for hazard
        if parameter.get("name") in fragility_set.demand_types:
            demand_type_names.append(parameter["name"])
        elif parameter.get("fullName") in fragility_set.demand_types:
            demand_type_names.append(parameter["fullName"])
        # check the rest of the parameters see if default or custom value has passed in
        else:
            if parameter.get("expression") is None and parameter.get("name") not in \
                    custom_curve_parameters:
                raise ValueError("The required parameter: " + parameter.get("name")
                                 + " does not have a default or custom value. Please check "
                                   "your fragility curve setting. Alternatively, you can include it in the "
                                   "custom_curve_parameters variable and passed it in this method. ")

    xy_set = {}

    start, end = get_start_end(fragility_set.hazard_type, demand_type_names[0])
    # print(start, end, sample_size)

    for curve in fragility_set.fragility_curves:
        x, y = PlotUtil.get_x_y(curve, demand_type_names[0],
                                fragility_set.curve_parameters,
                                custom_curve_parameters, start=start, end=end,
                                sample_size=sample_size)
        key = curve.return_type['description']
        xy_set[key] = {'x': _ndarray_to_list(x), 'y': _ndarray_to_list(y)}

    return xy_set


def get_refactored_xyz_fragility_set(fragility_set, custom_curve_parameters={}, sample_interval: int = 0.5):
    demand_type_names = []
    for parameter in fragility_set.curve_parameters:
        # for hazard
        if parameter.get("name") in fragility_set.demand_types:
            demand_type_names.append(parameter["name"])
        elif parameter.get("fullName") in fragility_set.demand_types:
            demand_type_names.append(parameter["fullName"])
        # check the rest of the parameters see if default or custom value has passed in
        else:
            if parameter.get("expression") is None and parameter.get("name") not in \
                    custom_curve_parameters:
                raise ValueError("The required parameter: " + parameter.get("name")
                                 + " does not have a default or  custom value. Please check "
                                   "your fragility curve setting. Alternatively, you can include it in the "
                                   "custom_curve_parameters variable and passed it in this method. ")

    xyz_set = {}
    start, end = get_start_end(fragility_set.hazard_type, demand_type_names[0])

    for curve in fragility_set.fragility_curves:
        X, Y, Z = PlotUtil.get_x_y_z(curve,
                                     demand_type_names[:2],
                                     fragility_set.curve_parameters,
                                     custom_curve_parameters, start=start, end=end,
                                     sample_size=sample_interval)
        result = np.vstack([X.ravel(), Y.ravel(), Z.ravel()])
        key = curve.return_type['description']
        xyz_set[key] = {'x': _ndarray_to_list(result[0]), 'y': _ndarray_to_list(result[1]), 'z': _ndarray_to_list(
            result[2])}

    return xyz_set


def get_start_end(hazard, demand_type):
    key = hazard.lower() + "-" + demand_type.lower()
    range = config.RANGE.get(key, config.RANGE["default"])

    return (range['start'], range['end'])


def _ndarray_to_list(numpy_ndarray):
    if isinstance(numpy_ndarray, np.ndarray):
        result = numpy_ndarray.tolist()
    else:
        result = numpy_ndarray

    return result

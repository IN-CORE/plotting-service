import math
import numpy as np

import config

from pyincore_viz.plotutil import PlotUtil
from pyincore import StandardFragilityCurve, PeriodStandardFragilityCurve, PeriodBuildingFragilityCurve, \
    ConditionalStandardFragilityCurve, ParametricFragilityCurve, CustomExpressionFragilityCurve


def get_xy_old_fragility_set(fragility_set, sample_size: int = 200):
    xy_set = {}

    # getting the start and end value assuming that there is 1 demand type in fragilty curve set
    start, end = get_start_end(fragility_set.hazard_type, fragility_set.demand_types[0])
    for curve in fragility_set.fragility_curves:
        if isinstance(curve, CustomExpressionFragilityCurve):
            if curve.expression.find('x') >= 0 and curve.expression.find('y') < 0:
                x, y = PlotUtil.get_custom_x_y(curve.expression, start=start, end=end, sample_size=sample_size)
            else:
                raise ValueError("We are only able to plot 2d fragility curve with x as variable name for now. "
                                 "More implementation coming soon...")

        elif isinstance(curve, StandardFragilityCurve) or isinstance(curve, PeriodStandardFragilityCurve):
            if curve.alpha_type == 'lambda':
                alpha = curve.alpha
            elif curve.alpha_type == 'median':
                alpha = math.log(curve.alpha)
            else:
                raise ValueError("The alpha type is not implemented")
            # get_standard_x_y needs "sample size" as a argument
            x, y = PlotUtil.get_standard_x_y(curve.curve_type, alpha, curve.beta)


        elif isinstance(curve, ConditionalStandardFragilityCurve):
            x, y = PlotUtil.get_conditional_x_y(
                curve.rules, curve.alpha_type, curve.alpha, curve.beta, start=start, end=end, sample_size=sample_size)

        elif isinstance(curve, ParametricFragilityCurve):
            x, y = PlotUtil.get_parametric_x_y(
                curve.curve_type, curve.parameters)

        elif isinstance(curve, PeriodBuildingFragilityCurve):
            x, y = PlotUtil.get_period_building_x_y(curve.fs_param0, curve.fs_param1, curve.fs_param2,
                                                    curve.fs_param3, curve.fs_param4, curve.fs_param5, start=start, end=end, sample_size=sample_size)
        else:
            raise ValueError(
                "This type of fragility curve is not implemented!")

        if isinstance(x, np.ndarray):
            new_x = x.tolist()
        else:
            new_x = x
        
        if isinstance(y, np.ndarray):
            new_y = y.tolist()
        else:
            new_y = y

        xy_set[curve.description] = {'x': new_x, 'y': new_y}

    return xy_set


def get_refactored_xy_fragility_set(fragility_set, custom_fragility_curve_parameters={}, sample_size: int = 200):
    demand_type_names = []
    for parameter in fragility_set.fragility_curve_parameters:
        # for hazard
        if parameter.get("name") in fragility_set.demand_types:
            demand_type_names.append(parameter["name"])
        elif parameter.get("fullName") in fragility_set.demand_types:
            demand_type_names.append(parameter["fullName"])
        # check the rest of the parameters see if default or custom value has passed in
        else:
            if parameter.get("expression") is None and parameter.get("name") not in \
                    custom_fragility_curve_parameters:
                raise ValueError("The required parameter: " + parameter.get("name")
                                 + " does not have a default or custom value. Please check "
                                 "your fragility curve setting. Alternatively, you can include it in the "
                                 "custom_fragility_curve_parameters variable and passed it in this method. ")

    xy_set = {}

    start, end = get_start_end(fragility_set.hazard_type, demand_type_names[0])
    print(start, end, sample_size)

    for curve in fragility_set.fragility_curves:

        x, y = PlotUtil.get_refactored_x_y(curve, demand_type_names[0],
                                           fragility_set.fragility_curve_parameters,
                                           custom_fragility_curve_parameters,start=start, end=end, sample_size=sample_size)
        key = curve.return_type['description']

        if isinstance(x, np.ndarray):
            new_x = x.tolist()
        else:
            new_x = x
        
        if isinstance(y, np.ndarray):
            new_y = y.tolist()
        else:
            new_y = y

        xy_set[key] = {'x': new_x, 'y': new_y}

    return xy_set

def get_start_end(hazard, demand_type):
    key = hazard.lower() + "-" + demand_type.lower()
    range = config.RANGE.get(key, "default")
    
    return (range['start'], range['end'])




"""
This library adds the interactive features to basic plots
for the sensitivity analysis

Dependencies:
plotting.py
data_processing.py
matplotlib
numpy
pandas
os
bokeh
"""

import data_processing as dp
from plotting import make_plot, make_second_order_heatmap

import os
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib

from bokeh.models.widgets import Panel, Tabs
from bokeh.io import save, vform
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.models.tools import (BoxZoomTool, ResetTool,
                                PreviewSaveTool,
                                ResizeTool,
                                PanTool, PolySelectTool,
                                WheelZoomTool)


from ipywidgets import (BoundedFloatText, FloatText, Checkbox,
                        SelectMultiple)

from IPython.html.widgets import interact, fixed


# sa_dict = dp.get_sa_data()


def plot_all_outputs(sa_dict, min_val=0.01, top=100, stacked=True,
                     error_bars=True, log_axis=True,
                     highlighted_parameters=[]):
    """
    This function calls plotting.make_plot() for all the sensitivity
    analysis output files and lets you choose which output to view
    using tabs

    Parameters:
    -----------
    sa_dict                : a dictionary with all the sensitivity analysis
                             results
    min_val                : a float indicating the minimum sensitivity value
                             to be shown
    top                    : integer indicating the number of parameters to
                             display (highest sensitivity values)
    stacked1               : Boolean indicating in bars should be stacked for
                             each parameter.
    error_bars             : Booelan indicating if error bars are shown (True)
                             or are omitted (False)
    log_axis               : Boolean indicating if log axis should be used
                             (True) or if a linear axis should be used (False).
    highlighted_parameters : List of strings indicating which parameter wedges
                             will be highlighted

    Returns:
    --------
    p :  a bokeh plot generated with plotting.make_plot() that includes tabs
         for all the possible outputs.
    """

    tabs_dictionary = {}
    outcomes_array = []

    for files in sa_dict.keys():
        outcomes_array.append(sa_dict[files][0])

    for i in range(len(sa_dict)):
        p = make_plot(outcomes_array[i],
                      top=top,
                      minvalues=min_val,
                      stacked=stacked,
                      errorbar=error_bars,
                      lgaxis=log_axis,
                      highlight=highlighted_parameters
                      )[0]
        tabs_dictionary[i] = Panel(child=p, title=sa_dict.keys()[i])

    tabs = Tabs(tabs=tabs_dictionary.values())
    p = show(tabs)

    return p


def interact_with_make_plot(sa_dict):
    """
    This function adds the ability to interactively adjust all of the
    plotting.make_plot() arguments.

    Parameters:
    ----------
    sa_dict : a dictionary with all the sensitivity analysis results

    Returns:
    -------
    An interactive plot
    """
    min_val_box = BoundedFloatText(value=0.01, min=0, max=1,
                                   description='Min value:')
    top_box = FloatText(value=20, description='Show top:')
    stacks = Checkbox(description='Show stacked plots:', value=True,)
    error_bars = Checkbox(description='Show error bars:', value=True)
    log_axis = Checkbox(description='Use log axis:', value=True)

    # get a list of all the parameter options
    key = sa_dict.keys()[0]
    param_options = list(sa_dict[key][0].Parameter.values)
    highlighted = SelectMultiple(description="Choose parameters to highlight",
                                 options=param_options)

    return interact(plot_all_outputs,
                    sa_dict=fixed(sa_dict),
                    min_val=min_val_box,
                    top=top_box,
                    stacked=stacks,
                    error_bars=error_bars,
                    log_axis=log_axis,
                    highlighted_parameters=highlighted,
                    __manual=True
                    )


def plot_all_second_order(sa_dict, top=5, mirror=True, include=[]):
    """
    This function calls plotting.make_second_order_heatmap() for all the
    sensitivity analysis output files and lets you choose which output to view
    using tabs

    Parameters:
    -----------
    sa_dict : a dictionary with all the sensitivity analysis results
    top     : integer indicating the number of parameters to display
              (highest sensitivity values)
    include : a list of parameters you would like to include even if they
              are not in the top `top` values

    Returns:
    --------
    p :  a bokeh plot that includes tabs for all the possible outputs.
    """
    tabs_dictionary = {}
    outcomes_array = []

    for files in sa_dict.keys():
        outcomes_array.append(sa_dict[files][1])

    for i in range(len(sa_dict)):
        p = make_second_order_heatmap(outcomes_array[i],
                                      top=top,
                                      mirror=True,
                                      include=include
                                      )
        tabs_dictionary[i] = Panel(child=p, title=sa_dict.keys()[i])

    tabs = Tabs(tabs=tabs_dictionary.values())
    p = show(tabs)

    return p

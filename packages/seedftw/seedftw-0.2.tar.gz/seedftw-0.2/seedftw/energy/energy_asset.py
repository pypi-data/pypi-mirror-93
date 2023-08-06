# -*- coding: utf-8 -*-
"""
Functions related to modelling of energy assets.

This file can also be imported as a module and contains the following
functions:

    [None] Refer to package "senasopt" on PyPi

Note: the previous functions have been deprecated.

"""

# Import all useful libraries
import numpy as np

def __moved_to_senasopt(new_function):
    raise Exception(
        """This function is deprecated and has been removed.

        To access a similar functionality, refer to the package "senasopt" on PyPi.

        The corresponding function in the package is: senasopt.{}
        (you might however have to do slight aaptation of your code at the interface)

        """.format(new_function)
    )

def wind_turbine_generator(
    *args
):
    ____moved_to_senasopt(new_function="wind.wind_turbine")

def solar_pv_generator(
    *args
):
    ____moved_to_senasopt(new_function="solar.pv_module")

def battery_optimal_controller(
    *args
):
    ____moved_to_senasopt(new_function="battery.battery_optimal_controller")
    

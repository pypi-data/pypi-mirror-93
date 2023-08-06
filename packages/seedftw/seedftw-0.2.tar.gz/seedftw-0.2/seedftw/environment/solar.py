# -*- coding: utf-8 -*-
"""
Functions related to solar radiatiom modelling.

This file can also be imported as a module and contains the following
functions:

    * hour_angle - Computes the solar hour angle
    * declination - Computes the solar declination 
    * day_length - Computes the day length
    * solar_azimuth_angle - Computes the solar azimuth angle
    * zenith_angle - Computes the solar zenith angle 
    * solar_altitude - Computes the solar altitude angle
    * air_mass_ratio - Computes the air-mass ratio 

Work to do:
    * beam_surface_angle - Implement the function
    * implement calls for above functions with lists and dataframe columns

References:
    [1] J. Twidell & T. Weir, Renewable Energy Resources, 2nd edition, 
    Taylor and Francis, 2006

"""

# Import all useful libraries
import numpy as np
from datetime import datetime, timedelta
from pytz import timezone

from seedftw.base.timeseries import timestep_start


# Sine and cosine in degrees
def __cosd(x):
    return np.cos(x * (2 * np.pi / 360))


def __sind(x):
    return np.sin(x * (2 * np.pi / 360))


def __tand(x):
    return np.tan(x * (2 * np.pi / 360))


def __secd(x):
    return 1 / __cosd(x)


def __arccosd(x):
    return 360 / (2 * np.pi) * np.arccos(x)


def __deg2pm180(x):
    return np.mod(x + 180, 360) - 180


# Solar constant ([1] p. 86) - in W/m2
__solar_constant = 1367

# Earth declination ([1] p. 90) - in degrees
__earth_declination = 23.45


def hour_angle(t):
    """Computes the solar hour

    Parameters
    ----------
    t : datetime
        Time for which to compute the hour angle

    Returns
    -------
    w : float
        Solar hour angle [degrees]
    """

    t_utc = t.astimezone(timezone("UTC"))
    w = 15 * (t_utc.hour - 12)
    return w


def declination(t):
    """Computes the solar declination

    Parameters
    ----------
    t : datetime
        Time for which to compute the declination

    Returns
    -------
    d : float
        Solar declination [degrees]
    """
    # From [1] p. 91, adjusted for radians
    t_utc = t.astimezone(timezone("UTC"))
    t_year_start = timestep_start("year", t=t)
    n = (t_utc - t_year_start).days + 1
    d = __earth_declination * np.sin(2 * np.pi * (284 + n) / 365)
    return d


def day_length(t, latitude):
    """Computes the day length

    Parameters
    ----------
    t : datetime
        Time for which to compute the day length
    latitude : float
        Geographical latitude [degrees]

    Returns
    -------
    daylight_hours : float
        Day length [h]
    """
    # From [1] p. 91, adjusted for radians
    d = declination(t)
    temp = -__tand(latitude) * __tand(d)
    if np.abs(temp) <= 1:
        daylight_hours = 2 / 15 * __arccosd(temp)
    else:
        if temp > 0:
            daylight_hours = 0
        else:
            daylight_hours = 24

    return daylight_hours


def solar_azimuth_angle(t, longitude):
    """Computes the solar azimuth angle

    Parameters
    ----------
    t : datetime
        Time for which to compute the azimuth angle
    longitude : datetime
        Longitude for which to compute the azimuth angle [degrees]

    Returns
    -------
    azi : float
        Solar azimuth [degrees]
    """
    # From [1] p.96
    w = hour_angle(t)
    gamma_s = w - longitude
    return __deg2pm180(gamma_s)


def zenith_angle(t, latitude):
    """Computes the solar zenith angle

    Parameters
    ----------
    t : datetime
        Time for which to compute the zenith angle
    latitude : datetime
        Geographical latitude for which to compute the zenith angle [degrees]

    Returns
    -------
    theta_z : float
        Zenith angle [degrees]
    """
    # From [1] p.96
    d = declination(t)
    phi = latitude
    w = hour_angle(t)
    theta_z = __arccosd(__sind(phi) * __sind(d) + __cosd(phi) * __cosd(w) * __cosd(d))
    return theta_z


def solar_altitude(t, latitude):
    """Computes the solar altitude angle

    Parameters
    ----------
    t : datetime
        Time for which to compute the solar altitude angle
    latitude : datetime
        Geographical latitude for which to compute the solar altitude angle [degrees]

    Returns
    -------
    alt : float
        Solar altitude angle [degrees]
    """
    # From [1] p.96
    theta_z = zenith_angle(t, latitude)
    return 90 - theta_z


def air_mass_ratio(t, latitude):
    """Computes the air-mass ratio

    Parameters
    ----------
    t : datetime
        Time for which to compute the air-mass ratio
    latitude : datetime
        Geographical latitude for which to compute the air-mass ratio [degrees]

    Returns
    -------
    AM : float
        Air-mass ratio [/]
        Note: This ratio is truncated below 1 and above 100 to ensure meaningfulness
    """
    # From [1] p.98
    theta_z = zenith_angle(t, latitude)
    AM = __secd(theta_z)
    if AM <= 1 or AM > 100:
        AM = np.nan
    return AM


def beam_surface_angle(t, latitude):
    # From [1] p.95
    raise Exception("To be implemented")


if __name__ == "__main__":

    import plotly.graph_objects as go

    latitude = 45
    t = datetime.now().astimezone(timezone("UTC"))
    day_length(t, latitude)

    solar_altitude(t, latitude)

    solar_azimuth_angle(t, longitude)

    def iterate_on_latitudes(f, lats=[-70, -45, 0, 20, 45, 60, 70, 80], step="day"):
        t0 = datetime.now().astimezone(timezone("UTC"))
        if step == "day":
            dt = lambda i: timedelta(days=i)
            t0 = timestep_start("year", t0)
            n = 365
        elif step == "hour":
            dt = lambda i: timedelta(hours=i)
            t0 = timestep_start("day", t0)
            n = 24

        fig = go.Figure()
        for lat in lats:
            ts = []
            h_day = []
            for i in range(0, n):
                t_i = t0 + dt(i)
                if lat is None:
                    h_day.append(f(t_i))
                else:
                    h_day.append(f(t_i, lat))
                ts.append(t_i)

            fig.add_trace(go.Scatter(x=ts, y=h_day, name=(str(lat))))
            fig["layout"]["yaxis"]["title"] = f.__name__
        return fig

    fig = iterate_on_latitudes(f=day_length, step="day")
    fig.show("png")

    fig = iterate_on_latitudes(f=air_mass_ratio, step="hour")
    fig.show("png")

    fig = iterate_on_latitudes(f=solar_altitude, step="hour")
    fig.show("png")

    fig = iterate_on_latitudes(f=zenith_angle, step="hour")
    fig.show("png")

    fig = iterate_on_latitudes(f=declination, step="day", lats=[None])
    fig.show("png")

    fig = iterate_on_latitudes(f=solar_azimuth_angle, step="hour")
    fig.show("png")

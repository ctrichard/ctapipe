"""Disp method based direction reconstruction


assume phi is good angle







TODO
----


add exception when width or length = 0 
	-> avoid division by 0 in ellipse mono_ellipse()

"""

import numpy as np
from ctapipe.reco import hillas
from astropy.units import Quantity
from collections import namedtuple


__all__ = [
    'MonoDirections',
    'MonoEllipseInfo',
]


MonoDirections = namedtuple(
    "MonoDirections",
    "pos_x,pos_y,pos_xx,pos_yy"
)


MonoEllipseInfo = namedtuple(
    "MonoEllipseInfo",
    "charge , npixel"
)


def disp_value(hillas_parameters):

    """"Compute Disp value

    Parameters
    ----------
    hillas_parameters: namedtuple
	
	
    Returns
    -------
    disp
	
    """

    w = hillas_parameters.width
    l = hillas_parameters.length

    disp = 1 - w / l

    return disp



def mono_source_position(hillas_parameters, disp):
	
    """Compute direction of shower

    Parameters
    -----   -----
    phi: float
        angle between camera x axis and main hillas axis
    cen_x: float
    cen_y: float
        center of the ellipse

    disp: float
        disp value

    Returns
    -------

    position : x and y
    """
    phi = hillas_parameters.phi
    cen_x = hillas_parameters.cen_x
    cen_y = hillas_parameters.cen_y
	
    x = np.cos(phi) * disp + cen_x
    y = np.sin(phi) * disp + cen_y

    """
    xx = cen_x - np.cos(phi) * disp
    yy = cen_y - np.sin(phi) * disp
    """

    return MonoDirections(pos_x=x, pos_y=y)


def mono_ellipse(pix_x, pix_y, image, hillas_parameters):

    """Compute number of pixel inside hillas ellipse

    Parameters
    ----------
    pix_x : array_like
    Pixel x-coordinate
    pix_y : array_like
    Pixel y-coordinate
    hillas_parameters: namedtuple
    Hillas parameters
    image : array_like
    Pixel values corresponding
    Returns
    -------
    Image with only hillas pixels
    """

    pix_x = Quantity(np.asanyarray(pix_x, dtype=np.float64)).value
    pix_y = Quantity(np.asanyarray(pix_y, dtype=np.float64)).value
    image = np.asanyarray(image, dtype=np.float64)
    assert pix_x.shape == image.shape
    assert pix_y.shape == image.shape

    cen_x = hillas_parameters.cen_x
    cen_y = hillas_parameters.cen_x
    w = hillas_parameters.width
    le = hillas_parameters.length

    outsideEllipse = ( pix_x - cen_x )**2  / w + ( pix_y - cen_y )**2 / le  > 1
    image[outsideEllipse] = 0

    return image





def mono_ellipse_info(pix_x, pix_y, image, hillas_parameters):

    """Compute all hillas ellipse related information
    Parameters
    ----------
    pix_x : array_like
        Pixel x-coordinate
    pix_y : array_like
        Pixel y-coordinate
    image : array_like
        Pixel values corresponding
    hillas_parameters: namedtuple
        Hillas parameters
    Returns
    -------
    Charge , npixel
    """

    imagereduced = mono_ellipse(pix_x, pix_y, image, hillas_parameters)
    c = np.sum(imagereduced)
    npix = np.count_nonzero(imagereduced)
    fracpix = np.sum()

    return MonoEllipseInfo(charge=c, npixel=npix, fracbrightpix=fracpix)

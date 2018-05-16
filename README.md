# unhealpix

Regrid a HEALPIX FITS file to target FITS image.

## Description

A simple implementation of [Astropy](http://www.astropy.org/) and [reproject](https://reproject.readthedocs.io/) FITS handling. This script reprojects a HEALPIX projected FITS file to an image projection. Beware of any projection issues this may cause!

## Getting Started

### Dependencies
Required libraries:
* [Astropy](http://www.astropy.org/)
* [reproject](https://reproject.readthedocs.io/)

### Installing

* Simply clone to whever you'd prefer
* Any modifications needed to be made to files/folders

### Executing program
Example usage:
```
python unhealpix.py healpix.fits target.fits output.fits
```
Output will be a FITS file with the shape of `target.fits`

## Notes

Currently the output is forced to be an image (NAXIS = 2). Modifcations will need to be made to handle FITS cubes (e.g. NAXIS = 3). In addition, the output header is rather minimal, so refer to the original file's header for full details.

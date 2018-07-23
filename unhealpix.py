#!/usr/bin/env python

from astropy.io import fits
from reproject import reproject_from_healpix, reproject_to_healpix
import sys


print 'Reading files...'
# Read in HEALPIX file
outf = sys.argv[1]
hdu2 = fits.open(outf)[1]

# Read in target fits file
inf = sys.argv[2]
hdu1 = fits.open(inf)[0]

print 'Generating header...'
# Generate a simple FITS header
target_header = fits.Header.fromstring("""NAXIS   =
NAXIS1  =
NAXIS2  =
CTYPE1  =
CRPIX1  =
CRVAL1  =
CDELT1  =
CTYPE2  =
CRPIX2  =
CRVAL2  =
CDELT2  =
""", sep='\n')

# Copy target information
for i in target_header:
    target_header[i] = hdu1.header[i]

# Force the axes to be 2D
target_header['NAXIS'] = 2

hdu2.header['COORDSYS'] = 'galactic'
# Regrid
print 'Regridding...'
array, footprint = reproject_from_healpix(hdu2, target_header, field = 0)

# Save the file!

outf1 = sys.argv[3]
print 'Saving output to '+ outf1
hdu = fits.PrimaryHDU(array,header=target_header)
hdul = fits.HDUList([hdu])
hdul.writeto(outf1, overwrite=True)

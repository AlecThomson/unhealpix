#!/usr/bin/env python

from astropy.io import fits
from reproject import reproject_from_healpix, reproject_to_healpix
import argparse

# Help string to be shown using the -h option
descStr = """
Regrid a HEALPIX FITS file to target FITS image.
A simple implementation of Astropy and Reproject FITS handling.
This script reprojects a HEALPIX projected FITS file to an image projection.
Beware of any projection issues this may cause!

"""

# Parse the command line options
parser = argparse.ArgumentParser(description=descStr,
                             formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("fitsHEAL", metavar="HEALPIX.fits", nargs=1,
                    help="FITS map in HEALPIX format.")
parser.add_argument("template", metavar="template.fits", nargs=1,
                    help="Template FITS map to project onto.")
parser.add_argument("out", metavar="output.fits", nargs=1,
                    help="FITS map to save output to.")
parser.add_argument("-e", dest="Extension", default=1,
                    help="Extension to select from HEALPIX file.")
parser.add_argument("-f", dest="field", default=0,
                    help="Select field within extension.")
parser.add_argument("-c", dest="COORDSYS", default='galactic',
                    help="Specify COORDSYS card.")
args = parser.parse_args()


print 'Reading files...'
# Read in HEALPIX file
outf = args.fitsHEAL[0]
hdu2 = fits.open(outf)[args.Extension]

# Read in target fits file
inf = args.template[0]
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

hdu2.header['COORDSYS'] = args.COORDSYS
# Regrid
print 'Regridding...'
array, footprint = reproject_from_healpix(hdu2, target_header, field = int(args.field))

# Save the file!

outf1 = args.out[0]
print 'Saving output to '+ outf1
hdu = fits.PrimaryHDU(array,header=target_header)
hdul = fits.HDUList([hdu])
hdul.writeto(outf1, overwrite=True)

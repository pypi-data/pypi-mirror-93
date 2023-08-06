import os, sys, argparse
from . import get_data
from .utils import *

def main():
    geo_msg = 'Use comma seperated values for latitude/longitude, e.g: -g="35.0,67.0"'
    parser = argparse.ArgumentParser(description='Download content from Snapmaps', usage='snapmap_archiver -o [OUTPUT DIR] -g="[LATITUDE],[LONGITUDE]"')
    parser.add_argument('-o', dest='output_dir', type=str, help='Output directory for downloaded content.')
    parser.add_argument('-g', dest='geolocation', type=str, help='Latitude/longitude of desired area.')
    parser.add_argument('-z', dest='zoom_depth', type=float, help='Snapmaps zoom depth, default is 5.')
    parser.add_argument('--write-json', dest='write_json', action='store_true', default=False, help='Write Snap metadata JSON.')
    args = parser.parse_args()

    if(not args.output_dir):
        sys.exit('Output directory (-o) is required.')

    if(not args.geolocation):
        sys.exit('Geolocation (-g) is required.')

    if(',' not in args.geolocation):
        sys.exit(geo_msg)

    if(not os.path.isdir(args.output_dir)):
        try:
            os.mkdir(args.output_dir)
        except:
            sys.exit(f'Could not create directory "{args.output_dir}"')

    try:
        geo_data = args.geolocation.split(',', 1)
        api_response = get_data.api_query(float(geo_data[0]), float(geo_data[1]))
        download_media(args.output_dir, organise_media(api_response), args.write_json)
    except:
        sys.exit(geo_msg)

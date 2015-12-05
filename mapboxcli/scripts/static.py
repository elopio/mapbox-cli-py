import click

import mapbox
from .helpers import MapboxCLIException, normalize_features


@click.command(short_help="Static map images.")
@click.argument('mapid', required=True)
@click.argument('output', type=click.File('wb'), required=True)
@click.option('--features', help="GeoJSON Features to render as overlay")
@click.option('--lat', type=float, help="Latitude")
@click.option('--lon', type=float, help="Longitude")
@click.option('--zoom', type=int, help="Zoom")
@click.option('--size', default=(600, 600), nargs=2, type=(int, int),
              help="Image width and height in pixels")
@click.pass_context
def staticmap(ctx, mapid, output, features, lat, lon, zoom, size):
    """
    Generate static map images from existing Mapbox map ids.
    Optionally overlay with geojson features.

      $ x-mapbox staticmap --features features.geojson mapbox.satellite out.png
      $ x-mapbox staticmap --lon -61.7 --lat 12.1 --zoom 12 mapbox.satellite out2.png

    An access token is required, see `x-mapbox --help`.
    """
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    if features:
        featiter = normalize_features(features)
    else:
        featiter = None

    service = mapbox.Static(access_token=access_token)
    res = service.image(mapid,
                        lon=lon, lat=lat, z=zoom,
                        width=size[0], height=size[1],
                        features=featiter, sort_keys=True)

    if res.status_code == 200:
        output.write(res.content)
    else:
        raise MapboxCLIException(res.text.strip())

import click

import mapbox
from .helpers import MapboxCLIException, normalize_features


@click.command('mapmatching', short_help="Snap GPS traces to OpenStreetMap")
@click.argument('linestring-feature', nargs=1, default="-")
@click.option("--gps-precision", default=4, type=int,
              help="Assumed precision of tracking device (default 4 meters)")
@click.option('--profile', default="mapbox.driving", type=click.Choice([
              'mapbox.driving', 'mapbox.walking', 'mapbox.cycling']),
              help="Mapbox profile id")
@click.pass_context
def match(ctx, linestring_feature, profile, gps_precision):
    """Mapbox Map Matching API lets you use snap your GPS traces
to the OpenStreetMap road and path network.

      $ mapbox mapmatching traces.geojson

An access token is required, see `mapbox --help`.
    """
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    features = normalize_features([linestring_feature])
    if len(features) > 1 or features[0]['geometry']['type'] != 'LineString':
        raise ValueError("Please supply a single linestring feature")

    service = mapbox.MapMatcher(access_token=access_token)
    res = service.match(features[0], profile=profile,
                        gps_precision=gps_precision)

    if res.status_code == 200:
        stdout = click.open_file('-', 'w')
        click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())
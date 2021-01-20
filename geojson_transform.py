import geojson
import shapely
from shapely.geometry.point import Point
from pyproj import Proj, transform
from address_to_latlng import Location


def to_geojson():
    """
    Given a geolocation , return a geojson in a circle shape around that geolocation.
    :param longitude: longitude coming from the coordinates function
    :param latitude: latitude coming from the coordinates function
    :return: geojson
    """
    loc = Location()
    loc.run()

    longitude = float(loc.coord['lng'])
    latitude = float(loc.coord['lat'])
    r = 75
    s = 102
    t = 51
    d = 90

    # change the longitude / latitude to belgian Lambert 1972 x, y
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:31370')
    lng, lat = transform(inProj, outProj, longitude, latitude)
    '''print(longitude)
    print(latitude)
    print(lng)
    print(lat)'''
    """
    # Test to make a circle zone to render
    center = Point(lng,lat)          
    circle = center.buffer(0.3) # degree radius between each point  
    return geojson.dumps(shapely.geometry.mapping(circle))"""

    # create the square polygon
    place_to_render = [{'type': 'Polygon', 'coordinates': [[(lng - r, lat - r), (lng - t, lat - d), (lng, lat - s),
                                                            (lng + t, lat - d),
                                                            (lng + r, lat - r), (lng + d, lat - t), (lng + s, lat),
                                                            (lng + d, lat + t),
                                                            (lng + r, lat + r), (lng + t, lat + d), (lng, lat + s),
                                                            (lng - t, lat + d),
                                                            (lng - r, lat + r), (lng - d, lat + t), (lng - s, lat),
                                                            (lng - d, lat - t)]]}]
    return place_to_render

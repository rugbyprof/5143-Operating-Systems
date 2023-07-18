"""
Classes:
    ObjectEncoder
    Feature 
    FeatureList

Functions:
    isClockWise         : returns if points in list are clockwise
    isCounterClockWise  : opposite of above
    isPoint             : checks geometry for valid point
    isLineString        : checks geometry for valid lineString
    isMultiPoint        :                           multipoint
    isMultiLineString   :                           multiLineString
    isPolygon           :                           polygon
    isMultiPolygon      :                           multiPolygon
    isLinearRing        : Linear ring has min 4 points and first and last point the same
    geometryType        : given a geometry, it will return what type it is

"""

import json
import sys

from rich import print
import gistyc

import inspect


class ObjectEncoder(json.JSONEncoder):
    """
    Source: https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    """

    def default(self, obj):
        if hasattr(obj, "to_json"):
            print("fucking 0")
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            print("fucking A")
            return self.default(d)
        print("fucking C")
        return obj


validLatitude = range(-90, 91)
validLongitude = range(-180, 181)


validGeometryTypes = [
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
]


def isClockWise(coords):
    """
    Determines if the points in a Polygon are clockwise or counter-clockwise

    Params:
        coords (list) : list of points
    Formula:
        (x_2 - x_1)(y_2 + y_1)
    Example:
        point[0] = (5,0)   edge[0]: (6-5)(4+0) =   4
        point[1] = (6,4)   edge[1]: (4-6)(5+4) = -18
        point[2] = (4,5)   edge[2]: (1-4)(5+5) = -30
        point[3] = (1,5)   edge[3]: (1-1)(0+5) =   0
        point[4] = (1,0)   edge[4]: (5-1)(0+0) =   0
                                                ---
                                                -44  counter-clockwise
    positive  = clockwise
    negative  = counter clockwise
    """
    if not isinstance(coords, list):
        return False

    sum = 0
    for i in range(len(coords) - 1):
        if not isPoint(coords[i]):
            return False
        x1 = coords[i][0]
        x2 = coords[i + 1][0]
        y1 = coords[i][1]
        y2 = coords[i + 1][1]
        sum += (x2 - x1) * (y2 + y1)

    return sum >= 0


def isCounterClockWise(coords):
    """Calls `counterClockWise` and returns a logical NOT of that result
    Params:
        coords (list) : list of points
    Returns:
        (bool) : True => points are counter clockwise False => points are clockwise
    """

    return not isClockWise(coords)


def isPoint(point):
    """Checks to see if a point: [x,y] or [lon,lat] has
        1: two integer or floating point values
        2: that the latitude and longitude are within ranges (-90,90 and -180,180)
    Params:
        point (list) : x,y coords or lon,lat coords
    Returns:
        (bool) : true => it is a valid point
    """

    if not type(point) in [list, tuple]:
        return False

    if len(point) != 2:
        return False

    if not type(point[0]) in (int, float) or not type(point[0]) in (int, float):
        return False

    if not int(point[0]) in validLongitude:
        return False

    if not int(point[1]) in validLatitude:
        return False

    return True


def isLineString(coords):
    """Checks to see if a lineString (list of points) is valid

    Params:
        coords (list) : list of x,y points or list of lon,lat points
    Returns:
        (bool) : true => it is a valid lineString
    """
    # 1: is it a list
    if not isinstance(coords, list):
        return False
    # 2: check each point for validity
    for p in coords:
        if not isPoint(p):
            return False
    # 3: Its valid if code makes it here
    return True


def isMultiPoint(coords):
    """A multiPoint is the same as a lineString so we simply call that method"""
    return isLineString(coords)


def isMultiLineString(coords):
    """Checks to see if a multiLineString (list of lineStrings) is valid

    Params:
        coords (list) : list of lineStrings
    Returns:
        (bool) : true => it is a valid multiLineString
    """
    # 1: is it a list
    if not isinstance(coords, list):
        return False
    # 2: are each lines valid lineStrings
    for line in coords:
        if not isLineString(line):
            return False
    # 3: Its valid if code makes it here
    return True


def isLinearRing(coords):
    """A linear ring is as follows:
        - Has 4 or more points
        - The first and last points are exactly the same

      This method assumes that the `coords` param contains valid points.

    Params:
        coords (list): a list of points to check for is "linearRing"

    Returns:
        bool: True = it is a linear ring
    """
    # 1: Is it a list?
    if not isinstance(coords, list):
        return False
    # 2: Does it have 4 or more points
    if len(coords) < 4:
        return False
    # 3: Is first and last coords the same?
    if coords[0] != coords[-1]:
        return False
    # 4: Made it here? You are a linearRing
    return True


def isPolygon(coords):
    """Checks for valid polygon format meaning:
    - It is a list of linear rings (which are lists of points)
    - The outer ring should be counter-clock wise
    - The inner rings (if any) should be clock wise
    Params:
        coords (list): a list of linearRings that make up a polygon
    Returns:
        (bool) : True => it is a polygon
    """
    # basic container must be a list
    if not isinstance(coords, list):
        return False
    # if isPoint(coords):
    #     return False
    # look at each "line" of points
    for i in range(len(coords)):
        if i == 0:
            # outer ring must be counter-clockwise
            if not isCounterClockWise(coords[i]):
                return False
        else:
            # inner ring must be clockwise
            if not isClockWise(coords[i]):
                return False
        # lastly each line must be a valid linearRing
        if not isLinearRing(coords[i]):
            return False
    return True


def isMultiPolygon(coords):
    """Checks for valid multiPolygon format:
        - It is a list of polygons
    Params:
        coords (list): a list of polygons that make up a multiPolygon
    Returns:
        (bool) : True => it is a multiPolygon
    """
    # basic container must be a list
    if not isinstance(coords, list):
        return False
    if isPoint(coords):
        return False
    for polygon in coords:
        if not isPolygon(polygon):
            return False

    return True


def geometryType(geometry):
    lookup = {
        "Point": isPoint,
        "LineString": isLineString,
        "MultiLineString": isMultiLineString,
        "Polygon": isPolygon,
        "MultiPolygon": isMultiPolygon,
    }

    tests = reversed(
        ["Point", "LineString", "MultiLineString", "Polygon", "MultiPolygon"]
    )

    for test in tests:
        if lookup[test](geometry):
            return test
    return None


class Feature(object):
    """Represents a feature that would exist in a geojson feature list

    Params:
        kwargs (dict): all params
            type (string)   : Point, LineString, Polygon, MultiPolygon
            coords (list)   : list of coordinates
            properties(dict): dictionary of key values
    """

    def __init__(self, **kwargs):
        # if a feature is passed in, we will use it
        feature = kwargs.get("feature", None)

        # no feature? them lets look for other peices of data
        if not feature:
            type = kwargs.get("type", None)
            coords = kwargs.get("coords", None)
            properties = kwargs.get("properties", {})

            # build feature using components if they exist
            self.feature = {
                "type": "Feature",
                "geometry": {"type": type, "coordinates": coords},
                "properties": properties,
            }

            # get correct geometry type
            if coords != None:
                self.feature["geometry"]["type"] = geometryType(coords)
        else:
            # use feature passed in (hope its valid!!)
            self.feature = feature

    def to_json(self):
        """Used by the `ObjectEncoder` class at the top to help with json dumping / printing out
        nested objects. This allows a `FeatureCollection` that is made of up `Features` to get
        a decent copy of the feature to be turned into a string, otherwise the encoding was
        getting converted to string twice... ugly long story.
        """
        return self.feature

    def __str__(self):
        """If object printed directly, it will json dumped (converted to a string)."""
        return json.dumps(self.feature, indent=4)

    def __repr__(self):
        return self.__str__()

    def setGeometryType(self, type):
        """Point, LineString, Polygon, MultiPolygon

        Params:
            type (string): valid geojson type
        """
        if type in validGeometryTypes:
            self.feature["geometry"]["type"] = type
        else:
            raise ValueError(f"Your type in `setGeometryType({type})` is not valid!")

    # @property
    # def __geo_interface__(self):
    #     if self.type in validGeometryTypes:
    #         return self

    def addCoords(self, coords):
        """Add or change the geometry of the current feature.
        Params:
            coords (list) : A valid geoJson geometry type (lineString,polygon, etc.)
        """
        self.feature["geometry"]["type"] = geometryType(coords)
        self.feature["geometry"]["coordinates"] = coords

    def addProperty(self, **kwargs):
        """Add a property to the geoJson feature.
        Params:
            kwargs (dict): all params
                properties (dict)   : Dictionary of key value pairs

                    OR

                key (string)        : single string key
                val (string)        : value for previous key
        """
        properties = kwargs.get("properties", None)
        key = kwargs.get("key", None)
        val = kwargs.get("val", None)

        if properties and isinstance(properties, dict):
            for key, val in properties.items():
                self.feature["properties"][key] = val
        elif properties and not isinstance(properties, dict):
            print(
                f"Error: `properties` kwarg existed and was not a dictionary. It was {type(properties)}"
            )
            sys.exit()

        if key and val:
            self.feature["properties"][key] = val


class FeatureCollection(object):
    def __init__(self, **kwargs):

        features = kwargs.get("features", [])

        self.featureCollection = {"type": "FeatureCollection", "features": features}
        self.pretty = kwargs.get("pretty", True)
        self.index = 0  # index for features

    def __str__(self):
        return json.dumps(self.featureCollection, cls=ObjectEncoder, indent=4)

    __repr__ = __str__

    def addFeature(self, **kwargs):
        """Adds a single feature to the feature collection.
        Params:
            kwargs:
                index (int)         : location to place feature within feature collection
                feature (Feature)   : the feature to be added
        """
        # numeric index location to place feature if you wanted it in a certain place
        # within the list of features
        index = kwargs.get("index", None)

        # the feature to add
        feature = kwargs.get("feature", None)

        # current size of feature list
        size = len(self.featureCollection["features"])

        if not isinstance(feature, Feature):
            feature = Feature(feature=feature)

        if not index:
            self.featureCollection["features"].append(feature)
        else:
            if index < size:
                self.featureCollection["features"].insert(index, feature)
            else:
                raise ValueError(
                    f"Your index in `addFeature()` is not valid!  Index: {index} > Size: {size} "
                )

    def addFeatures(self, features):
        """Adds a list of features to the feature list
        Params:
            features (list) : list of features
        """
        if not isinstance(features, list):
            raise ValueError(
                f"Your features `addFeatures()` is not a list! It must be a list of features."
            )

        for feature in features:
            if not isinstance(feature, Feature):
                feature = Feature(feature=feature)

            self.addFeature(feature=feature)

    def getFeature(self, index=None):
        size = len(self.featureCollection["features"])
        if index:
            if not index < size:
                raise ValueError(
                    f"Index passed to getFeature() was out of bounds! Index: {index} Size: {size}"
                )
            f = self.featureCollection["features"][index]
        else:
            f = self.featureCollection["features"][self.index]
            self.index = (self.index + 1) % size

        return f

    def to_json(self):
        """Used by the `ObjectEncoder` class at the top to help with json dumping / printing out
        nested objects. This allows a `FeatureCollection` that is made of up `Features` to get
        a decent copy of the feature to be turned into a string, otherwise the encoding was
        getting converted to string twice... ugly long story.
        """
        return self.featureCollection


if __name__ == "__main__":
    f = Feature()

    print("Empty feature")
    print(f.feature)

    line_string = [
        [88.41796875, 36.1733569352216],
        [91.58203125, 32.99023555965106],
        [95.2734375, 35.31736632923788],
        [94.74609375, 37.996162679728116],
        [88.41796875, 36.1733569352216],
    ]

    print("Feature that should be detected as a lineString")
    f = Feature(coords=line_string)
    print(f)

    # this is a multilinestring with ONE line
    multi_line_string = [
        [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
        [[100.8, 0.8], [100.8, 0.2], [100.2, 0.2], [100.2, 0.8], [100.8, 0.8]],
    ]

    print("Feature that should be detected as a multiLineString")
    f = Feature(coords=multi_line_string)
    print(f)

    poly = [
        [
            [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
            [[100.8, 0.8], [100.8, 0.2], [100.2, 0.2], [100.2, 0.8], [100.8, 0.8]],
        ],
        [
            [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
            [[100.8, 0.8], [100.8, 0.2], [100.2, 0.2], [100.2, 0.8], [100.8, 0.8]],
        ],
    ]

    print("Feature that should be detected as a multipolygon")
    f = Feature(coords=poly)
    print(f)

    ukraine = {
        "type": "Feature",
        "properties": {"name": "Ukraine"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [22.060546874999996, 45.706179285330855],
                    [37.001953125, 45.706179285330855],
                    [37.001953125, 52.3755991766591],
                    [22.060546874999996, 52.3755991766591],
                    [22.060546874999996, 45.706179285330855],
                ]
            ],
        },
    }

    poland = {
        "type": "Feature",
        "properties": {"name": "Poland"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [13.53515625, 48.922499263758255],
                    [24.2578125, 48.922499263758255],
                    [24.2578125, 54.67383096593114],
                    [13.53515625, 54.67383096593114],
                    [13.53515625, 48.922499263758255],
                ]
            ],
        },
    }

    f = Feature(feature=ukraine)
    print(f)

    fl = FeatureCollection(features=[ukraine, poland])
    print(fl)

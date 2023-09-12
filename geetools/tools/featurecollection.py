# coding=utf-8
"""Module holding tools for ee.FeatueCollections."""
import ee

from . import collection as eecollection
from . import geometry as geometry_module


def addId(collection, name="id", start=1):
    """Add a unique numeric identifier, from parameter 'start' to
    collection.size() stored in a property called with parameter 'name'.

    :param collection: the collection
    :type collection: ee.FeatureCollection
    :param name: the name of the resulting property
    :type name: str
    :param start: the number to start from
    :type start: int
    :return: the parsed collection with a new property
    :rtype: ee.FeatureCollection
    """
    start = ee.Number(start)
    collist = collection.toList(collection.size())
    first = ee.Feature(collist.get(0))
    rest = collist.slice(1)

    # Set first id
    first = ee.List([first.set(name, start)])

    # Set rest
    def over_col(feat, last):
        last = ee.List(last)
        last_feat = ee.Feature(last.get(-1))
        feat = ee.Feature(feat)
        last_id = ee.Number(last_feat.get("id"))
        return last.add(feat.set("id", last_id.add(1)))

    return ee.FeatureCollection(ee.List(rest.iterate(over_col, first)))


def clean(collection):
    """Convert Features that have a Geometry of type `GeometryCollection`
    into the inner geometries
    .
    """
    withType = collection.map(
        lambda feat: feat.set("GTYPE", ee.String(feat.geometry().type()))
    )
    geomcol = withType.filter(ee.Filter.eq("GTYPE", "GeometryCollection"))
    notgeomcol = withType.filter(ee.Filter.neq("GTYPE", "GeometryCollection"))

    def wrap(feat, fc):
        feat = ee.Feature(feat)
        fc = ee.FeatureCollection(fc)
        newfc = geometry_module.GeometryCollection_to_FeatureCollection(feat)
        return fc.merge(newfc)

    newfc = ee.FeatureCollection(geomcol.iterate(wrap, ee.FeatureCollection([])))
    return notgeomcol.merge(newfc)


def enumerateProperty(col, name="enumeration"):
    """Create a list of lists in which each element of the list is:
    [index, element]. For example, if you parse a FeatureCollection with 3
    Features you'll get: [[0, feat0], [1, feat1], [2, feat2]].

    :param collection: the collection
    :return: ee.FeatureCollection
    """
    enumerated = eecollection.enumerate(col)

    def over_list(l):
        l = ee.List(l)
        index = ee.Number(l.get(0))
        element = l.get(1)
        return ee.Feature(element).set(name, index)

    featlist = enumerated.map(over_list)
    return ee.FeatureCollection(featlist)


def enumerateSimple(collection, name="ENUM"):
    """Simple enumeration of features inside a collection. Each feature stores
    its enumeration, so if the order of features changes over time, the
    numbers will not be in order
    .
    """
    size = collection.size()
    collist = collection.toList(size)
    seq = ee.List.sequence(0, size.subtract(1))

    def wrap(n):
        n = ee.Number(n).toInt()
        feat = collist.get(n)
        return ee.Feature(feat).set(name, n)

    fc = ee.FeatureCollection(seq.map(wrap))

    return ee.FeatureCollection(fc.copyProperties(source=collection))


def listOptions(collection, propertyName):
    """List all available values of `propertyName` in a feature collection."""

    def wrap(feat, l):
        l = ee.List(l)
        return l.add(feat.get(propertyName))

    options = collection.iterate(wrap, ee.List([]))

    return ee.List(options).distinct()


def mergeGeometries(collection):
    """Merge the geometries of many features. Return ee.Geometry."""
    alist = collection.toList(collection.size())

    first = ee.Feature(alist.get(0))
    rest = alist.slice(1)

    def wrap(feat, ini):
        ini = ee.Geometry(ini)
        feat = ee.Feature(feat)
        geom = feat.geometry()
        union = geom.union(ini)
        return union.dissolve()

    return ee.Geometry(rest.iterate(wrap, first.geometry()))

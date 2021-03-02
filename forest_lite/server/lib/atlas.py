"""Map features lakes, borders etc."""
import forest.data
import cartopy.feature
from forest.data import xs_ys, cut, iterlines


def load_feature(feature, scale, extent):
    if feature.lower() == "borders":
        return multiline(border(scale), extent)
    elif feature.lower() == "coastlines":
        return multiline(coastline(scale), extent)
    elif feature.lower() == "lakes":
        return multiline(lake(scale), extent)
    elif feature.lower() == "disputed":
        return disputed_borders()
    else:
        raise Exception(f"Unrecognised feature: {feature}")


def border(scale):
    """Country borders"""
    return cartopy.feature.NaturalEarthFeature(
            'cultural',
            'admin_0_boundary_lines_land',
            scale)


def coastline(scale):
    """Continent and island coastlines"""
    return cartopy.feature.NaturalEarthFeature(
            'physical',
            'coastline',
            scale)


def lake(scale):
    """Lakes"""
    return cartopy.feature.NaturalEarthFeature(
            'physical',
            'lakes',
            scale)


def multiline(feature, extent=None):
    """Process cartopy feature"""
    if extent is None:
        geometries = feature.geometries()
    else:
        geometries = feature.intersecting_geometries(extent)
    return xs_ys(cut(iterlines(geometries), 180))


def disputed_borders():
    """Politically disputed areas"""
    return xs_ys(iterlines(
            cartopy.feature.NaturalEarthFeature(
                "cultural",
                "admin_0_boundary_lines_disputed_areas",
                "50m").geometries()))

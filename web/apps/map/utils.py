"""Map utils"""
from typing import List, Optional, Tuple

import folium

MarkerModel = Tuple[str, float, float, int]
LABEL = 0
LAT = 1
LON = 2
RADIUS = 3


def get_html_map(target: Optional[MarkerModel] = None,
                 cities: Optional[List[MarkerModel]] = None) -> str:
    """
    Create OpenStreetMap iframe using :params.
    Params:
        :param target: Optional[MarkerModel] - The map is centered on this object
            and draw aroud circle with r=target_range:int (if required).
        :param cities: Optional[List[MarkerModel]] - Drawing FeatureGroup with Marker coordinates.
            :key '<LayerName:str>': - Create new layer with Marker - objects on Map.
    Returns:
        Iframe as html representation of openstreetmap object.

    Examples:
        >>> get_html_map(zoom_start=3,target=('target', 0, 0, 100),cities=)
        ...
        >>> '<div style="width=100%">...</div>'
    """
    # TODO map settings
    #   NOTE zoom - height of iframe ~= diameter*1.2
    #   NOTE max and min lat and lon ~= Point+-radian(radius)
    controls = {
        'location': (target[LAT], target[LON]) if target is not None else (0, 0),
        'zoom_control': True,
        'zoom_start': 8,
        # 'min_lat': ,
        # 'max_lat': ,
        # 'min_lon': ,
        # 'max_lon': ,
    }

    # Create map
    map_obj = folium.Map(**controls)

    # Add layer with target
    if target is not None:
        target_group = folium.FeatureGroup(name="Target", control=False).add_to(map_obj)
        folium.Marker(location=(target[LAT], target[LON]), popup=target[LABEL]).add_to(target_group)

    # Add layer with cities
    if cities is not None:
        cities_group = folium.FeatureGroup(name="Cities", control=True).add_to(map_obj)
        for city in cities:
            folium.Marker(location=(city[LAT], city[LON]), popup=city[LABEL], lazy=True).add_to(cities_group)

    return map_obj._repr_html_()    # type: ignore

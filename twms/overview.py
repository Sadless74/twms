# -*- coding: utf-8 -*-
#    This file is part of tWMS.

#   tWMS is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   tWMS is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with tWMS.  If not, see <http://www.gnu.org/licenses/>.


from config import *
import projections

def html(ref):
    """
    Gives overall information about tWMS server and its layers in HTML format.
    """
    resp = "<!doctype html>"
    resp += "<html><head><title>"
    resp += wms_name
    resp += "</title></head><body><h2>"
    resp += wms_name
    resp += "</h2><table>"
    for i in layers:
      bbox =  layers[i].get("data_bounding_box", projections.projs[layers[i]["proj"]]["bounds"] )
      resp += "<tr><td><img src=\""
      resp += ref + "?layers=" + i+ "&amp;bbox=%s,%s,%s,%s" % bbox + "&amp;width=200&amp;format=image/png\" width=\"200\" /></td><td><h3>"
      resp += layers[i]["name"]
      resp += "</h3><b>Bounding box:</b> "+ str(bbox) +" (show on <a href=\"http://openstreetmap.org/?minlon=%s&amp;minlat=%s&amp;maxlon=%s&amp;maxlat=%s&amp;box=yes\">OSM</a>" % bbox  +")<br />"
      resp += "<b>Projection:</b> "+ layers[i]["proj"]  +"<br />"
      resp += "<b>WMS half-link:</b> "+ ref + "?layers=" + i + "&amp;<br />"
      resp += "<b>Tiles URL:</b> "+ ref + "" + i + "/!/!/!." + layers[i].get("ext", "jpg") + "<br />"
      resp += "</td></tr>"
    resp += "</table></body></html>"
    return resp

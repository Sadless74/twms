# -*- coding: utf-8 -*-
#    This file is part of twms.

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

try:
    from PIL import Image, ImageDraw, ImageColor
except ImportError:
    import Image, ImageDraw, ImageColor

import urllib
import os, sys
import array

import projections
import config
from gpxparse import GPXParser
import math


HAVE_CAIRO = True
try:
  import cairo
except ImportError:
  HAVE_CAIRO = False

def wkt(wkt, img, bbox, srs, color, blend = 0.5):
    """
    Simple WKT renderer
    """
    wkt = wkt.replace("((","(")
    for obj in wkt.split("),"):

       canvas = img.copy()
       name, coords = obj.split("(")
       coords = coords.replace(")","")
       coords = coords.split(",")
       coords = [ [float(t) for t in x.split(" ")] for x in coords]
       canvas = render_vector(name, canvas, bbox, coords, srs, color)
       img = Image.blend(img, canvas, blend)
    return img

def gpx(track, img, bbox, srs, color, blend = 0.5):
    """
    Simple GPX renderer
    """
    for i in track.tracks.keys():
      coords = track.getTrack(i)
      canvas = img.copy()
      canvas = render_vector("LINESTRING", canvas, bbox, coords, srs, color)
      img = Image.blend(img, canvas, blend)
    return img


def render_vector(geometry, img, bbox, coords, srs, color=None, renderer=None):
    """
    Renders a vector geometry on image.
    """
    if not color:
      color = config.geometry_color[geometry]
    if not renderer:
      renderer = config.default_vector_renderer
    bbox = projections.from4326(bbox, srs)
    lo1, la1, lo2, la2 = bbox
    coords = projections.from4326(coords, srs)
    W,H = img.size
    prevcoord = False
    coords = [((coord[0]-lo1)*(W-1)/abs(lo2-lo1), (la2-coord[1])*(H-1)/(la2-la1)) for coord in coords]

    if renderer == "cairo" and HAVE_CAIRO:
      "rendering as cairo"
      imgd = img.tostring()
      a = array.array('B',imgd)
      surface = cairo.ImageSurface.create_for_data (a, cairo.FORMAT_ARGB32, W, H, W*4)
      cr = cairo.Context(surface)
      cr.move_to(*coords[0])
      color = ImageColor.getrgb(color)
      cr.set_source_rgba(color[2]/255.0, color[1]/255.0, color[0]/255.0, 1)
      if geometry == "LINESTRING" or geometry == "POLYGON":
        for k in coords:
          cr.line_to(*k)
      if geometry == "LINESTRING":
        cr.stroke()
      elif geometry == "POLYGON":
        cr.fill()
      elif geometry == "POINT":
        cr.arc(coords[0][0],coords[0][1],6,0,2*math.pi)
        cr.fill()
      img = Image.frombuffer("RGBA",( W,H ),surface.get_data(),"raw","RGBA",0,1)
    
    else:
      "falling back to PIL"
      coord = [(int(coord[0]),int(coord[1])) for coord in coords]                 # PIL dislikes subpixels
      draw = ImageDraw.Draw(img)
      if geometry == "LINESTRING":
        draw.line (coords, fill=color, width=3)
      elif geometry == "POINT":
        draw.ellipse((coords[0][0]-3,coords[0][1]-3,coords[0][0]+3,coords[0][1]+3),fill=color,outline=color)
      elif geometry == "POLYGON":
        draw.polygon(coords, fill=color, outline=color)
    return img

About
=====

twms is a script that connects World of Tiles and World of WMS.
The name ‘twms’ stands for twms web map server.

The primary purpose of twms is to export your map tiles to the
WMS-enabled applications.

twms can export a set of raster tiles as a WMS service
so GIS applications that support WMS protocol can access
this tile set. Also, twms can act as a proxy and perform
WMS requests to external services and serve the tile cache

Documentation
=============

Documentation is in Wiki branch of the project.

https://github.com/Komzpa/twms/blob/wiki/Installing.md
https://github.com/Komzpa/twms/blob/wiki/Filters.md
https://github.com/Komzpa/twms/blob/wiki/Config.md

twms imlplements OGC WMS protocol, http://www.opengeospatial.org/standards/wms

TODO
====

 - Make fetchers work with proxy
 - Full reprojection support
 - Imagery realignment

Conventions
===========

 - Inside tWMS, only EPSG:4326 latlon should be used for transmitting coordinates.

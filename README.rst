!!!!!!! Updated to run using urllib3, tested in python 3.9
Test program is basis of something i was using to check forecast
at local skateparks.. !!!!!!!

================
 metoffer v.2.0
================

metoffer is a simple wrapper for the API provided by the British
`Met Office <http://www.metoffice.gov.uk>`_ known as DataPoint. It
can be used to retrieve weather observations and forecasts. At its
heart is the ``MetOffer`` class which has methods to retrieve data
available through the API and make them available as Python objects.
Also included are a couple of functions and classes useful for
interpretting the data.

This project is now maintained at `<https://github.com/sludgedesk/metoffer>`_.

Example
-------

Get forecast for Met Office site closest to supplied latitude and
longitude, the forecast to be given in three-hourly intervals::

	>>> import metoffer
	>>> api_key = '01234567-89ab-cdef-0123-456789abcdef'
	>>> M = metoffer.MetOffer(api_key)
	>>> x = M.nearest_loc_forecast(51.4033, -0.3375, metoffer.THREE_HOURLY)

*It's worth noting here that, if you expect many requests for forecast data
to be made, it is probably better to use the functions called by this
convenience function so that data that does not change often (e.g. data
about Met Office sites) may be cached.*

Parse this data into a ``metoffer.Weather`` instance::

	>>> y = metoffer.Weather(x)
	>>> y.name
	'HAMPTON COURT PALACE'
	>>> y.country
	'ENGLAND'
	>>> y.continent
	'EUROPE'
	>>> y.lat
	51.4007
	>>> y.lon
	-0.3337
	>>> y.elevation
	4.0
	>>> y.ident # The Met Office site ident
	'351747'
	>>> y.data_date
	'2014-06-14T23:00:00Z'
	>>> y.dtype
	'Forecast'
	>>> import pprint
	>>> pprint.pprint(y.data)
	[{'Feels Like Temperature': (17, 'C', 'F'),
	  'Max UV Index': (1, '', 'U'),
	  'Precipitation Probability': (7, '%', 'Pp'),
	  'Screen Relative Humidity': (63, '%', 'H'),
	  'Temperature': (19, 'C', 'T'),
	  'Visibility': ('VG', '', 'V'),
	  'Weather Type': (7, '', 'W'),
	  'Wind Direction': ('NNE', 'compass', 'D'),
	  'Wind Gust': (18, 'mph', 'G'),
	  'Wind Speed': (11, 'mph', 'S'),
	  'timestamp': (datetime.datetime(2014, 6, 14, 18, 0), '')},
	 {'Feels Like Temperature': (15, 'C', 'F'),
	  'Max UV Index': (0, '', 'U'),
	  'Precipitation Probability': (0, '%', 'Pp'),
	  'Screen Relative Humidity': (72, '%', 'H'),
	  'Temperature': (16, 'C', 'T'),
	  'Visibility': ('VG', '', 'V'),
	  'Weather Type': (0, '', 'W'),
	  'Wind Direction': ('NNE', 'compass', 'D'),
	  'Wind Gust': (18, 'mph', 'G'),
	  'Wind Speed': (9, 'mph', 'S'),
	  'timestamp': (datetime.datetime(2014, 6, 14, 21, 0), '')},

	    [...]

	 {'Feels Like Temperature': (16, 'C', 'F'),
	  'Max UV Index': (0, '', 'U'),
	  'Precipitation Probability': (2, '%', 'Pp'),
	  'Screen Relative Humidity': (66, '%', 'H'),
	  'Temperature': (16, 'C', 'T'),
	  'Visibility': ('VG', '', 'V'),
	  'Weather Type': (0, '', 'W'),
	  'Wind Direction': ('NNE', 'compass', 'D'),
	  'Wind Gust': (13, 'mph', 'G'),
	  'Wind Speed': (7, 'mph', 'S'),
	  'timestamp': (datetime.datetime(2014, 6, 18, 21, 0), '')}]

Interpret the data further::

	>>> for i in y.data:
	...     print("{} - {}".format(i["timestamp"][0].strftime("%d %b, %H:%M"), metoffer.WEATHER_CODES[i["Weather Type"][0]]))
	... 
	14 Jun, 18:00 - Cloudy
	14 Jun, 21:00 - Clear night
	15 Jun, 00:00 - Clear night
	15 Jun, 03:00 - Cloudy

	    [...]

	18 Jun, 09:00 - Partly cloudy (day)
	18 Jun, 12:00 - Partly cloudy (day)
	18 Jun, 15:00 - Cloudy
	18 Jun, 18:00 - Cloudy
	18 Jun, 21:00 - Clear night
	>>> metoffer.VISIBILITY[y.data[0]["Visibility"][0]]
	'Very good - Between 20-40 km'
	>>> metoffer.guidance_UV(y.data[0]["Max UV Index"][0])
	'Low exposure. No protection required. You can safely stay outside'

The MetOffer Class
------------------

Available methods:

* ``loc_forecast``. Return location-specific forecast data (including lists of
  available sites and time capabilities) for given time step.

* ``nearest_loc_forecast``. Work out nearest possible site to lat & lon
  coordinates and return its forecast data for the given time step.

* ``loc_observations``. Return location-specific observation data, including a
  list of available sites (time step will be HOURLY).

* ``nearest_loc_obs``. Work out nearest possible site to lat & lon coordinates
  and return observation data for it.

* ``text_forecast``. Return textual forecast data for regions, national parks
  or mountain areas.

* ``text_uk_extremes``. Return textual data of UK extremes.

* ``stand_alone_imagery``. Returns capabilities data for stand alone imagery and
  includes URIs for the images.

* ``map_overlay_forecast``. Returns capabilities data for forecast map overlays.

* ``map_overlay_obs``. Returns capabilities data for observation map overlays.

The Site Class
--------------

Describes object to hold site metadata.  Also describes method
(``distance_to_coords``) to return a Site instance's 'distance' from any given
lat & lon coordinates.  This 'distance' is a value which is used to guide
``MetOffer.nearest_loc_forecast`` and ``MetOffer.nearest_loc_obs``. It simply
calculates the difference between the two sets of coordinates and arrives at a
value through Pythagorean theorem.

The Weather Class
-----------------

A hold-all for returned weather data, including associated metadata.  It parses
returned dict of MetOffer location-specific data into a Weather instance.
Works with single or multiple time steps.  There are a couple of points to
note:

* All dict keys have a tuple, even where there is no obvious need, such as
  with 'timestamp' and 'Weather Type'.  'timestamp' is a 2-tuple, all else
  is a 3-tuple.  This is a feature.

* When the Met Office does not have a recorded observation against a category,
  metoffer will return None.

* For parsed DAILY forecasts, the hours and minutes of the 'timestamp'
  datetime.datetime object are superfluous.  In fact, it would be misleading
  to follow them.  Rather, this time there is a sensible entry in the second
  part of the tuple.  This alternates between 'Day' and 'Night' with each
  successive dict.  The categories are often specific to the time of day.
  This is how the API provides it.  Take note as it may catch you out.

The TextForecast Class
----------------------

A hold-all for returned textual regional forecasts, including associated meta-
data, created by parsing the data returned by ``MetOffer.text_forecast``.

Useful Functions
----------------

* ``parse_sitelist``. Return list of Site instances from retrieved sitelist data.

* ``get_nearest_site``. Return a list of strings (site IDs) which can be used
  as 'request' in calls to ``loc_forecast`` and ``loc_observations``.

* ``guidance_UV``. Return Met Office guidance regarding UV exposure based on UV
   index.

* ``extract_data_key``. Returns a dict that maps measurement type to its description
  and measurement unit.

Feedback & Bug Reports
----------------------

Get in touch:

Stephen B Murray <sbm199@gmail.com>
@sludgedesk

Legal
-----

Copyright 2012-2014, 2018 Stephen B Murray

Distributed under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

You should have received a copy of the GNU General Public License along with
this package. If not, see <http://www.gnu.org/licenses/>

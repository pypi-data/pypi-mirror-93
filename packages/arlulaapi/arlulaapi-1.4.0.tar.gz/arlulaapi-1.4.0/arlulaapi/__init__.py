import gevent.monkey as curious_george
curious_george.patch_all(thread=False, select=False)
import math
import pgeocode
import sys
import platform
import arlulacore
import grequests
import json
import os
import typing
import warnings

# Package Name
name = "arlulaapi"

# User agent setting
sdk_version = "1.4.0"
py_version = sys.version.split(' ')[0]
os_version = platform.platform()
def_ua = "archive-sdk " + \
    sdk_version + " python " + py_version + " OS " + os_version


# Exception when group searching


def gsearch_exception(r, e):
    return("request failed")


class Session:

    def __init__(self, key, secret, user_agent=def_ua):
        self.session = arlulacore.Session(key,
                                          secret,
                                          user_agent=user_agent)
        self.archive = arlulacore.Archive(self.session)
        self.orders = arlulacore.Orders(self.session)
        self.max_cloud = 100

    def set_max_cloud(self, val):
        if (val < 0 or val > 100):
            raise arlulacore.ArlulaSessionError(
                "Max cloud value must be between 0 and 100")
        self.max_cloud = val

    def get_max_cloud(self):
        return self.max_cloud

    def filter(self, r):
        if isinstance(r, arlulacore.ArlulaObj):
            return r.cloud <= self.max_cloud
        else:
            return r['cloud'] <= self.max_cloud

    def search(self,
               start: typing.Optional[str] = None,
               end: typing.Optional[str] = None,
               res: typing.Optional[typing.Union[float, str]] = None,
               lat: typing.Optional[float] = None,
               long: typing.Optional[float] = None,
               north: typing.Optional[float] = None,
               south: typing.Optional[float] = None,
               east: typing.Optional[float] = None,
               west: typing.Optional[float] = None):
        return [x for x in self.archive.search(
                start=start,
                end=end,
                res=res,
                lat=lat,
                long=long,
                north=north,
                south=south,
                east=east,
                west=west)
                if self.filter(x)]

    def order(self,
              id: typing.Optional[str] = None,
              eula: typing.Optional[str] = None,
              seats: typing.Optional[int] = None,
              webhooks: typing.List[str] = [],
              emails: typing.List[str] = []):
        return self.archive.order(
            id=id,
            eula=eula,
            seats=seats,
            webhooks=webhooks,
            emails=emails
        )

    def get_order(self,
                  id: typing.Optional[str] = None):
        return self.orders.get(id=id)

    def list_orders(self):
        return self.orders.list()

    def get_resource(self,
                     id: typing.Optional[str] = None,
                     filepath: typing.Optional[str] = None,
                     suppress: bool = False,
                     # an optional generator that yields float or None
                     progress_generator: typing.Optional[typing.Generator[typing.Optional[float], None, None]] = None):
        self.orders.get_resource(
            id=id,
            filepath=filepath,
            suppress=suppress,
            progress_generator=progress_generator
        )

    # Asynchronously retrieves multiple searches and aggregates results
    def gsearch(self,
                params):
        searches = []
        for p in params:
            url = self.session.baseURL+"/api/archive/search"

            querystring = {k: v for k, v in p.items()
                           if v is not None or v == 0}

            searches.append(grequests.get(
                url,
                headers=self.session.header,
                params=querystring))

        # Send requests and wait for all to return
        response = grequests.map(
            searches, exception_handler=gsearch_exception)

        # Aggregate results
        result = []
        for r in response:
            result.extend([arlulacore.ArlulaObj(x)
                           for x in json.loads(r.text) if self.filter(x)])
        return result

    def get_order_resources(self,
                            id: typing.Optional[str] = None,
                            folder: typing.Optional[str] = None,
                            suppress: bool = False):
        if folder is None:
            raise arlulacore.ArlulaSessionError(
                "You must specify a folder for the download")

        if not os.path.exists(folder):
            os.makedirs(folder)

        # Get the list of resources
        res = self.get_order(id=id)
        counter = 1
        total = len(res.resources)

        # For each resource, download using get_resource
        for r in res.resources:
            querystring = {"id": id}

            if not suppress:
                print("File {} of {}".format(counter, total))
            try:
                self.get_resource(id=r.id, filepath=folder +
                                  "/"+r.name, suppress=suppress)
            except Exception as e:
                print("Error retrieving file {}, id={}, filename={}".format(
                    counter, r.id, r.name))
                print(e)
            counter += 1
        if not suppress:
            print("All files downloaded")

    def parse_postcode(self, res):
        if math.isnan(res.latitude):
            raise arlulacore.ArlulaSessionError(
                "Could not find postcode {}".format(res.postal_code))
        if res.accuracy >= 5:
            warnings.warn(
                "Postcode {} lat/long could be inaccurate".format(res.postal_code), arlulacore.ArlulaSessionWarning)
        return {'postcode': res.postal_code, 'lat': res.latitude, 'long': res.longitude, 'name': res.place_name}

    def search_postcode(self,
                        start: typing.Optional[str] = None,
                        end: typing.Optional[str] = None,
                        res: typing.Optional[typing.Union[float, str]] = None,
                        country: typing.Optional[str] = None,
                        postcode: typing.Optional[typing.Union[str, int,
                                                  typing.List[typing.Union[str, int]]]] = None,
                        boxsize: typing.Optional[float] = None):

        # transformation constants
        dist_to_deg_lat = 110.574
        dist_to_deg_long_factor = 111.32

        # Find country
        try:
            nomi = pgeocode.Nominatim(country)
        except ValueError:
            raise arlulacore.ArlulaSessionError(
                "Invalid country code {}".format(country))

        if isinstance(postcode, str) or isinstance(postcode, int):
            postcode = [postcode]

        # For each postcode, find coordinates using pgeocode
        data = nomi.query_postal_code(postcode)
        params = []
        pcs = [self.parse_postcode(d[1]) for d in data.iterrows()]

        # Set parameters and search simultaneously across all postcodes
        if boxsize is None:
            params = [{'start': start, 'end': end, 'res': res,
                       'lat': pc['lat'], 'long': pc['long']} for pc in pcs]
        else:
            params = [{'start': start, 'end': end, 'res': res,
                       'south': pc['lat']-boxsize/dist_to_deg_lat,
                       'north': pc['lat']+boxsize/dist_to_deg_lat,
                       'west': pc['long']-boxsize/(math.cos(math.radians(pc['lat']))*dist_to_deg_long_factor),
                       'east': pc['long']+boxsize/(math.cos(math.radians(pc['lat']))*dist_to_deg_long_factor)} for pc in pcs]
        search_res = self.gsearch(params=params)

        # Return results
        if len(pcs) == 1:
            return arlulacore.ArlulaObj({'location': pcs[0], 'data': search_res[0]})
        return [arlulacore.ArlulaObj({'location': pcs[i], 'data': search_res[i]}) for i in range(0, len(pcs))]

# Make compatible with old versions
ArlulaSession = Session
import os
import json
import logging
from requests import get
from uuid import uuid1, uuid4
from datetime import datetime, timedelta
from urllib.parse import urlencode, urljoin, urlparse


class Pluto:
    """
    Automatically gets the channels data from pluto.tv

    Attributes:
    - channels: the channels data from pluto.tv

    Methods:
    - generate_m3u8: generates a m3u8 string with the channels
    - write_m3u8: writes the m3u8 file to disk

    """

    CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache.json")
    DATE_FORMAT = "%Y-%m-%dT%H:00:00.000Z"
    CHANNELS_URL = "http://api.pluto.tv/v2/channels"

    PARAMS = {
        "advertisingId": "",
        "appName": "web",
        "appVersion": "unknown",
        "appStoreUrl": "",
        "architecture": "",
        "buildVersion": "",
        "clientTime": "0",
        "deviceDNT": "0",
        "deviceId": uuid1(),
        "deviceMake": "Chrome",
        "deviceModel": "web",
        "deviceType": "web",
        "deviceVersion": "unknown",
        "includeExtendedEvents": "false",
        "sid": uuid4(),
        "userId": "",
        "serverSideAds": "true",
    }

    def __init__(self) -> None:
        self.channels = self.__get_channels()

    def __load_cache(self) -> dict:
        """
        Load the cached channels if present and is not older than 30 minutes

        """
        logging.debug("loading cache")

        try:
            if (
                os.path.getmtime(self.CACHE_FILE)
                > (datetime.now() - timedelta(minutes=30)).timestamp()
            ):
                logging.debug("loading channels from cache")
                with open(self.CACHE_FILE, "r") as f:
                    return json.load(f)
        except FileNotFoundError:
            logging.debug("cache not found")

    def __get_channels(self) -> dict:
        """
        Get the channels data from pluto.tv
        if the data is not cached or is older than 30 minutes

        """
        logging.debug("getting channels data")

        cache = self.__load_cache()

        if cache:
            return cache

        # getting the channels data from pluto.tv
        start = datetime.now()
        stop = start + timedelta(hours=48)

        params = {
            "start": start.strftime(self.DATE_FORMAT),
            "stop": stop.strftime(self.DATE_FORMAT),
        }

        response = get(self.CHANNELS_URL, params=params)

        if response.status_code == 200:

            data = response.json()

            with open(self.CACHE_FILE, "w") as f:
                json.dump(data, f, indent=4)

            return data

        else:
            logging.error("error getting channels data")
            response.raise_for_status()

    def generate_m3u8(self) -> str:
        """
        Genenerates a m3u8 string with the channels

        """
        logging.debug("generating m3u8 file")

        result = []

        for channel in self.channels:
            if channel["isStitched"]:
                slug = channel["slug"]
                logo = channel["colorLogoPNG"]["path"]
                group = channel["category"]
                name = channel["name"]

                url = channel["stitched"]["urls"][0]["url"]
                base_uri = urljoin(url, urlparse(url).path)
                m3u8_url = f"{base_uri}?{urlencode(self.PARAMS)}"

                result.append(
                    f'#EXTINF:0 tvg-id="{slug}" '
                    f'tvg-logo="{logo}" '
                    f'group-title="{group}", '
                    f"{name}\n{m3u8_url}"
                )

        return "\n\n".join(result)

    def write_m3u8(self, filename="pluto_tv") -> None:
        """
        Writes the m3u8 file to disk

        """
        logging.debug("writing m3u8 file")

        with open(f"{filename}.m3u8", "w") as f:
            f.write(self.generate_m3u8())

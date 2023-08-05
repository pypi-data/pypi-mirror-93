#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Porsche Connect API.

"""
import asyncio
import calendar
import datetime
import json
import logging
import time
from typing import Dict, Text

import aiohttp
from yarl import URL

from .exceptions import IncompleteCredentials, PorscheException

_LOGGER = logging.getLogger(__name__)


class Connection:
    """Connection to Porsche Connect API."""

    def __init__(
        self,
        websession: aiohttp.ClientSession,
        email: Text = None,
        password: Text = None,
        access_token: Text = None,
        refresh_token: Text = None,
        expiration: int = 0,
    ) -> None:
        """Initialize connection object."""
        self.user_agent: Text = "Android REL 4.4.4; en_US"
        self.client_id: Text = "TZ4Vf5wnKeipJxvatJ60lPHYEzqZ4WNp"
        self.porscheLogin: Text = "https://login.porsche.com/auth/de/de_DE"
        self.porscheLoginAuth: Text = "https://login.porsche.com/auth/api/v1/de/de_DE/public/login"
        self.porscheAPIClientID: Text = "TZ4Vf5wnKeipJxvatJ60lPHYEzqZ4WNp"
        self.porscheAPIRedirectURI: Text = "https://my-static02.porsche.com/static/cms/auth.html"
        self.porscheAPIAuth: Text = "https://login.porsche.com/as/authorization.oauth2"
        self.porscheAPIToken: Text = "https://login.porsche.com/as/token.oauth2"
        self.porscheAPI: Text = "https://connect-portal.porsche.com/core/api/v3/de/de_DE"

        self.oauth: Dict[Text, Text] = {}
        self.expiration: int = expiration
        self.access_token = access_token
        self.head = None
        self.refresh_token = refresh_token
        self.websession = websession
        self.token_refreshed = False
        self.generate_oauth(email, password, refresh_token)
        if self.access_token:
            self.__sethead(access_token=self.access_token, expiration=self.expiration)
            _LOGGER.debug("Connecting with existing access token")

    def generate_oauth(
        self, email: Text = None, password: Text = None, refresh_token: Text = None
    ) -> None:
        """Generate oauth header.

        Args
            email (Text, optional): Porsche account email address. Defaults to None.
            password (Text, optional): Password for account. Defaults to None.
            refresh_token (Text, optional): Refresh token. Defaults to None.

        Raises
            IncompleteCredentials

        Returns
            None

        """
        refresh_token = refresh_token or self.refresh_token
        self.oauth = {"client_id": self.client_id }
        if email and password:
            self.oauth["grant_type"] = "password"
            self.oauth["email"] = email
            self.oauth["password"] = password
        elif refresh_token:
            self.oauth["grant_type"] = "refresh_token"
            self.oauth["refresh_token"] = refresh_token
        elif not refresh_token:
            raise IncompleteCredentials(
                "Missing oauth authentication details: refresh token."
            )
        else:
            raise IncompleteCredentials(
                "Missing oauth authentication details: email and password."
            )

    async def get(self, command):
        """Get data from API."""
        return await self.post(command, "get", None)

    async def post(self, command, method="post", data=None):
        """Post data to API."""
        now = calendar.timegm(datetime.datetime.now().timetuple())
        if now > self.expiration:
            _LOGGER.debug(
                "Requesting new oauth token using %s", self.oauth["grant_type"]
            )
            auth = await self.__open("/oauth/token", "post", data=self.oauth)
            self.__sethead(
                access_token=auth["access_token"], expires_in=auth["expires_in"]
            )
            self.refresh_token = auth["refresh_token"]
            self.generate_oauth()
            self.token_refreshed = True
        return await self.__open(
            f"{self.api}{command}", method=method, headers=self.head, data=data
        )

    def __sethead(
        self, access_token: Text, expires_in: int = 1800, expiration: int = 0
    ):
        """Set HTTP header."""
        self.access_token = access_token
        if expiration > 0:
            self.expiration = expiration
        else:
            now = calendar.timegm(datetime.datetime.now().timetuple())
            self.expiration = now + expires_in
        self.head = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": self.user_agent,
        }

    async def __open(
        self,
        url: Text,
        method: Text = "get",
        headers=None,
        data=None,
        baseurl: Text = "",
    ) -> None:
        """Open url."""
        headers = headers or {}
        if not baseurl:
            baseurl = self.baseurl
        url: URL = URL(baseurl + url)

        _LOGGER.debug("%s: %s %s", method, url, data)

        try:
            resp = await getattr(self.websession, method)(
                url, headers=headers, data=data
            )
            data = await resp.json()
            _LOGGER.debug("%s: %s", resp.status, json.dumps(data))
            if resp.status > 299:
                if resp.status == 401:
                    if data and data.get("error") == "invalid_token":
                        raise PorscheException(resp.status, "invalid_token")
                elif resp.status == 408:
                    raise PorscheException(resp.status, "vehicle_unavailable")
                raise PorscheException(resp.status)
            if data.get("error"):
                # known errors:
                #     'vehicle unavailable: {:error=>"vehicle unavailable:"}',
                #     "upstream_timeout", "vehicle is curently in service"
                _LOGGER.debug(
                    "Raising exception for : %s",
                    f'{data.get("error")}:{data.get("error_description")}',
                )
                raise PorscheException(
                    f'{data.get("error")}:{data.get("error_description")}'
                )
        except aiohttp.ClientResponseError as exception_:
            raise PorscheException(exception_.status)
        return data

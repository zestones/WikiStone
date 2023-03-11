from wikibase_api import Wikibase as WikibaseApi

from wikibase_request_api.data_model import (
    Aliases,
    Claim,
    Claims,
    Description,
    Item,
    Label,
    Property,
    Qualifier,
    Qualifiers,
    Reference,
    References,
)
from wikibase_request_api.data_types import ExternalId, GeoLocation, Quantity, StringValue, UrlValue

DEFAULT_CONFIG = {
	"api_url": "http://localhost/w/api.php",
    "oauth_credentials": {},
    "login_credentials": {
		"botUsername": "Admin@botstone",
		"botPassword": "i64r0f9ujvu780cd27sovvf19ds4pige"
	},
	"is_bot": True,
	"summary": "Modified using python-wikibase"
}


class PyWikibase:
    def __init__(
        self,
        # wikibase-api params
        api_url=DEFAULT_CONFIG["api_url"],
        oauth_credentials=DEFAULT_CONFIG["oauth_credentials"],
        login_credentials=DEFAULT_CONFIG["login_credentials"],
        is_bot=DEFAULT_CONFIG["is_bot"],
        summary=DEFAULT_CONFIG["summary"],
        config_path=None,
        # Other params
        language="en",
    ):
        # Create instance of wikibase-api's Wikibase class (includes authentication)
        self.api = WikibaseApi(
            api_url=api_url,
            oauth_credentials=oauth_credentials,
            login_credentials=login_credentials,
            is_bot=is_bot,
            summary=summary,
            config_path=config_path,
        )

        self.language = language
        self.api_url = api_url

    def getApiUrl(self):
        return self.api_url

    def getLanguage(self):
        return self.language

    def setLanguage(self, lang):
        self.language = lang

    # Data model

    def Aliases(self):
        return Aliases(self, self.api, self.language)

    def Claim(self):
        return Claim(self, self.api, self.language)

    def Claims(self):
        return Claims(self, self.api, self.language)

    def Description(self):
        return Description(self, self.api, self.language)

    def Item(self):
        return Item(self, self.api, self.language)

    def Label(self):
        return Label(self, self.api, self.language)

    def Property(self):
        return Property(self, self.api, self.language)

    def Qualifier(self):
        return Qualifier(self, self.api, self.language)

    def Qualifiers(self):
        return Qualifiers(self, self.api, self.language)

    def Reference(self):
        return Reference(self, self.api, self.language)

    def References(self):
        return References(self, self.api, self.language)

    # Data types

    def ExternalId(self):
        return ExternalId(self, self.api, self.language)

    def GeoLocation(self):
        return GeoLocation(self, self.api, self.language)

    def Quantity(self):
        return Quantity(self, self.api, self.language)

    def StringValue(self):
        return StringValue(self, self.api, self.language)

    def UrlValue(self):
        return UrlValue(self, self.api, self.language)

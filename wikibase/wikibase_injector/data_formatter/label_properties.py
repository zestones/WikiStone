
# VALUE OF THE PROPERTIES
TYPE_STRING = "StringValue"
TYPE_URL = "UrlValue"
TYPE_COORDINATE = "GeoLocation"

# DESCRIPTION OF THE ITEM
ITEM_DESCRIPTION = "description"

# CONTENT OF A PROP OBJECT
LABEL = "label"
TYPE = "type"
DESCRIPTION = "description"

###### LABEL OF THE PROPERTIES ######
PROP_REGION = {
    LABEL: "region",
    TYPE: TYPE_STRING,
    DESCRIPTION: "La Région est la plus récente des collectivités territoriales, reconnue en 1982 par les lois de décentralisation au même titre que la commune et le département, mais véritablement « opérationnelle » en 1986, après les premières élections régionales.",
}

PROP_DEPARTEMENT = {
    LABEL: "departement",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Le département est à la fois : une circonscription administrative, territoire de compétence de services de l'État",
}

PROP_CITY = {
    LABEL: "city",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Milieu géographique et social formé par une réunion importante de constructions abritant des habitants qui travaillent, pour la plupart, à l'intérieur de l'agglomération.",
}

PROP_ADDRESS = {
    LABEL: "address",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Adresse d'un bâtiment ou d'une attraction culturelle, patrimoine culturel, musée ou monument.",
}

PROP_POSTCODE = {
    LABEL: "postcode",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Code postal d'un bâtiment ou d'une attraction culturelle, patrimoine culturel, musée ou monument.",
}

PROP_NAME = {
    LABEL: "name",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Nom d'une œuvre, par exemple d'un livre, d'un film, d'un magazine ou d'une œuvre d'art performatif",
}

PROP_PRECISION_ON_PROTECTION = {
    LABEL: "precision_on_the_protection",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Precision sur la protection d'un bien culturel, patrimoine, monument, musée, œuvre d'art, etc.",
}

PROP_DATE_OF_PROTECTION = {
    LABEL: "date_of_protection",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Date à laquelle un bien culturel, patrimoine, monument, musée, œuvre d'art, etc. a été protégé",
}

PROP_HISTORIQUE = {
    LABEL: "historique",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Historique d'un bien culturel, patrimoine, monument, musée, œuvre d'art, etc.",
}

PROP_LOCATION = {
    LABEL: "location",
    TYPE: TYPE_COORDINATE,
    DESCRIPTION: "Emplacement géographique d'un bien culturel, patrimoine, monument, musée, œuvre d'art, etc.",
}

PROP_SIECLE = {
    LABEL: "siecle",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Siècle de création d'un bien culturel, patrimoine, monument, musée, œuvre d'art, etc.",
}

PROP_STATUT = {
    LABEL: "statut",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Statut d'un bien culturel, patrimoine, monument, musée, œuvre d'art, etc.",
}

PROP_CONTACT = {
    LABEL: "contact",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Adresse de contact pour obtenir plus d'informations sur un bien culturel, patrimoine, monument, musée, œuvre d'art, etc.",
}

PROP_PHONE = {
    LABEL: "phone",
    TYPE: TYPE_STRING,
    DESCRIPTION: "Numéro de téléphone pour obtenir plus d'informations sur un bien culturel, patrimoine, monument, musée, œuvre d'art, etc.",
}

PROP_WEBSITE = {
    LABEL: "website",
    TYPE: TYPE_URL,
    DESCRIPTION: "Site web pour obtenir plus d'informations sur un bien culturel, patrimoine, monument, musée, œuvre d'art, etc.",
}
MOD_LIST = [
    "core.sc2mod",
    "liberty.sc2mod",
    "swarm.sc2mod",
    "void.sc2mod",
    "voidprologue.sc2mod",
    "missionpacks/campaigncommon.sc2mod",
    "missionpacks/novacampaign.sc2mod",
    "novastoryassets.sc2mod",
    "starcoop/starcoop.sc2mod",
    "starcoop/commanders/egonstetmann.sc2mod",
    "starcoop/commanders/arcturusmengsk.sc2mod",
    "alliedcommanders.sc2mod",
    "libertymulti.sc2mod",
    "swarmmulti.sc2mod",
    "voidmulti.sc2mod",
    "balancemulti.sc2mod",

]

LANGUAGE_LIST = [
    "enus",
    "dede",
    "eses",
    "esmx",
    "frfr",
    "itit",
    "kokr",
    "plpl",
    "ptbr",
    "ruru",
    "zhcn",
    "zhtw",
]

ID_WHITELIST = [
]

ID_BLACKLIST = [
]
# Only include short texts that are likely to be terms
TERM_ONLY = True 
# If True, allow multiple entries with the same source text. If False, only allow one entry per unique source text and print a warning for duplicates.
ALLOW_DUPLICATE_SOURCE = False 
# The language to use as base reference for the glossary. Should be one of the languages in LANGUAGE_LIST. Only entries with text in the source language will be included in the output glossary.
SOURCE_LANGUAGE = "zhcn" 

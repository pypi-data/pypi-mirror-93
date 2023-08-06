CLI_CONFIG = {
    "beacon_profiles": {"nargs": "*"},
    "format": {},
    # acct options
    "acct_file": {"source": "acct", "os": "ACCT_FILE"},
    "acct_key": {"source": "acct", "os": "ACCT_KEY"},
    # evbus options
    "ingress_profiles": {"source": "evbus"},
    "random": {"source": "evbus", "action": "store_true"},
    # rend options
    "output": {"source": "rend"},
}
CONFIG = {
    "beacon_profiles": {
        "help": "The acct profile names to allowlist.  If none are specified then all profiles will be used",
        "default": [],
    },
    "format": {
        "type": str,
        "help": "The plugin to use for processing data",
        "default": "json",
    },
}
DYNE = {
    "acct": ["acct"],
    "beacon": ["beacon"],
}

CLI_CONFIG = {
    "ingress_profiles": {"nargs": "*"},
    "random": {"action": "store_true"},
    # acct options
    "acct_file": {"source": "acct", "os": "ACCT_FILE"},
    "acct_key": {"source": "acct", "os": "ACCT_KEY"},
    # rend options
    "output": {"source": "rend"},
}
CONFIG = {
    "ingress_profiles": {
        "help": "The acct profile names to allowlist.  If none are specified then all profiles will be used",
        "default": [],
    },
    "random": {
        "help": "Run the random number generator that automatically populates the event bus",
        "default": False,
        "type": bool,
    },
}
SUBCOMMANDS = {}
DYNE = {
    "acct": ["acct"],
    "evbus": ["evbus"],
    "ingress": ["ingress"],
}

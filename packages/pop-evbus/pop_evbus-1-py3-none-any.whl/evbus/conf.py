CLI_CONFIG = {
    "output": {"source": "rend"},
    "acct_file": {"source": "acct", "os": "ACCT_FILE"},
    "acct_key": {"source": "acct", "os": "ACCT_KEY"},
    "ingress_profiles": {"nargs": "*", "options": ["-P"]},
    "random": {"action": "store_true"},
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

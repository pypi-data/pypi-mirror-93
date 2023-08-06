"""
Variables common to main storm commands.
"""
from datetime import date, timedelta

from storm_modules.utils.date_time import date_floor

today = date.today()
last_monday = date_floor(today) - timedelta(days=today.weekday())
last_saturday = today - timedelta(days=today.weekday() + 2)
tomorrow = today + timedelta(days=1)

MAIN_CLI_ARGS = [
    (
        ("--db-uri",),
        {"help": "Database URI"},
    ),
    (
        ("--http-proxy",),
        {"help": "HTTP Proxy"},
    ),
    (
        ("--https-proxy",),
        {"help": "HTTPS Proxy"},
    ),
    (
        ("--ftp-proxy",),
        {"help": "FTP Proxy"},
    ),
    (
        ("--mercure-user",),
        {"help": "Username of Mercure user"},
    ),
    (
        ("--mercure-password",),
        {"help": "Password of Mercure user"},
    ),
    (
        ("--mercure-client-id",),
        {"help": "Mercure client ID"},
    ),
    (
        ("--mercure-client-secret",),
        {"help": "Mercure client secret"},
    ),
    (
        ("--mercure-prod",),
        {"help": "Use production version of mercure ' '(default: false)", "default": False},
    ),
]


COMMON_DB_ARGS = [
    (
        ("--start-date",),
        {"help": "Start date of the run " "(default: last monday)", "default": last_monday},
    ),
    (("--end-date",), {"help": "End date of the run " "(default: start date + 14d)"}),
    (
        ("--now",),
        {"help": "Select date that will be used as " "now", "default": None},
    ),
    (("--nova",), {"action": "store_true", "help": "Use nova_OTC_price.xlsm to rescale prices"}),
    (("--GV",), {"action": "store_true", "help": "Use OTCpricesfromGV.xlsm to rescale prices"}),
    (
        ("--cleared",),
        {"action": "store_true", "help": "Use cleared prices were possible for row countries"},
    ),
    (
        ("--week-ahead",),
        {"type": int, "help": "Number" "of week-ahead scenarios"},
    ),
    (
        ("--long-term",),
        {"type": int, "help": "Number of " "long-term scenarios"},
    ),
    (("--3mv-avail",), {"type": int, "help": "Number" "of availabiltity scenarios"}),
    (
        ("--refresh",),
        {"default": [], "action": "append", "help": "Generate only the selected tabs"},
    ),
    (("--blend-weather",), {"action": "store_true", "help": "blend EC and " "GFS weather models"}),
    (
        ("--day-ahead-view",),
        {"action": "store_true", "help": "Slice horizon day by day", "default": None},
    ),
    (
        ("--day-ahead-now",),
        {
            "type": int,
            "help": "Hour (in local time)" "at which now will be set on each slice of day-ahead",
            "default": 12,
        },
    ),
    (("--no3MVload",), {"action": "store_true", "help": "Slice horizon day by day", "default": None}),
    (
        ("--no-hydro-calib",),
        {
            "action": "store_true",
            "help": "Disable calibration of prices in hydro model",
            "default": None,
        },
    ),
    (
        ("--force-meta",),
        {"help": "Use local meta file"},
    ),
    (
        ("--for",),
        {"help": "Use local file for forced outages"},
    ),
    (("--for-variant",), {"help": "Select variant on forced outages"}),
    (("--addBENL",), {"help": "Add on the load " "(default: start date + 14d)"}),
    (
        ("--module-cache",),
        {"help": "Module cache directory"},
    ),
    (
        ("--keep-module-cache",),
        {
            "action": "store_true",
            "help": "Do not automatically delete " "module cache at the end of the run",
        },
    ),
    (
        ("--mercure-cache",),
        {"help": "Mercure cache directory"},
    ),
    (("--flat-res-capa",), {"action": "store_true", "help": "Force constant value of 1 for RES"}),
]


class CommandModuleWorker:

    string = "run-module"
    arguments = [
        (("--csv",), {"help": "Save result in given csv file", "dest": "csv"}),
        (("--quiet",), {"action": "store_true", "help": "Will not print anything", "dest": "quiet"}),
        (("--port",), {"type": int, "default": 8080, "help": "Local port to connect to"}),
    ]
    arguments.extend(COMMON_DB_ARGS)

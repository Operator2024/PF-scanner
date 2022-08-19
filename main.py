#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import os

__version__ = os.environ["VER"] if os.environ.get("VER") else "0.1.1"

__author__ = "Vladimir Belomestnykh aka Operator2024"

__license__ = "MIT"

import argparse
import json
import sys
from io import BufferedReader
from re import search
from subprocess import PIPE, Popen, check_output
from typing import NoReturn, Optional, Text

import jc


def main(sdr_type: Text = "") -> Optional[NoReturn]:
    storage = dict()
    result = b""
    if sdr_type is None:
        return None
    proc = Popen(
        [
            "ipmitool",
            "sdr",
            "type",
            sdr_type,
        ],
        shell=False,
        stdout=PIPE,
        stderr=PIPE,
    )
    if isinstance(proc.stderr,
                  BufferedReader) and isinstance(proc.stdout, BufferedReader):
        result = proc.stdout.read() + proc.stderr.read()
    if len(result) == 0:
        return None
    if proc.stdout and sdr_type == "Fan":
        for i in result.decode().split("\n"):
            if len(i) > 0:
                SKIP = False
                for idx, val in enumerate(i.split("|")):
                    _name = ""
                    if idx == 0:
                        _name = val.lstrip(" ").rstrip(" ")
                        if "FAN" in _name.upper():
                            if (
                                "FRNT" not in _name.upper()
                                and "REAR" not in _name.upper()
                            ):
                                SKIP = True
                            if len(_name) <= 5 and SKIP is True:
                                SKIP = False
                    elif idx == 1 and SKIP is False:
                        storage[_name] = {"SensorName": val.lstrip(" ").rstrip(" ")}
                    elif idx == 2 and SKIP is False:
                        if val.lstrip(" ").rstrip(" ") == "lnr":
                            storage[_name]["State"] = "Lower Non-Recoverable"
                        elif val.lstrip(" ").rstrip(" ") == "lcr":
                            storage[_name]["State"] = "Lower Critical"
                        elif val.lstrip(" ").rstrip(" ") == "lnc":
                            storage[_name]["State"] = "Lower Non-Critical"
                        elif val.lstrip(" ").rstrip(" ") == "unc":
                            storage[_name]["State"] = "Upper Non-Critical"
                        elif val.lstrip(" ").rstrip(" ") == "ucr":
                            storage[_name]["State"] = "Upper Critical"
                        elif val.lstrip(" ").rstrip(" ") == "unr":
                            storage[_name]["State"] = "Upper Non-Recoverable"
                        else:
                            storage[_name]["State"] = val.lstrip(" ").rstrip(" ")
                    elif idx == 3 and SKIP is False:
                        storage[_name]["Instance"] = val.lstrip(" ").rstrip(" ")
                    elif idx == 4 and SKIP is False:
                        storage[_name]["Speed"] = val.lstrip(" ").rstrip(" ")
    elif proc.stdout and sdr_type == "Power Supply":
        psu_count = -1
        for i in result.decode().split("\n"):
            if len(i) > 0:
                for idx, val in enumerate(i.split("|")):
                    if idx == 0:
                        _match = search(r"(^PS\d|^PSU\d)", val)
                        if _match:
                            if (val[_match.span()[1] - 1].isdigit and psu_count == -1):
                                psu_count = int(val[_match.span()[1] - 1])
                            elif val[_match.span()[1] - 1].isdigit:
                                if int(val[_match.span()[1] - 1]) > psu_count:
                                    psu_count = int(val[_match.span()[1] - 1])
                            else:
                                pass
        storage["PSU_total"] = psu_count
        if sys.version_info < (3, 7):
            cmd_output = check_output(["dmidecode", "-t", "39"])
            psu_additional = jc.parse("dmidecode", cmd_output.decode())
        else:
            cmd_output = check_output(["dmidecode", "-t", "39"], text=True)
            psu_additional = jc.parse("dmidecode", cmd_output)

        if not isinstance(psu_additional, list):
            print(
                "The Variable type 'psu_additional' is different from the type 'list' !"
            )
            return
        if psu_additional and len(psu_additional) == storage["PSU_total"]:
            _psu_counter = 0
            for unit in psu_additional:
                for idx, val in enumerate(unit):
                    if idx == 4 and isinstance(unit[val], dict):
                        if unit[val].get("power_unit_group"):
                            storage[str(unit[val]["power_unit_group"])] = unit[val]
                        else:
                            _psu_counter += 1
                            storage[str(_psu_counter)] = unit[val]
                    else:
                        pass
        else:
            pass
    else:
        pass

    print(json.dumps(storage))


if __name__ == "__main__":
    description = "PSU and Fan inventory system aka PF-checker"
    parser = argparse.ArgumentParser(prog="PF-Checker")
    parser.add_argument(
        "--type",
        "-T",
        type=str,
        nargs=1,
        help=(
            "The type of device you want to get information about (possible:"
            " Fan, Power Supply)"
        ),
    )
    parser.add_argument(
        "--version",
        "-V",
        help="This key allows you to get the current version",
        version=(
            f"{description}, {__license__} license, {__author__}, version:"
            f" {__version__} "
        ),
        action="version",
    )
    args = parser.parse_args()
    if args.type is not None:
        if args.type[0] not in ["Fan", "Power Supply"]:
            print(
                json.dumps({
                    "State": ("Possible values is only ['Fan', 'Power Supply']")
                })
            )
        else:
            main(args.type[0])
    else:
        parser.print_help()

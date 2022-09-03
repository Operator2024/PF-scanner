#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import os

__version__ = os.environ["VER"] if os.environ.get("VER") else "0.1.2"

__author__ = "Vladimir Belomestnykh aka Operator2024"

__license__ = "MIT"

import argparse
import json
import sys
from io import BufferedReader
from re import search
from subprocess import PIPE, Popen, check_output
from typing import Dict, Text, Union

import jc


def main(sdr_type: Text = "") -> Union[Dict, Text, None]:
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
    if proc.stdout and sdr_type == "Fan" and "not open" not in result.decode():
        for i in result.decode().split("\n"):
            if len(i) > 0:
                SKIP = False
                _fname = ""
                for idx, val in enumerate(i.split("|")):
                    if idx == 0:
                        _fname = val.lstrip(" ").rstrip(" ")
                        if "FAN" in _fname.upper():
                            if (
                                "FRNT" not in _fname.upper()
                                and "REAR" not in _fname.upper()
                            ):
                                SKIP = True
                            if len(_fname) <= 5 and SKIP is True:
                                SKIP = False
                    elif idx == 1 and SKIP is False:
                        storage[_fname] = {"SensorName": val.lstrip(" ").rstrip(" ")}
                    elif idx == 2 and SKIP is False:
                        if val.lstrip(" ").rstrip(" ") == "lnr":
                            storage[_fname]["State"] = "Lower Non-Recoverable"
                        elif val.lstrip(" ").rstrip(" ") == "lcr":
                            storage[_fname]["State"] = "Lower Critical"
                        elif val.lstrip(" ").rstrip(" ") == "lnc":
                            storage[_fname]["State"] = "Lower Non-Critical"
                        elif val.lstrip(" ").rstrip(" ") == "unc":
                            storage[_fname]["State"] = "Upper Non-Critical"
                        elif val.lstrip(" ").rstrip(" ") == "ucr":
                            storage[_fname]["State"] = "Upper Critical"
                        elif val.lstrip(" ").rstrip(" ") == "unr":
                            storage[_fname]["State"] = "Upper Non-Recoverable"
                        else:
                            storage[_fname]["State"] = val.lstrip(" ").rstrip(" ")
                    elif idx == 3 and SKIP is False:
                        storage[_fname]["Instance"] = val.lstrip(" ").rstrip(" ")
                    elif idx == 4 and SKIP is False:
                        storage[_fname]["Speed"] = val.lstrip(" ").rstrip(" ")
    elif proc.stdout and sdr_type == "Power Supply" and\
            "not open" not in result.decode():
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
        return result.decode()
    return storage


if __name__ == "__main__":
    _name = "PF-scanner"
    description = f"PSU and Fan inventory system aka {_name}"
    parser = argparse.ArgumentParser(prog=_name)
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
            ret = main(args.type[0])
            if ret:
                print(json.dumps({_name: [ret]}))
    else:
        parser.print_help()

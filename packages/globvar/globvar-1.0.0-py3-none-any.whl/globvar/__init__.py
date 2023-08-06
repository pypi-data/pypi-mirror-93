#!/usr/bin/python3
# -*- coding: utf-8 -*-
__version__ = "1.0.0"
from typing import Any

globals()["_globvar"] = {}


def set(key: str, value: Any, read_only: bool = False) -> None:
    if key in globals()["_globvar"] and globals()["_globvar"][key]["ro"]:
        raise RuntimeError("This value ('%s') is read only!" % key)
    else:
        globals()["_globvar"][key] = {
            "value": value,
            "ro": read_only
        }


def get(key: str) -> Any:
    return globals()["_globvar"].get(key).get("value")

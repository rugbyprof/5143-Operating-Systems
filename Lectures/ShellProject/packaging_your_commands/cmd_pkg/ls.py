#!/usr/bin/env python
import subprocess


def ls(**kwargs):
    """This is my manpage entry for the pwd command"""
    folder = kwargs.get("params", [])
    result = subprocess.run(["ls", "-lah", folder[0]], stdout=subprocess.PIPE)

    return result.stdout.decode("utf-8")

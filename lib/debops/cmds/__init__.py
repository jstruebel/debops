# -*- coding: utf-8 -*-
"""
Support functions for command line utilities (scripts).
"""
# This program is free software; you can redistribute
# it and/or modify it under the terms of the
# GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General
# Public License along with this program; if not,
# write to the Free Software Foundation, Inc., 59
# Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# An on-line copy of the GNU General Public License can
# be downloaded from the FSF web page at:
# http://www.gnu.org/copyleft/gpl.html

from __future__ import print_function

import os
import sys
import platform
import subprocess
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    # open DEVNULL like `subprocess` module does
    DEVNULL = os.open(os.devnull, os.O_RDWR)

from .. import find_debops_project as _find_debops_project, \
    find_playbookpath as _find_playbookpath, \
    find_inventorypath as _find_inventorypath

SCRIPT_NAME = os.path.basename(sys.argv[0])

# Don't check SSH fingerprint on connection (to enable, set INSECURE=1 on the
# command line)
INSECURE = bool(os.environ.get('INSECURE', False))


def error_msg(message, severity="Error"):
    """
    Display error message and exit
    """
    print(SCRIPT_NAME+':', severity+':', message)
    if severity == "Error":
        raise SystemExit(1)

def require_commands(*cmd_names):
    """
    Check if required commands exist.
    """
    def command_exists(cmd_name):
        which = "where" if platform.system() == "Windows" else "which"
        return not subprocess.call([which, cmd_name],
                                   stdout=DEVNULL, stderr=subprocess.STDOUT)

    for name in cmd_names:
        if not command_exists(name):
            error_msg("%s: command not found" % name)


def find_debops_project(path=None, required=True):
    debops_root = _find_debops_project(path)
    if required and not debops_root:
        # Exit if we are outside of project directory
        error_msg("Not a DebOps project directory")
    return debops_root

def find_playbookpath(debops_root, required=True):
    playbooks_path = _find_playbookpath(debops_root)
    if required and not playbooks_path:
        error_msg("DebOps playbooks not installed")
    return playbooks_path

def find_inventorypath(debops_root, required=True):
    inventory = _find_inventorypath(debops_root)
    if required and not inventory:
        error_msg("Ansible inventory not found")
    return inventory

# Copyright (c) 2017 StackHPC Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os
import os.path
import subprocess
import sys

from kayobe import utils
from kayobe import vault


DEFAULT_CONFIG_PATH = "/etc/kolla"

CONFIG_PATH_ENV = "KOLLA_CONFIG_PATH"

DEFAULT_VENV_PATH = "venvs/kolla-ansible"

VENV_PATH_ENV = "KOLLA_VENV_PATH"

LOG = logging.getLogger(__name__)


def add_args(parser):
    """Add arguments required for running Kolla Ansible to a parser."""
    # $KOLLA_CONFIG_PATH or /etc/kolla.
    default_config_path = os.getenv(CONFIG_PATH_ENV, DEFAULT_CONFIG_PATH)
    # $KOLLA_VENV_PATH or $PWD/venvs/kolla-ansible
    default_venv = os.getenv(VENV_PATH_ENV,
                             os.path.join(os.getcwd(), DEFAULT_VENV_PATH))
    parser.add_argument("--kolla-config-path", default=default_config_path,
                        help="path to Kolla configuration. "
                             "(default=$%s or %s)" %
                             (CONFIG_PATH_ENV, DEFAULT_CONFIG_PATH))
    parser.add_argument("-ke", "--kolla-extra-vars", metavar="EXTRA_VARS",
                        action="append",
                        help="set additional variables as key=value or "
                             "YAML/JSON for Kolla Ansible")
    parser.add_argument("-ki", "--kolla-inventory", metavar="INVENTORY",
                        help="specify inventory host path "
                             "(default=$%s/inventory or %s/inventory) or "
                             "comma-separated host list for Kolla Ansible" %
                             (CONFIG_PATH_ENV, DEFAULT_CONFIG_PATH))
    parser.add_argument("-kl", "--kolla-limit", metavar="SUBSET",
                        help="further limit selected hosts to an additional "
                             "pattern")
    parser.add_argument("--kolla-skip-tags", metavar="TAGS",
                        help="only run plays and tasks whose tags do not "
                             "match these values in Kolla Ansible")
    parser.add_argument("-kt", "--kolla-tags", metavar="TAGS",
                        help="only run plays and tasks tagged with these "
                             "values in Kolla Ansible")
    parser.add_argument("--kolla-venv", metavar="VENV", default=default_venv,
                        help="path to virtualenv where Kolla Ansible is "
                             "installed (default=$%s or $PWD/%s)" %
                             (VENV_PATH_ENV, DEFAULT_VENV_PATH))


def _get_inventory_path(parsed_args, inventory_filename):
    """Return the path to the Kolla inventory."""
    if parsed_args.kolla_inventory:
        return parsed_args.kolla_inventory
    else:
        return os.path.join(parsed_args.kolla_config_path, "inventory",
                            inventory_filename)


def _validate_args(parsed_args, inventory_filename):
    """Validate Kayobe Ansible arguments."""
    vault.validate_args(parsed_args)
    result = utils.is_readable_dir(parsed_args.kolla_config_path)
    if not result["result"]:
        LOG.error("Kolla configuration path %s is invalid: %s",
                  parsed_args.kolla_config_path, result["message"])
        sys.exit(1)

    inventory = _get_inventory_path(parsed_args, inventory_filename)
    result = utils.is_readable_dir(parsed_args.kolla_venv)
    if not result["result"]:
        # NOTE(mgoddard): Previously the inventory was a file, now it is a
        # directory to allow us to support inventory host_vars. Support both
        # formats for now.
        result_f = utils.is_readable_file(inventory)
        if not result_f["result"]:
            LOG.error("Kolla inventory %s is invalid: %s",
                      inventory, result["message"])
            sys.exit(1)

    result = utils.is_readable_dir(parsed_args.kolla_venv)
    if not result["result"]:
        LOG.error("Kolla virtualenv %s is invalid: %s",
                  parsed_args.kolla_venv, result["message"])
        sys.exit(1)


def build_args(parsed_args, command, inventory_filename, extra_vars=None,
               tags=None, verbose_level=None, extra_args=None, limit=None):
    """Build arguments required for running Kolla Ansible."""
    venv_activate = os.path.join(parsed_args.kolla_venv, "bin", "activate")
    cmd = [".", venv_activate, "&&"]
    cmd += ["kolla-ansible", command]
    if verbose_level:
        cmd += ["-" + "v" * verbose_level]
    cmd += vault.build_args(parsed_args, "--key")
    inventory = _get_inventory_path(parsed_args, inventory_filename)
    cmd += ["--inventory", inventory]
    if parsed_args.kolla_config_path != DEFAULT_CONFIG_PATH:
        cmd += ["--configdir", parsed_args.kolla_config_path]
        cmd += ["--passwords",
                os.path.join(parsed_args.kolla_config_path, "passwords.yml")]
    if parsed_args.kolla_extra_vars:
        for extra_var in parsed_args.kolla_extra_vars:
            # Don't quote or escape variables passed via the kayobe -e CLI
            # argument, to match Ansible's behaviour.
            cmd += ["-e", extra_var]
    if extra_vars:
        for extra_var_name, extra_var_value in extra_vars.items():
            # Quote and escape variables originating within the python CLI.
            extra_var_value = utils.quote_and_escape(extra_var_value)
            cmd += ["-e", "%s=%s" % (extra_var_name, extra_var_value)]
    if parsed_args.kolla_limit or limit:
        limits = [l for l in [parsed_args.kolla_limit, limit] if l]
        cmd += ["--limit", ":&".join(limits)]
    if parsed_args.kolla_skip_tags:
        cmd += ["--skip-tags", parsed_args.kolla_skip_tags]
    if parsed_args.kolla_tags or tags:
        all_tags = [t for t in [parsed_args.kolla_tags, tags] if t]
        cmd += ["--tags", ",".join(all_tags)]
    if extra_args:
        cmd += extra_args
    return cmd


def run(parsed_args, command, inventory_filename, extra_vars=None,
        tags=None, quiet=False, verbose_level=None, extra_args=None,
        limit=None):
    """Run a Kolla Ansible command."""
    _validate_args(parsed_args, inventory_filename)
    cmd = build_args(parsed_args, command,
                     inventory_filename=inventory_filename,
                     extra_vars=extra_vars, tags=tags,
                     verbose_level=verbose_level,
                     extra_args=extra_args,
                     limit=limit)
    env = os.environ.copy()
    vault.update_environment(parsed_args, env)
    try:
        utils.run_command(" ".join(cmd), quiet=quiet, shell=True, env=env)
    except subprocess.CalledProcessError as e:
        LOG.error("kolla-ansible %s exited %d", command, e.returncode)
        sys.exit(e.returncode)


def run_seed(*args, **kwargs):
    """Run a Kolla Ansible command using the seed inventory."""
    return run(*args, inventory_filename="seed", **kwargs)


def run_overcloud(*args, **kwargs):
    """Run a Kolla Ansible command using the overcloud inventory."""
    return run(*args, inventory_filename="overcloud", **kwargs)

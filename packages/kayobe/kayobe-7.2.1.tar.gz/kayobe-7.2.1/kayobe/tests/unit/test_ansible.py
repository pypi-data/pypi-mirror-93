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

import argparse
import errno
import os
import shutil
import subprocess
import tempfile
import unittest

import mock

from kayobe import ansible
from kayobe import exception
from kayobe import utils
from kayobe import vault


@mock.patch.dict(os.environ, clear=True)
class TestCase(unittest.TestCase):

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    def test_run_playbooks(self, mock_validate, mock_vars, mock_run):
        mock_vars.return_value = ["/etc/kayobe/vars-file1.yml",
                                  "/etc/kayobe/vars-file2.yaml"]
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        parsed_args = parser.parse_args([])
        ansible.run_playbooks(parsed_args, ["playbook1.yml", "playbook2.yml"])
        expected_cmd = [
            "ansible-playbook",
            "--inventory", "/etc/kayobe/inventory",
            "-e", "@/etc/kayobe/vars-file1.yml",
            "-e", "@/etc/kayobe/vars-file2.yaml",
            "playbook1.yml",
            "playbook2.yml",
        ]
        expected_env = {"KAYOBE_CONFIG_PATH": "/etc/kayobe"}
        mock_run.assert_called_once_with(expected_cmd, check_output=False,
                                         quiet=False, env=expected_env)
        mock_vars.assert_called_once_with("/etc/kayobe")

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    def test_run_playbooks_all_the_args(self, mock_validate, mock_vars,
                                        mock_run):
        mock_vars.return_value = ["/path/to/config/vars-file1.yml",
                                  "/path/to/config/vars-file2.yaml"]
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        args = [
            "-b",
            "-C",
            "--config-path", "/path/to/config",
            "-e", "ev_name1=ev_value1",
            "-i", "/path/to/inventory",
            "-l", "group1:host",
            "-t", "tag1,tag2",
            "-lt",
        ]
        parsed_args = parser.parse_args(args)
        ansible.run_playbooks(parsed_args, ["playbook1.yml", "playbook2.yml"],
                              verbose_level=2)
        expected_cmd = [
            "ansible-playbook",
            "-vv",
            "--list-tasks",
            "--inventory", "/path/to/inventory",
            "-e", "@/path/to/config/vars-file1.yml",
            "-e", "@/path/to/config/vars-file2.yaml",
            "-e", "ev_name1=ev_value1",
            "--become",
            "--check",
            "--limit", "group1:host",
            "--tags", "tag1,tag2",
            "playbook1.yml",
            "playbook2.yml",
        ]
        expected_env = {"KAYOBE_CONFIG_PATH": "/path/to/config"}
        mock_run.assert_called_once_with(expected_cmd, check_output=False,
                                         quiet=False, env=expected_env)
        mock_vars.assert_called_once_with("/path/to/config")

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    @mock.patch.object(vault, "_ask_vault_pass")
    def test_run_playbooks_all_the_long_args(self, mock_ask, mock_validate,
                                             mock_vars, mock_run):
        mock_vars.return_value = ["/path/to/config/vars-file1.yml",
                                  "/path/to/config/vars-file2.yaml"]
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        mock_ask.return_value = "test-pass"
        args = [
            "--ask-vault-pass",
            "--become",
            "--check",
            "--config-path", "/path/to/config",
            "--extra-vars", "ev_name1=ev_value1",
            "--inventory", "/path/to/inventory",
            "--limit", "group1:host1",
            "--skip-tags", "tag3,tag4",
            "--tags", "tag1,tag2",
            "--list-tasks",
        ]
        parsed_args = parser.parse_args(args)
        mock_run.return_value = "/path/to/kayobe-vault-password-helper"
        ansible.run_playbooks(parsed_args, ["playbook1.yml", "playbook2.yml"])
        expected_cmd = [
            "ansible-playbook",
            "--list-tasks",
            "--vault-password-file", "/path/to/kayobe-vault-password-helper",
            "--inventory", "/path/to/inventory",
            "-e", "@/path/to/config/vars-file1.yml",
            "-e", "@/path/to/config/vars-file2.yaml",
            "-e", "ev_name1=ev_value1",
            "--become",
            "--check",
            "--limit", "group1:host1",
            "--skip-tags", "tag3,tag4",
            "--tags", "tag1,tag2",
            "playbook1.yml",
            "playbook2.yml",
        ]
        expected_env = {"KAYOBE_CONFIG_PATH": "/path/to/config",
                        "KAYOBE_VAULT_PASSWORD": "test-pass"}
        expected_calls = [
            mock.call(["which", "kayobe-vault-password-helper"],
                      check_output=True, universal_newlines=True),
            mock.call(expected_cmd, check_output=False, quiet=False,
                      env=expected_env)
        ]
        self.assertEqual(expected_calls, mock_run.mock_calls)
        mock_vars.assert_called_once_with("/path/to/config")

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    @mock.patch.object(vault, "update_environment")
    def test_run_playbooks_vault_password_file(self, mock_update,
                                               mock_validate,
                                               mock_vars, mock_run):
        mock_vars.return_value = []
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        args = [
            "--vault-password-file", "/path/to/vault/pw",
        ]
        parsed_args = parser.parse_args(args)
        ansible.run_playbooks(parsed_args, ["playbook1.yml"])
        expected_cmd = [
            "ansible-playbook",
            "--vault-password-file", "/path/to/vault/pw",
            "--inventory", "/etc/kayobe/inventory",
            "playbook1.yml",
        ]
        expected_env = {"KAYOBE_CONFIG_PATH": "/etc/kayobe"}
        mock_run.assert_called_once_with(expected_cmd, check_output=False,
                                         quiet=False, env=expected_env)
        mock_update.assert_called_once_with(mock.ANY, expected_env)

    @mock.patch.dict(os.environ, {"KAYOBE_VAULT_PASSWORD": "test-pass"},
                     clear=True)
    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    def test_run_playbooks_vault_password_helper(self, mock_validate,
                                                 mock_vars, mock_run):
        mock_vars.return_value = []
        parser = argparse.ArgumentParser()
        mock_run.return_value = "/path/to/kayobe-vault-password-helper"
        ansible.add_args(parser)
        vault.add_args(parser)
        mock_run.assert_called_once_with(
            ["which", "kayobe-vault-password-helper"], check_output=True,
            universal_newlines=True)
        mock_run.reset_mock()
        parsed_args = parser.parse_args([])
        ansible.run_playbooks(parsed_args, ["playbook1.yml"])
        expected_cmd = [
            "ansible-playbook",
            "--vault-password-file", "/path/to/kayobe-vault-password-helper",
            "--inventory", "/etc/kayobe/inventory",
            "playbook1.yml",
        ]
        expected_env = {"KAYOBE_CONFIG_PATH": "/etc/kayobe",
                        "KAYOBE_VAULT_PASSWORD": "test-pass"}
        mock_run.assert_called_once_with(expected_cmd, check_output=False,
                                         quiet=False, env=expected_env)

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    def test_run_playbooks_vault_ask_and_file(self, mock_validate, mock_vars,
                                              mock_run):
        mock_vars.return_value = []
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        args = [
            "--ask-vault-pass",
            "--vault-password-file", "/path/to/vault/pw",
        ]
        self.assertRaises(SystemExit, parser.parse_args, args)

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    def test_run_playbooks_func_args(self, mock_validate, mock_vars, mock_run):
        mock_vars.return_value = ["/etc/kayobe/vars-file1.yml",
                                  "/etc/kayobe/vars-file2.yaml"]
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        args = [
            "--extra-vars", "ev_name1=ev_value1",
            "--limit", "group1:host1",
            "--tags", "tag1,tag2",
        ]
        parsed_args = parser.parse_args(args)
        kwargs = {
            "extra_vars": {"ev_name2": "ev_value2"},
            "limit": "group2:host2",
            "tags": "tag3,tag4",
            "verbose_level": 0,
            "check": True,
        }
        ansible.run_playbooks(parsed_args, ["playbook1.yml", "playbook2.yml"],
                              **kwargs)
        expected_cmd = [
            "ansible-playbook",
            "--inventory", "/etc/kayobe/inventory",
            "-e", "@/etc/kayobe/vars-file1.yml",
            "-e", "@/etc/kayobe/vars-file2.yaml",
            "-e", "ev_name1=ev_value1",
            "-e", "ev_name2='ev_value2'",
            "--check",
            "--limit", "group1:host1:&group2:host2",
            "--tags", "tag1,tag2,tag3,tag4",
            "playbook1.yml",
            "playbook2.yml",
        ]
        expected_env = {"KAYOBE_CONFIG_PATH": "/etc/kayobe"}
        mock_run.assert_called_once_with(expected_cmd, check_output=False,
                                         quiet=False, env=expected_env)
        mock_vars.assert_called_once_with("/etc/kayobe")

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    def test_run_playbooks_ignore_limit(self, mock_validate, mock_vars,
                                        mock_run):
        mock_vars.return_value = ["/etc/kayobe/vars-file1.yml",
                                  "/etc/kayobe/vars-file2.yaml"]
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        args = [
            "-l", "group1:host",
        ]
        parsed_args = parser.parse_args(args)
        ansible.run_playbooks(parsed_args, ["playbook1.yml", "playbook2.yml"],
                              limit="foo", ignore_limit=True)
        expected_cmd = [
            "ansible-playbook",
            "--inventory", "/etc/kayobe/inventory",
            "-e", "@/etc/kayobe/vars-file1.yml",
            "-e", "@/etc/kayobe/vars-file2.yaml",
            "playbook1.yml",
            "playbook2.yml",
        ]
        expected_env = {"KAYOBE_CONFIG_PATH": "/etc/kayobe"}
        mock_run.assert_called_once_with(expected_cmd, check_output=False,
                                         quiet=False, env=expected_env)
        mock_vars.assert_called_once_with("/etc/kayobe")

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    def test_run_playbooks_list_tasks_arg(self, mock_validate, mock_vars,
                                          mock_run):
        mock_vars.return_value = []
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        args = [
            "--list-tasks",
        ]
        parsed_args = parser.parse_args(args)
        kwargs = {
            "list_tasks": False
        }
        ansible.run_playbooks(parsed_args, ["playbook1.yml", "playbook2.yml"],
                              **kwargs)
        expected_cmd = [
            "ansible-playbook",
            "--inventory", "/etc/kayobe/inventory",
            "playbook1.yml",
            "playbook2.yml",
        ]
        expected_env = {"KAYOBE_CONFIG_PATH": "/etc/kayobe"}
        mock_run.assert_called_once_with(expected_cmd, check_output=False,
                                         quiet=False, env=expected_env)
        mock_vars.assert_called_once_with("/etc/kayobe")

    @mock.patch.object(utils, "run_command")
    @mock.patch.object(ansible, "_get_vars_files")
    @mock.patch.object(ansible, "_validate_args")
    def test_run_playbooks_failure(self, mock_validate, mock_vars, mock_run):
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        vault.add_args(parser)
        parsed_args = parser.parse_args([])
        mock_run.side_effect = subprocess.CalledProcessError(1, "dummy")
        self.assertRaises(SystemExit,
                          ansible.run_playbooks, parsed_args, ["command"])

    @mock.patch.object(shutil, 'rmtree')
    @mock.patch.object(utils, 'read_yaml_file')
    @mock.patch.object(os, 'listdir')
    @mock.patch.object(ansible, 'run_playbook')
    @mock.patch.object(tempfile, 'mkdtemp')
    def test_config_dump(self, mock_mkdtemp, mock_run, mock_listdir, mock_read,
                         mock_rmtree):
        parser = argparse.ArgumentParser()
        parsed_args = parser.parse_args([])
        dump_dir = "/path/to/dump"
        mock_mkdtemp.return_value = dump_dir
        mock_listdir.return_value = ["host1.yml", "host2.yml"]
        mock_read.side_effect = [
            {"var1": "value1"},
            {"var2": "value2"}
        ]
        result = ansible.config_dump(parsed_args)
        expected_result = {
            "host1": {"var1": "value1"},
            "host2": {"var2": "value2"},
        }
        self.assertEqual(result, expected_result)
        dump_config_path = utils.get_data_files_path(
            "ansible", "dump-config.yml")
        mock_run.assert_called_once_with(parsed_args,
                                         dump_config_path,
                                         extra_vars={
                                             "dump_path": dump_dir,
                                         },
                                         check_output=True, tags=None,
                                         verbose_level=None, check=False,
                                         list_tasks=False)
        mock_rmtree.assert_called_once_with(dump_dir)
        mock_listdir.assert_any_call(dump_dir)
        mock_read.assert_has_calls([
            mock.call(os.path.join(dump_dir, "host1.yml")),
            mock.call(os.path.join(dump_dir, "host2.yml")),
        ])

    @mock.patch.object(utils, 'galaxy_install', autospec=True)
    @mock.patch.object(utils, 'is_readable_file', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test_install_galaxy_roles(self, mock_mkdirs, mock_is_readable,
                                  mock_install):
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        parsed_args = parser.parse_args([])
        mock_is_readable.return_value = {"result": False}

        ansible.install_galaxy_roles(parsed_args)

        mock_install.assert_called_once_with(utils.get_data_files_path(
            "requirements.yml"), utils.get_data_files_path(
            "ansible", "roles"), force=False)
        mock_is_readable.assert_called_once_with(
            "/etc/kayobe/ansible/requirements.yml")
        self.assertFalse(mock_mkdirs.called)

    @mock.patch.object(utils, 'galaxy_install', autospec=True)
    @mock.patch.object(utils, 'is_readable_file', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test_install_galaxy_roles_with_kayobe_config(
            self, mock_mkdirs, mock_is_readable, mock_install):
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        parsed_args = parser.parse_args([])
        mock_is_readable.return_value = {"result": True}

        ansible.install_galaxy_roles(parsed_args)

        expected_calls = [
            mock.call(utils.get_data_files_path("requirements.yml"),
                      utils.get_data_files_path("ansible", "roles"),
                      force=False),
            mock.call("/etc/kayobe/ansible/requirements.yml",
                      "/etc/kayobe/ansible/roles", force=False)]
        self.assertEqual(expected_calls, mock_install.call_args_list)
        mock_is_readable.assert_called_once_with(
            "/etc/kayobe/ansible/requirements.yml")
        mock_mkdirs.assert_called_once_with("/etc/kayobe/ansible/roles")

    @mock.patch.object(utils, 'galaxy_install', autospec=True)
    @mock.patch.object(utils, 'is_readable_file', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test_install_galaxy_roles_with_kayobe_config_forced(
            self, mock_mkdirs, mock_is_readable, mock_install):
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        parsed_args = parser.parse_args([])
        mock_is_readable.return_value = {"result": True}

        ansible.install_galaxy_roles(parsed_args, force=True)

        expected_calls = [
            mock.call(utils.get_data_files_path("requirements.yml"),
                      utils.get_data_files_path("ansible", "roles"),
                      force=True),
            mock.call("/etc/kayobe/ansible/requirements.yml",
                      "/etc/kayobe/ansible/roles", force=True)]
        self.assertEqual(expected_calls, mock_install.call_args_list)
        mock_is_readable.assert_called_once_with(
            "/etc/kayobe/ansible/requirements.yml")
        mock_mkdirs.assert_called_once_with("/etc/kayobe/ansible/roles")

    @mock.patch.object(utils, 'galaxy_install', autospec=True)
    @mock.patch.object(utils, 'is_readable_file', autospec=True)
    @mock.patch.object(os, 'makedirs', autospec=True)
    def test_install_galaxy_roles_with_kayobe_config_mkdirs_failure(
            self, mock_mkdirs, mock_is_readable, mock_install):
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        parsed_args = parser.parse_args([])
        mock_is_readable.return_value = {"result": True}
        mock_mkdirs.side_effect = OSError(errno.EPERM)

        self.assertRaises(exception.Error,
                          ansible.install_galaxy_roles, parsed_args)

        mock_install.assert_called_once_with(utils.get_data_files_path(
            "requirements.yml"), utils.get_data_files_path("ansible", "roles"),
            force=False)
        mock_is_readable.assert_called_once_with(
            "/etc/kayobe/ansible/requirements.yml")
        mock_mkdirs.assert_called_once_with("/etc/kayobe/ansible/roles")

    @mock.patch.object(utils, 'galaxy_remove', autospec=True)
    def test_prune_galaxy_roles(self, mock_remove):
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        parsed_args = parser.parse_args([])

        ansible.prune_galaxy_roles(parsed_args)

        expected_roles = [
            'stackhpc.os-shade',
        ]
        mock_remove.assert_called_once_with(expected_roles,
                                            "ansible/roles")

    @mock.patch.object(utils, 'is_readable_file', autospec=True)
    def test_passwords_yml_exists_false(self, mock_is_readable):
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        parsed_args = parser.parse_args([])
        mock_is_readable.return_value = {"result": False}

        result = ansible.passwords_yml_exists(parsed_args)

        self.assertFalse(result)
        mock_is_readable.assert_called_once_with(
            "/etc/kayobe/kolla/passwords.yml")

    @mock.patch.object(utils, 'is_readable_file', autospec=True)
    def test_passwords_yml_exists_true(self, mock_is_readable):
        parser = argparse.ArgumentParser()
        ansible.add_args(parser)
        parsed_args = parser.parse_args(["--config-path", "/path/to/config"])
        mock_is_readable.return_value = {"result": True}

        result = ansible.passwords_yml_exists(parsed_args)

        self.assertTrue(result)
        mock_is_readable.assert_called_once_with(
            "/path/to/config/kolla/passwords.yml")

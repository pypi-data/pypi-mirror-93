#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--
# ansible-roles-ctl, manage installation and upgrade of Ansible roles
# Copyright (C) 2016-2020  Marc Dequènes (Duck)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#++
# You can find the code here: https://gitlab.com/osas/ansible-roles-ctl

VERSION = "1.2.0"


# PYTHON_ARGCOMPLETE_OK
import argcomplete,argparse
from argcomplete.completers import ChoicesCompleter, SuppressCompleter
import yaml
import os.path
import re
import shutil
import time
import ansible.constants as C
from ansible import context
from ansible.galaxy import Galaxy
from ansible.playbook.role.requirement import RoleRequirement
from ansible.galaxy.role import GalaxyRole
import git
from git import Repo,Commit
from git.exc import GitCommandError
import ansible.release
from pkg_resources import parse_version
from pathlib import Path


# GitPython path parameter was broken
if parse_version(git.__version__) >= parse_version("3.1.10"):
    # used to ignore leftover from Galaxy installation
    GITPYTHON_DIRTY_PATHSPEC = ":!meta/.galaxy_install_info"
else:
    GITPYTHON_DIRTY_PATHSPEC = None


class AnsibleRolesCtlException(Exception):
    """AnsibleRolesCtl exceptions"""

class InvalidAnsibleRole(AnsibleRolesCtlException):
    """Ansible role is in an unusable state"""

class NonExistingAnsibleRoleTarget(AnsibleRolesCtlException):
    """Ansible role is setup to target a non-existing tag or branch"""

class ReqOffAnsibleRole(AnsibleRolesCtlException):
    """Ansible role is setup to target a non-existing tag or branch"""

# reusing default options from the CLI.
# there is no way to get them properly because it is merged with the
# CLI parser.
class GalaxyDefaultOptions:
    def __init__(self):
        self.ignore_certs = C.GALAXY_IGNORE_CERTS
        self.roles_path = C.DEFAULT_ROLES_PATH
        if parse_version(ansible.release.__version__) >= parse_version("2.9.0"):
            # we do not support collections yet
            self.type = 'role'

# reusing GalaxyRole initialization to obtain name and path properly
class AnsibleRole(GalaxyRole):

    tag_version_regex = "^v?(?P<version>\d+\.\d+(\.\d+)?)$"

    def __init__(self, **role):
        if parse_version(ansible.release.__version__) >= parse_version("2.8.0"):
            context._init_global_context(GalaxyDefaultOptions())
            galaxy = Galaxy()
        else:
            galaxy = Galaxy(GalaxyDefaultOptions())
        if parse_version(ansible.release.__version__) >= parse_version("2.9.0"):
            super(AnsibleRole, self).__init__(galaxy, None, **role)
        else:
            super(AnsibleRole, self).__init__(galaxy, **role)

        self.repo = None
        if self.isInstalled():
            try:
                self.repo = Repo(self.path)
            except Exception as e:
                pass

        # if no version specified, then master is considered default
        if not self.version:
            self.version = 'master'

    def isInstalled(self):
        return os.path.exists(self.path)

    def localBranch(self):
        if self.repo.head.is_detached:
            return None

        return self.repo.head.reference

    def localVersion(self):
        try:
            return self.versionTags()[self.repo.head.commit]
        except:
            return None

    def remoteBranch(self):
        if self.repo.head.is_detached:
            return None

        # used configured tracking branch if exist
        branch = self.localBranch().tracking_branch()
        if branch:
            return branch

        # or try a matching branch name in 'origin' remote
        if self.localBranch().name in self.repo.remotes.origin.refs:
            ref = self.repo.remotes.origin.refs[self.localBranch().name]
            self.localBranch().set_tracking_branch(ref)
            print("role '{}' lacked tracking branch configuration, fixed".format(self.name))
            return ref

        return None

    def isTargetingVersionTag(self):
        if re.match(self.tag_version_regex, self.version):
            return True
        else:
            return False

    def testValid(self):
        if self.scm and self.scm != 'git':
            raise InvalidAnsibleRole("using an unsupported SCM")
        if not (self.scm or re.search("https?://", self.src)):
            raise InvalidAnsibleRole("{} from Ansible Galaxy".format(self.src))

        # if role is not installed yet, then skip following tests
        if not self.isInstalled():
            return

        if not self.repo:
            raise InvalidAnsibleRole("not a valid SCM directory")
        if self.repo.bare:
            raise InvalidAnsibleRole("bare repository")
        if self.localBranch() is not None and self.remoteBranch() is None:
            raise InvalidAnsibleRole("on a local branch '{}' (no corresponding remote branch)".format(self.localBranch().name))

        self.version_commit = None
        if self.isTargetingVersionTag():
            try:
                self.version_commit = self.repo.tags[self.version].commit
            except ValueError as e:
                raise NonExistingAnsibleRoleTarget("targeting an unexisting version ({})".format(self.version))

        return

    def testRequirements(self):
        if self.isTargetingVersionTag():
            if self.repo.head.commit != self.version_commit:
                version = self.localVersion()
                if version:
                    raise ReqOffAnsibleRole("on version '{}' but not the requirements (version '{}')".format(version, self.version))
                elif self.localBranch() is not None:
                    raise ReqOffAnsibleRole("on branch '{}' but not the requirements (version '{}')".format(self.localBranch().name, self.version))
                else:
                    raise ReqOffAnsibleRole("on a detached commit but not the requirements (version '{}')".format(self.version))

        elif self.localBranch() is None:
            version = self.localVersion()
            if version:
                raise ReqOffAnsibleRole("on version '{}' but not the requirements (branch '{}')".format(version, self.version))
            else:
                raise ReqOffAnsibleRole("on a detached commit but not the requirements (branch '{}')".format(self.version))

        elif self.localBranch().name != self.version:
            raise ReqOffAnsibleRole("on branch '{}' but not the requirements (branch '{}')".format(self.localBranch().name, self.version))

    def fetchUpdates(self):
        self.repo.remotes.origin.fetch()

    def commitsAhead(self):
        if self.repo.head.is_detached:
            return []

        if self.remoteBranch().is_valid():
            return Commit.iter_items(self.repo, "{}..HEAD".format(self.remoteBranch()))
        else:
            return Commit.iter_items(self.repo, "HEAD")

    def commitsBehind(self):
        if self.repo.head.is_detached:
            return []

        if self.remoteBranch().is_valid():
            return Commit.iter_items(self.repo, "HEAD..{}".format(self.remoteBranch()))
        else:
            return []

    def versionTags(self):
        list = {}
        for t in self.repo.tags:
            m = re.match(self.tag_version_regex, t.name)
            if m:
                #list[t.commit.hexsha] = m.group('version')
                list[t.commit] = m.group('version')
        return list

    def newVersions(self):
        if self.localBranch() is not None:
            all_tags = self.versionTags()

            new_versions = []
            for commit in self.commitsBehind():
                if commit in all_tags:
                    new_versions.append(all_tags[commit])
            return sorted(new_versions)

        version = self.localVersion()
        if version:
            return sorted([x for x in self.versionTags().values() if x > version])

        return []

    def hasRemoteBranch(self, branch):
        try:
            self.repo.remotes.origin.refs[branch]
            return True
        except Exception as e:
            return False

    def trackRemoteBranch(self, branch):
        if branch not in self.repo.refs:
            self.repo.create_head(branch, self.repo.remotes.origin.refs[branch])
        self.repo.heads[branch].set_tracking_branch(self.repo.remotes.origin.refs[branch])
        self.repo.heads[branch].checkout()

    def uninstall(self):
        if not self.isInstalled():
            return

        shutil.rmtree(self.path)

    def install(self):
        if self.isInstalled():
            return False

        self.repo = Repo.clone_from(self.src, self.path)

        # newly created empty repository
        if not self.repo.remotes.origin.refs:
            return True

        if self.isTargetingVersionTag():
            if self.version in self.repo.tags:
                self.repo.tags[self.version].checkout
            else:
                self.uninstall()
                raise NonExistingAnsibleRoleTarget("setup to target version '{}', but it does not exist".format(self.version))

        else:
            if self.hasRemoteBranch(self.version):
                self.trackRemoteBranch(self.version)
            else:
                self.uninstall()
                raise NonExistingAnsibleRoleTarget("setup to follow branch '{}', but it does not exist".format(self.version))

        return True

    def update(self, new_target_version=None):
        if not self.isInstalled():
            raise InvalidAnsibleRole("not yet installed")

        if self.repo.is_dirty(untracked_files=True, path=GITPYTHON_DIRTY_PATHSPEC):
            raise InvalidAnsibleRole("has local changes (please commit, stash or cleanup)")

        self.fetchUpdates()
        try:
            self.fetchUpdates()
        except GitCommandError as e:
            raise InvalidAnsibleRole("has problems fetching updates: {}".format(e))

        new_target_tag = None

        if new_target_version:
            new_target_tag = "v{}".format(new_target_version)
            if new_target_tag not in self.repo.tags:
                raise NonExistingAnsibleRoleTarget("cannot be upgraded to nonexisting version '{}'".format(new_target_version))

        elif self.isTargetingVersionTag():
            all_tags = self.versionTags()
            for commit in self.commitsBehind():
                if commit in all_tags:
                    new_target_version = all_tags[commit]

            if not new_target_version:
                return False

            new_target_tag = "v{}".format(new_target_version)

        if new_target_tag:
            # already at target
            if self.repo.tags[new_target_tag].commit == self.repo.head.reference.commit:
                return False

            self.repo.head.reference = new_target_tag
            self.repo.head.reset(index=True, working_tree=True)
            self.version = new_target_tag

        else:
            updated = False

            # if not on the right branch, then switch
            if self.localBranch().name != self.version:
                self.trackRemoteBranch(self.version)
                updated = True

            la = list(self.commitsAhead())
            lb = list(self.commitsBehind())

            if la and lb:
                raise NonExistingAnsibleRoleTarget("has diverged from origin")

            if la:
                raise NonExistingAnsibleRoleTarget("is ahead origin")

            # already at target
            if not lb:
                return updated

            self.repo.remotes.origin.pull()

        return True

# errors deferred for completion, returning None instead
def load_roles_info():
    try:
        stream = open("requirements.yml", "r")
    except Exception as e:
        print("Unable to open requirements file")
        return None

    try:
        required_roles = yaml.safe_load(stream)
    except Exception as e:
        print("Unable to load data from the requirements file")
        return None

    if required_roles is None:
        print("No roles found in requirements file")
        return None

    roles_info_list = {}
    for dep in required_roles:
        role_info = RoleRequirement.role_yaml_parse(dep)
        roles_info_list[role_info['name']] = role_info

    return roles_info_list

def load_roles(args, roles_info_list, selected_roles):
    role_list = {}
    for role_info in roles_info_list.values():
        if selected_roles and role_info['name'] not in selected_roles:
            continue

        role = AnsibleRole(**role_info)

        try:
            role.testValid()
        except InvalidAnsibleRole as e:
            if not args.quiet:
                print("role '{}' is invalid: {}".format(role.name, e))
            continue

        role_list[role.name] = role

    return role_list

def display_changelog(commit, new_versions):
    try:
        changelog = commit.tree['CHANGELOG.yml']
    except Exception as e:
        print("  no changelog file ('CHANGELOG.yml') could be found")
        return

    try:
        changelog_entries = yaml.safe_load(changelog.data_stream)
    except Exception as e:
        print("  changelog file ('CHANGELOG.yml') could not be parsed")
        return

    print("  changelog:")
    for version in sorted(new_versions):
        if version in changelog_entries:
            print("    {}:".format(version))
            for entry in changelog_entries[version]:
                print("      - {}".format(entry))
        else:
            print("    {}: changelog entry is missing for this version".format(version))

def action_status(dep_list, selected_roles, args):
    ret_ok = True

    for role_name in sorted(dep_list.keys()):
        if selected_roles and role_name not in selected_roles:
            continue

        role = dep_list[role_name]

        if not role.isInstalled():
            ret_ok = False
            print("role '{}' is not installed".format(role.name))
            continue

        if role.repo.remotes.origin.url != role.src:
            print("role '{}' is installed but does not track the expected origin (current: {}, expected: {})".format(role.name, role.repo.remotes.origin.url, role.src))
            continue

        try:
            role.fetchUpdates()
        except GitCommandError as e:
            ret_ok = False
            print("role '{}' has problems fetching updates: {}".format(role.name, e))
            continue

        warning_msg = False
        type = "version" if role.isTargetingVersionTag() else "branch"
        msg = "role '{}' is properly installed, targeting {} '{}'".format(role.name, type, role.version)

        try:
            role.testRequirements()
        except Exception as e:
            warning_msg = True
            ret_ok = False
            msg += "\n  is off target: {}".format(e)

        if role.localBranch() is not None and role.remoteBranch().is_valid():
            if role.localBranch().commit == role.remoteBranch().commit:
                msg += "\n  is up-to-date with origin"

            else:
                warning_msg = True
                ret_ok = False
                la = list(role.commitsAhead())
                lb = list(role.commitsBehind())
                if la and lb:
                    msg += "\n  has diverged from origin"
                elif la:
                    msg += "\n  is {} commits ahead origin".format(len(la))
                    if args.changelog:
                        for commit in la:
                            msg += "\n    {}:  {}".format(time.strftime("%Y-%m-%d %H:%M %Z", time.gmtime(commit.committed_date)), commit.summary)
                elif lb:
                    msg += "\n  is {} commits behind origin:".format(len(lb))
                    if args.changelog:
                        for commit in lb:
                            msg += "\n    {}:  {}".format(time.strftime("%Y-%m-%d %H:%M %Z", time.gmtime(commit.committed_date)), commit.summary)

                new_versions = role.newVersions()
                if new_versions:
                    warning_msg = True
                    msg += "\n  has new version(s) available: {}".format(", ".join(new_versions))
                    if args.changelog:
                        commit = role.repo.tags["v{}".format(new_versions[-1])]
                        display_changelog(commit, new_versions)

        if role.localBranch() is not None and not role.remoteBranch().is_valid():
            la = list(role.commitsAhead())
            if (la):
                warning_msg = True
                msg += "\n  is {} commits ahead (empty) origin".format(len(la))
                if args.changelog:
                    for commit in la:
                        msg += "\n    {}:  {}".format(time.strftime("%Y-%m-%d %H:%M %Z", time.gmtime(commit.committed_date)), commit.summary)

        if role.repo.is_dirty(untracked_files=True, path=GITPYTHON_DIRTY_PATHSPEC):
            warning_msg = True
            msg += "\n  contains local changes (please commit, stash or cleanup)".format(role.name)

        if selected_roles or warning_msg or not args.quiet:
            print(msg)

    return 0 if ret_ok else -1

def action_install(dep_list, selected_roles, args):
    for role_name in sorted(dep_list.keys()):
        if selected_roles and role_name not in selected_roles:
            continue

        role = dep_list[role_name]

        try:
            if role.install():
                print("role '{}' has been installed".format(role.name))
                if not role.repo.remotes.origin.refs:
                    print("  is an empty repository")
            else:
                if not args.quiet:
                    print("role '{}' is already installed".format(role.name))
        except Exception as e:
            print("role '{}' installation failed: {}".format(role.name, e))

def update_requirements(dep_list):
    req_list = []
    for role_name in sorted(dep_list.keys()):
        role = dep_list[role_name]
        req_list.append(role.spec)

    with open("requirements.yml", 'w') as f:
        yaml.safe_dump(req_list, f, default_flow_style=False)

def action_update(dep_list, selected_roles, args):
    selected_versions = {}
    for role_name in args.roles:
        l = role_name.split("=")
        if len(l) > 1:
            selected_versions[l[0]] = l[1]

    req_file_needs_update = False

    for role_name in sorted(dep_list.keys()):
        if selected_roles and role_name not in selected_roles:
            continue

        role = dep_list[role_name]

        new_target_version = None
        if role.name in selected_versions:
            new_target_version = selected_versions[role.name]

        try:
            if role.update(new_target_version):
                req_file_needs_update = True
                print("role '{}' has been updated".format(role.name))
            else:
                if not args.quiet:
                    print("role '{}' is already updated to target".format(role.name))
        except Exception as e:
            print("role '{}' update failed: {}".format(role.name, e))

    if req_file_needs_update and args.req_update:
        update_requirements(dep_list)
        if not args.quiet:
            print("requirements file has been updated, please check before commiting")


if __name__ == "__main__":
    roles_info_list = load_roles_info()

    if roles_info_list:
        roles_names = list(roles_info_list.keys())
    else:
        roles_names = []
    # work around https://bugs.python.org/issue27227
    #             https://bugs.python.org/issue9625
    # by adding the empty list to the list of choices
    roles_names.append([])

    # declare available subcommands and options
    parser = argparse.ArgumentParser(description='Manage roles installation')
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(VERSION))
    parser.add_argument('--quiet', '-q', action='store_true', help='less verbose display')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_status = subparsers.add_parser('status', help='inform about roles installation status')
    parser_status.set_defaults(func=action_status)
    parser_status.add_argument('--changelog', '-c', action='store_true', help='display changelog entries for new versions')
    parser_status.add_argument('roles', nargs='*', choices=roles_names, help='limit command to this list of roles')
    parser_install = subparsers.add_parser('install', help='install roles')
    parser_install.set_defaults(func=action_install)
    parser_install.add_argument('roles', nargs='*', choices=roles_names, help='limit command to this list of roles')
    parser_update = subparsers.add_parser('update', help='update roles')
    parser_update.set_defaults(func=action_update)
    parser_update.add_argument('--req-update', '-r', action='store_true', help='update requirements file')
    parser_update.add_argument('roles', nargs='*', choices=roles_names, help='limit command to this list of roles; "role=<version>" syntax is possible to enforce a specific version')

    # Completion
    argcomplete.autocomplete(parser)

    # deferred for completion
    if not roles_info_list:
        exit(-1)

    # let's parse
    args = parser.parse_args()

    # load user config
    selected_roles = []
    if hasattr(args, 'roles'):
        selected_roles = list(map(lambda i: i.split("=")[0], args.roles))
    dep_list = load_roles(args, roles_info_list, selected_roles)

    # action!
    if hasattr(args, 'func'):
        exit(args.func(dep_list, selected_roles, args))
    else:
        parser.print_help()


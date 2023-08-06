# -*- coding: utf-8 -*-

# Copyright (C) 2019  Marcus Rickert
#
# See https://github.com/marcus67/python_base_app
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import pwd

from python_base_app import base_user_handler
from python_base_app import configuration

SECTION_NAME = "UnixUserHandler"

HANDLER_NAME = "unix"

DEFAULT_MIN_UID = 500
DEFAULT_MAX_UID = 65000
INVALID_SHELLS = ["/usr/sbin/nologin", "/bin/false"]


class BaseUserHandlerConfigModel(configuration.ConfigModel):

    def __init__(self):
        super().__init__(p_section_name=SECTION_NAME)
        self.admin_username = configuration.NONE_STRING
        self.admin_password = configuration.NONE_STRING
        self.user_list = configuration.NONE_STRING
        self.min_uid = DEFAULT_MIN_UID
        self.max_uid = DEFAULT_MAX_UID

    def is_active(self):
        return self.admin_username is not None and self.admin_password is not None


class UnixUserHandler(base_user_handler.BaseUserHandler):

    def __init__(self, p_config, p_exclude_user_list=None):

        super().__init__()

        self._config = p_config
        self._users = None
        self._exclude_user_list = p_exclude_user_list

        if self._exclude_user_list is None:
            self._exclude_user_list = []

        msg = "Using admin user '{username}'"
        self._logger.info(msg.format(username=self._config.admin_username))

        if self._config.user_list is not None:
            try:
                self._users = {name_uid.split(":")[0].strip(): int(name_uid.split(":")[1]) for name_uid in
                               self._config.user_list.split(",")}

            except Exception as e:
                msg = "Invalid user:uid list '{list}' in [UnixUserHandler].user_list"
                raise configuration.ConfigurationException(msg.format(list=self._config.user_list))

            msg = "Using predefined users {users}"
            self._logger.info(msg.format(users=",".join(self._users.keys())))

    def list_users(self):

        users = []

        if self._users is None:
            for entry in pwd.getpwall():
                if (entry.pw_uid >= self._config.min_uid and
                        entry.pw_uid <= self._config.max_uid and
                        entry.pw_passwd != "" and entry.pw_passwd is not None and
                        entry.pw_shell not in INVALID_SHELLS and
                        entry.pw_name not in self._exclude_user_list):
                    users.append(entry.pw_name)

            return users

        else:
            return self._users.keys()

    def get_uid(self, p_username):

        if self._users is None:
            try:
                user = pwd.getpwnam(p_username)

                if user is not None:
                    return user.pw_uid

            except KeyError:
                pass

        else:
            return self._users.get(p_username)

        return None

    def authenticate(self, p_username, p_password):

        return p_username == self._config.admin_username and p_password == self._config.admin_password

    def is_admin(self, p_username):

        return self._config.admin_username == p_username

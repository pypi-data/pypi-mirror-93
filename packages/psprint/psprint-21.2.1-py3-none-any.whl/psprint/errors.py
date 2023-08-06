#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Errors and warnings
'''


class KeyWarning(Warning):
    '''
    Warning that a key was wrongly passed and has been interpreted as default
    '''


class ValueWarning(Warning):
    '''
    Warning that a value was wrongly passed and has been interpreted as default
    '''


class BadMark(Exception):
    '''
    Error that a ``mark`` supplied in ``config`` cannot be parsed

    Args:
        mark: passed mark
        config: config file that defined the mark
    '''
    def __init__(self, mark: str, config: str) -> None:
        super().__init__(f'''
        Prefix-mark {mark} from {config} couldn't be parsed
        ''')

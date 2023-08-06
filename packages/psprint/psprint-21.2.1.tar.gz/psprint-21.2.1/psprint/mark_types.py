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
# GNU Lesser General Public License for more details. #
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Information Marker

'''

import os
import typing
import warnings
from colorama import Fore, Back, Style
import yaml
from .errors import KeyWarning, ValueWarning
from .text_types import PrintPref, PrintText


DEFAULT_STYLE = {'color': 7, 'gloss': 1, 'bgcol': 0}
'''
Default Styles: white color, normal Gloss, black background
'''
AVAIL_GLOSS = [Style.RESET_ALL, Style.NORMAL, Style.DIM, Style.BRIGHT]
'''
Gloss for easy referencing: 0: reset_all, 1: normal, 2: dim, 3: bright
'''
FORE_COLORS = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
               Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
               Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
               Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
               Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]
'''
Colors for easy referencing:
0: Black, 1: Red, 2: Green, 3: Yellow, 4: Blue, 5: Magenta, 6: Cyan, 7: White
Light-: 7 + `above`
'''
BACK_COLORS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW,
               Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE,
               Back.LIGHTBLACK_EX, Back.LIGHTRED_EX, Back.LIGHTGREEN_EX,
               Back.LIGHTYELLOW_EX, Back.LIGHTBLUE_EX, Back.LIGHTMAGENTA_EX,
               Back.LIGHTCYAN_EX, Back.LIGHTWHITE_EX]
'''
Background colors for easy referencing:
0: Black, 1: Red, 2: Green, 3: Yellow, 4: Blue, 5: Magenta, 6: Cyan, 7: White
Light-: 7 + `above`
'''

with open(os.path.join(os.path.dirname(__file__), "codes.yml"), "r") as stream:
    _INDICES = yaml.safe_load(stream)

COLOR_INDICES: typing.List[list] = _INDICES['color_indices']
'''
Aliases for colors: red = 1 = r, green = 2 = g, etc [loaded from codes.yml]
'''
GLOSS_INDICES: typing.List[list] = _INDICES['gloss_indices']
'''
Aliases for gloss: dim = 2 = d, etc [loaded from codes.yml]
'''
PREF_MAX_LEN: int = _INDICES['pref_max_len']
'''
Maximum length of prefix. Prefix is padded to this length if called.
'''


class InfoMark():
    '''
    Prefix Mark information

    Attributes:
        pref: PrintPref: Prefix text properties
        text: PrintText: Text properties

    Args:
        parent: Inherit information from-
        pref: Message-description prefix
        pref_s: Short-description (1 character-long)
        pad_to: pad prefix to reach length
        pref_args: dict with keys: color, gloss, bgcol
        text_args: dict with keys: color, gloss, bgcol

    '''
    def __init__(self,
                 parent: 'InfoMark' = None,
                 pref: str = '',
                 pref_s: str = '>',
                 text_args: dict = {},
                 pref_args: dict = {},) -> None:
        # Standards check
        if len(pref) > PREF_MAX_LEN:
            trim = pref[:PREF_MAX_LEN]
            warnings.warn(
                f"Prefix string '{pref}'" +
                f" is too long (length>{PREF_MAX_LEN}) " +
                f"trimming to {trim}",
                category=ValueWarning
            )
            pref = trim

        if len(pref_s) > 1:
            trim = pref_s[:1]
            warnings.warn(
                "Prefix string '{pref_s}'" +
                f" is too long (length>1) trimming to {trim}",
                category=ValueWarning
            )
            pref_s = trim

        # Styles
        # inheritance:
        # Order of importance: kwargs ELSE parent ELSE default
        if parent is not None:
            pref_args = {**DEFAULT_STYLE,
                         **parent.pref.style_kwargs,
                         **pref_args}
            text_args = {**DEFAULT_STYLE,
                         **parent.text.style_kwargs,
                         **text_args}
            pref = pref or parent.pref.val
            pref_s = pref_s if pref_s != ">" else parent.pref.short
        else:
            pref_args = {**DEFAULT_STYLE, **pref_args}
            text_args = {**DEFAULT_STYLE, **text_args}

        self.pref = PrintPref(val=pref, short=pref_s, pad_to=PREF_MAX_LEN)
        self.text = PrintText()
        # Settings
        self.pref.color = self._color_idx_2_obj(pref_args['color'])
        self.pref.bgcol = self._color_idx_2_obj(pref_args['bgcol'],
                                                back=True)
        self.pref.gloss = self._gloss_idx_2_obj(pref_args['gloss'])
        self.text.color = self._color_idx_2_obj(text_args['color'])
        self.text.bgcol = self._color_idx_2_obj(text_args['bgcol'],
                                                back=True)
        self.text.gloss = self._gloss_idx_2_obj(text_args['gloss'])

    def _color_idx_2_obj(self, color: typing.Union[str, int] = 7,
                         back=False) -> str:
        '''
        Convert color strings to corresponding integers

        Args:
            Color: color {[0-15],[[l]krgybmcw],[[light] color_name]}
            back: is this color for background?

        '''
        if color in (*FORE_COLORS, *BACK_COLORS):
            return color
        if isinstance(color, int):
            if not 0 <= color <= 15:
                warnings.warn("0 <= color <= 15, using 7", category=KeyWarning)
                color = 7
        else:
            for idx, alias_tup in enumerate(COLOR_INDICES):
                if color in alias_tup:
                    color = idx
                    break
        if not isinstance(color, int):
            warnings.warn(
                "Color string was not understood, fallback to default",
                category=KeyWarning
            )
            color = 0 if back else 7
        return BACK_COLORS[color] if back else FORE_COLORS[color]

    def _gloss_idx_2_obj(self, gloss: typing.Union[str, int] = 1) -> str:
        '''
        Convert gloss strings to corresponding integers

        Args:
            gloss: gloss to text {[0-3],[rcdb],{reset,normal,dim,bright}}
        '''
        if gloss in AVAIL_GLOSS:
            return gloss
        if isinstance(gloss, int):
            if not 0 <= gloss <= 3:
                warnings.warn("0 <= gloss <= 3, using 1", category=KeyWarning)
                gloss = 1
        else:
            for idx, alias_tup in enumerate(GLOSS_INDICES):
                if gloss in alias_tup:
                    gloss = idx
        if not isinstance(gloss, int):
            warnings.warn(
                "Gloss string was not understood, defaulting to normal",
                category=KeyWarning
            )
            gloss = 1
        return AVAIL_GLOSS[gloss]

    def __str__(self) -> str:
        '''
        String format of available information
        '''
        return "\t".join(
            ("", self.pref.effects + self.pref.short,
             str(self.pref),
             self.text.effects + "<CUSTOM>" + Style.RESET_ALL)
        )

    def __copy__(self):
        '''
        Copy of instance
        '''
        child = InfoMark(pref=self.pref.val, pref_s=self.pref_s)
        child.pref = self.pref.__copy__()
        child.text = self.text.__copy__()
        return child

    def get_info(self) -> str:
        '''
        Print information

        '''
        info = str(self)
        print(info)
        return info

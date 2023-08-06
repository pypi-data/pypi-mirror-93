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
Text Parts

'''


import typing
import colorama


class PrintText():
    '''
    Plain text object
    Text to be printed to (ANSI) terminal

    Args:
        val: the text
        color: color of text [0-15]
        gloss: gloss of text {0: bland, 1:normal ,2: dim, 3: bright}
        bgcol: color of background [0-15]

    '''
    def __init__(self, val: typing.Union[str, list] = '',
                 color=colorama.Fore.WHITE,
                 gloss=colorama.Style.NORMAL,
                 bgcol=colorama.Back.BLACK) -> None:
        self.val = str(val)
        self.color = color
        self.gloss = gloss
        self.bgcol = bgcol

    @property
    def effects(self) -> str:
        '''
        All effects combined
        '''
        return self.color + self.bgcol + self.gloss

    @effects.setter
    def effects(self, val):
        '''
        Value augmented with effects (color, gloss, background)
        '''
        self.val = val
        self.color = ''
        self.gloss = ''
        self.bgcol = ''

    @effects.deleter
    def effects(self):
        self.color = ''
        self.gloss = ''
        self.bgcol = ''

    @property
    def style_kwargs(self):
        '''
        extract color, gloss, bgcol to **kwargs
        '''
        return {'color': self.color,'gloss': self.gloss, 'bgcol': self.bgcol}

    def __str__(self) -> str:
        '''
        Human readable form
        '''
        return self.effects + str(self.val) + colorama.Style.RESET_ALL

    def __len__(self) -> int:
        '''
        length of value
        '''
        return len(self.val)

    def __copy__(self):
        '''
        create a copy
        '''
        return PrintText(val=self.val, color=self.color,
                         gloss=self.gloss, bgcol=self.bgcol)

    def copy(self):
        '''
        method to create a copy
        '''
        return self.__copy__()

    def to_str(self, bland: bool = False) -> str:
        '''
        Human readable form

        Args:
            bland: colorless pref

        '''
        out_str = [str(self.val)]
        if not bland:
            out_str.insert(0, self.effects)
            out_str.append(colorama.Style.RESET_ALL)
        return ''.join(out_str)


class PrintPref(PrintText):
    '''
    Prefix that informs about Text

    Args:
        val: str: prefix in long format
        pad_to: int: pad with `space` to length
        short: str: prefix in short format
        color: : color of text
        gloss: : gloss of text
        bgcol: : color of background

    Arguments:
        short: str: short representation of val
        pad_to: int: pad long_str to

    '''
    def __init__(self, val: str = None,  short: str = '>', pad_to: int = 0,
                 **kwargs) -> None:
        self.short = short
        if val is None:
            kwargs['val'] = ''
            self.pad_len = 2
        else:
            self.pad_len = 0
            kwargs['val'] = val.upper()
        self.pad_len += max(pad_to - len(kwargs['val']), 0)
        super().__init__(**kwargs)

    def __copy__(self):
        '''
        create a copy
        '''
        return PrintPref(val=self.val, short=self.short,
                         color=self.color, gloss=self.gloss, bgcol=self.bgcol)

    def to_str(self, **kwargs) -> str:
        '''
        Print value with effects

        Args:
            short: prefix in short form?
            pad: Pad prefix
            bland: colorless pref
'''
        if not kwargs.get('short'):
            out_str = [super().to_str(bland=kwargs.get('bland'))]
            if self.val:
                out_str.insert(0, "[")
                out_str.append("]")
            if kwargs.get('pad'):
                if not self.val:
                    out_str.append("  ")
                out_str.append(self.pad_len * " " + " ")
        else:
            out_str = [self.short]
            if self.short:
                out_str.insert(0, "[")
                out_str.append("]")
            if not kwargs.get('bland'):
                out_str.insert(0, self.effects)
                out_str.append(colorama.Style.RESET_ALL)
            if kwargs.get('pad'):
                if self.short:
                    out_str.append(" ")
                else:
                    out_str.append("    ")
        return ''.join(out_str)

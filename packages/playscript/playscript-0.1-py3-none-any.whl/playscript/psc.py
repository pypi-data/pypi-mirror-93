'''Classes to make up play script object.
'''

# from typing import List, overload
import re
from enum import Enum


class PScLineType(Enum):
    '''Types for PScLine.
    '''

    TITLE = 0                   # Title
    AUTHOR = 1                  # Author name
    CHARSHEADLINE = 2           # Headline of character list
    CHARACTER = 3               # Character
    H1 = 4                      # Headline of scene (level 1)
    H2 = 5                      # Headline of scene (level 2)
    H3 = 6                      # Headline of scene (level 3)
    DIRECTION = 7               # Direction
    DIALOGUE = 8                # Dialogue
    ENDMARK = 9                 # End mark
    COMMENT = 10                # Comment
    EMPTY = 11                  # Empty line
    CHARACTER_CONTINUED = 12    # Following lines of Character
    DIRECTION_CONTINUED = 13    # Following lines of Direction
    DIALOGUE_CONTINUED = 14     # Following lines of Dialogue
    COMMENT_CONTINUED = 15      # Foloowing lines of Comment


class PScLine:
    '''Line in PSc lines.
    '''

    # Delimiter of name and text in character lines
    chr_delimiter = re.compile(r'\s+')
    # Delimiter of name and text in dialogue lines
    dlg_delimiter = re.compile(r'\s*[\s「]')

    def __init__(self, line_type, name=None, text=None):
        try:
            self.type = PScLineType(line_type)
        except ValueError:
            raise TypeError(
                'Argument "line_type" should be a PScLineType member.')

        if line_type in (PScLineType.CHARACTER, PScLineType.DIALOGUE):
            if not name:
                raise ValueError(
                    'Argument "name" is required '
                    'for type CHARACTER or DIALOGUE.')

        if line_type not in (PScLineType.EMPTY, PScLineType.CHARACTER):
            if not text:
                raise ValueError(
                    'Argument "text" is required '
                    'for the other types than EMPTY or CHARACTER.')

        if name:
            self.name = name
        if text:
            self.text = text

    @classmethod
    def from_text(cls, line_type, text):
        '''Make PScLine object from PScLineType and a text
        '''

        text = text.strip()

        if line_type == PScLineType.CHARACTER:
            # Split text to name and text
            if not cls.chr_delimiter.search(text):
                name, text = text, ''
            else:
                name, text = cls.chr_delimiter.split(text, maxsplit=1)
            return cls(line_type, name=name, text=text)

        if line_type == PScLineType.DIALOGUE:
            # Split text to name and text
            if not cls.dlg_delimiter.search(text):
                name = '*'
            else:
                name, text = cls.dlg_delimiter.split(text, maxsplit=1)
            
            # TODO: 閉じ括弧を削除する。
            
            return cls(line_type, name=name, text=text)

        # TODO: line_type が数字や文字列だった場合に対応する。

        return cls(line_type, text=text)


class PSc:
    '''Play script.
    '''

    def __init__(self, title='', author='', chars=[], lines=[]):
        self.title = title
        self.author = author
        self.chars = chars
        # lines could be a generator while self.lines should be a list.
        self.lines = list(lines)

    @classmethod
    def from_lines(cls, lines):
        return cls(lines=lines)

    @classmethod
    def lines_from_types_and_texts(cls, line_types, texts):
        lines = []
        for line_type, text in zip(line_types, texts):
            line = PScLine.from_text(line_type, text)
            lines.append(line)
        return lines

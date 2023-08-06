# playscript

## Overview

Package for play script structure in Japanese style.

## Classes

### PSc

Play script containing lines and meta data.

### PScLine

Each line of lines contained in PSc object.  
It has an attribute "type" to determine if it's a dialogue or a direction, etc.

### PScLineType

This enum defines types for PScLine.

## Example

### Creating a 3-line script

```python
from playscript import PScLineType, PScLine, PSc

title = PScLine.from_text(PScLineType.TITLE, 'ろくでなしの冒険')
dialogue1 = PScLine.from_text(PScLineType.DIALOGUE, '六郎「どうする？」')
dialogue2 = PScLine.from_text(PScLineType.DIALOGUE, '七郎「帰って寝る」')

script = PSc(lines=[title, dialogue1, dialogue2])
```

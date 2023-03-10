# Mathiful - A simple shader-like game to draw using python!
---
## Features
* Simple step / running system
* Challenges
---
## How it works
* It goes through a list of pixel colors
```python
[
    [[0, 0, 0], [0, 0, 0], [255, 0, 0]],
    [[0, 0, 0], [255, 0, 0], [0, 0, 0]],
    [[255, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [255, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [255, 0, 0]]
]
```
* Goes through every RGB channel
* Applies expression, user entered\
For example: `c // (x + 1)`, which means: color divided by x coordinate plus 1 (preventing from division error)

### Before:
<img src="preview.png" alt="before" width="150" height="200"/>

### After:
<img src="after.png" alt="after" width="150" height="200"/>

---

PS: This "game" is still under development

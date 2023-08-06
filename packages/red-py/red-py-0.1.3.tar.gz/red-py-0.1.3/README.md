# red-py

library of useful tools and extensions

## installation

```bash
pip3 install red-py
```

## usage

### turtle
```python
from red.inara.turtle import CoolTurtle

turtle = CoolTurtle()

turtle.fillrgba(25, 25, 112, 1)
turtle.begin_fill()
turtle.ellipse(100, 50, 180)
turtle.end_fill()
```
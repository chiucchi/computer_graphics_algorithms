# Application

This app is being made with python 3.9.7, and tkinter library.

## Setup

You should install (if you don't have) Python 3.9

## Run

Clone my repository to your computer by doing a `git clone`:

```shell
git clone https://github.com/chiucchi/computer_graphics_algorithms
```

And when on the root directory for my project, execute `python3 main.py` on your terminal.

## Guidelines

Line rasterization:
1- Press on the button with of the desired algorithm
2- Click 2 times somewhere on the canvas, and the line will show up

Circunference rasterization:
1 - Enter the radius on the input
2 - Click the circunference button
3 - Click somewhere on the canvas, and the circunference will show up

Transformations:
For either translation and scale you should use the two following inputs as (x,y)
For rotation, use the last input on the row to input the desired radius.
The reflections don't need any input so just press the chosen one after a rasterization.
If you want to do any transformation there's should be at least a line or a circunference on the canvas.

Clipping:
Either for cohen-sutherland and liang-barsky you need to provide windows limits values on the last row of inputs, just enter the values and click the wanted button.

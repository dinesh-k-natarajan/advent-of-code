# My Solution for Day 20

[Jurassic Jigsaw](https://adventofcode.com/2020/day/20)

The toughest puzzle in this year's Advent!

### [Part 1](https://github.com/dinesh-k-natarajan/advent-of-code/blob/main/2020/20/20-1.py)
To find the corners of the jigsaw puzzle, a shortcut is to find the
number of matching tiles for a given tile. If a tile has 2 matching
tiles, then the tile would be a corner tile. If a tile has 3 matching
tiles, then the tile would be a border tile, etc.

Numpy was very helpful in solving this puzzle, thanks to the np.flip and
np.rot90 functions.

```bash
$ python 20-1.py
Test 1 Solution =  20899048083289
Part 1 Solution =  29584525501199
```

### [Part 2](https://github.com/dinesh-k-natarajan/advent-of-code/blob/main/2020/20/20-1.py)
Using the shortcut in Part 1 without actually solving the jigsaw puzzle
proved costly for Part 2. With the help of the AOC reddit thread, a jigsaw
solver was reimplemented for solving Part 1.

Using the solved jigsaw grid, the image is constructed. With the ASCII
monster as a kernel, an [image convolution](https://legacy.imagemagick.org/Usage/convolve/#convolve)
was applied to detect the monster patterns in the image and count the
number of monsters.

```bash
$ python 20-2.py
Test 1 Solution =  20899048083289
Test 2 Solution =  273
Part 1 Solution =  29584525501199
Part 2 Solution =  1665
```

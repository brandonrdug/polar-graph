# polar-graph
An ~easily configurable Python script for animating polar graphs using **[manim](https://github.com/ManimCommunity/manim)**

![Polar Graph of $r = cos(4 \theta)$](https://github.com/brandonrdug/polar-graph/blob/48706b4565282ec4bb57072f08b0689f6913021f/rose.gif)

### Prerequisites
- manim ([Installation Guide](https://docs.manim.community/en/stable/installation.html))
- LaTeX

### Configuring
To get started, simply edit the `polar_equation` function defined near the top of the file. Then, update the label written in LaTeX, and you're done!

You can easily adjust the range for the angles used in the graph by editing the value assigned to `polar_function_range`.
And, if your polar graph calls for more or less space on the x and y axes, you can edit `function_x_range` and `function_y_range`.

### Rendering
- Run `manim -qk polar_graph.py PolarGraph`
- Alternatively, run `manim -ql polar_graph.py PolarGraph` for a faster rendering with worse quality
- Add the flag `--format=gif` to compile into a gif instead of mp4 (e.g. `manim -qk --format=gif polar_graph.py PolarGraph`)

Your initial render will take the longest, manim needs to cache each new LaTeX string, and the theta tracking label in the scene will create a new string for every 10 degrees within your configured range. Luckily, it only needs to do this once, so each subsequent rendering will be much faster!

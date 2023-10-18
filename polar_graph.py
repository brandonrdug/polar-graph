from manim import *

config.pixel_width = 3840
config.pixel_height = 2160
config.background_color = "#171614"
config.tex_template.add_to_preamble(r"\usepackage{gensymb}")


# Polar function to be configured
def polar_function(theta):
    return np.cos(theta)


# LaTeX label for the function
polar_function_label = r"r = \cos(\theta)"
polar_function_range = (0, TAU)


# Actual parametric function being graphed; just utilitizes polar_function
def function(theta):
    return np.array(
        [
            polar_function(theta) * np.cos(theta),
            polar_function(theta) * np.sin(theta),
            0,
        ]
    )


# Remember to update the axes range if the function's range is relevant (e.g. if r can be > 1.25)
function_x_range = [-1.25, 1.25]
function_y_range = [-1.25, 1.25]


# Nothing to regularly configure below this line

# Dictionary of angles and their LaTeX labels
angle_dict = {
    PI / 6: r"\frac{\pi}{6}",
    PI / 4: r"\frac{\pi}{4}",
    PI / 3: r"\frac{\pi}{3}",
    2 * PI / 3: r"\frac{2\pi}{3}",
    3 * PI / 4: r"\frac{3\pi}{4}",
    5 * PI / 6: r"\frac{5\pi}{6}",
    7 * PI / 6: r"\frac{7\pi}{6}",
    5 * PI / 4: r"\frac{5\pi}{4}",
    4 * PI / 3: r"\frac{4\pi}{3}",
    5 * PI / 3: r"\frac{5\pi}{3}",
    7 * PI / 4: r"\frac{7\pi}{4}",
    11 * PI / 6: r"\frac{11\pi}{6}",
}


class PolarEquation(Scene):
    def setup_theta(self):
        self.theta_tracker = ValueTracker(0)

        self.theta_label = MathTex(
            r"\theta = ", r"0", r"\degree", font_size=24, color="#aaaaaa"
        ).move_to(RIGHT * 3.8)

        self.theta_label_updater = lambda m: m.become(
            MathTex(
                r"\theta = ",
                str(int(round(self.theta_tracker.get_value() * 180 / PI, -1))),
                r"\degree",
                color="#aaaaaa",
                font_size=24,
            ).move_to(m)
        )

    def setup_axes(self):
        self.axes = (
            Axes(
                x_range=[*function_x_range, 1],
                y_range=[*function_y_range, 1],
                axis_config={"include_ticks": False},
                tips=False,
                x_length=6,
                y_length=6,
            )
            .set_color(GREY_BROWN)
            .set_stroke(width=1)
        )

        self.graph += self.axes
        self.add(self.axes)

    def setup_func(self):
        self.func = self.axes.plot_parametric_curve(
            function,
            t_range=np.array(polar_function_range),
            color=GREEN,
        ).set_stroke(width=1)

        self.r_max: float = np.array(
            [
                r
                for r in [
                    self.axes.polar_to_point(polar_function(a), 0)[0]
                    for a in np.arange(*polar_function_range, 0.01)
                ]
            ]
        ).max()

        self.r_max_coord: float = np.array(
            [
                r
                for r in [
                    polar_function(a) for a in np.arange(*polar_function_range, 0.01)
                ]
            ]
        ).max()

        self.funcTracer = Line(
            self.graph.get_center(),
            self.axes.i2gp(0, self.func),
            stroke_width=1,
            color=GREY_BROWN,
        ).add_updater(
            lambda m: m.become(
                Line(
                    self.graph.get_center(),
                    self.axes.i2gp(self.theta_tracker.get_value(), self.func),
                    stroke_width=1,
                    color=GREY_BROWN,
                )
            )
        )

        self.graph += self.func
        self.graph += self.funcTracer

    def setup_func_label(self):
        self.func_label = MathTex(
            polar_function_label, font_size=24, color="#aaaaaa"
        ).move_to(UP * 3.3)

        self.add(self.func_label)

    def setup_radial_points(self):
        self.axes_circle = (
            Circle(radius=self.r_max, color=GREY_BROWN)
            .set_stroke(width=1)
            .set_opacity(0.5)
            .set_fill(None, opacity=0)
        )

        def angle_label_updater(m):
            angle = self.theta_tracker.get_value()

            for key in angle_dict.keys():
                if angle > key:
                    line2point = Line(
                        self.graph.get_center(),
                        self.axes.polar_to_point(self.r_max_coord, key),
                        stroke_width=1,
                        color=GREY_BROWN,
                    ).set_opacity(0.2)

                    offset_factor = 0.2
                    offset_x = (
                        offset_factor * RIGHT
                        if angle < PI / 2 or angle > 3 * PI / 2
                        else offset_factor * LEFT
                    )
                    offset_y = (
                        offset_factor * UP if angle < PI else offset_factor * DOWN
                    )

                    tex = (
                        MathTex(angle_dict[key], font_size=16)
                        .set_color("#aaaaaa")
                        .move_to(
                            self.axes.polar_to_point(self.r_max_coord, key)
                            + offset_x
                            + offset_y
                        )
                    )

                    group = VGroup(line2point, tex)
                    self.add(group)
                    turn_animation_into_updater(FadeIn(group, run_time=0.5))

                    del angle_dict[key]
                    break

        self.axes_circle.add_updater(angle_label_updater)
        self.graph += self.axes_circle
        self.add(self.axes_circle)

    def setup_angle(self):
        self.angle = Angle(
            self.axes.x_axis,
            self.axes.y_axis,
            radius=0,
            other_angle=False,
        )

        def update_angle(angle):
            if self.theta_tracker.get_value() > 0:
                angle.become(
                    Angle(
                        self.axes.x_axis,
                        Line(
                            self.graph.get_center(),
                            self.graph.get_center() + RIGHT,
                            stroke_width=0,
                        ).rotate(
                            self.theta_tracker.get_value(),
                            about_point=self.graph.get_center(),
                        ),
                        radius=0.25,
                        other_angle=False,
                        stroke_width=1,
                        color=GREY_BROWN,
                    )
                )

        self.angle_updater = update_angle
        self.graph += self.angle

    def construct(self):
        self.graph = VGroup()

        self.setup_theta()
        self.setup_axes()
        self.setup_func()
        self.setup_func_label()
        self.setup_radial_points()
        self.setup_angle()

        self.play(
            self.theta_tracker.animate(run_time=8).set_value(polar_function_range[1]),
            Create(self.func, run_time=8),
            FadeIn(self.funcTracer, self.angle, self.theta_label, run_time=0.5),
            UpdateFromFunc(self.theta_label, self.theta_label_updater),
            UpdateFromFunc(self.angle, self.angle_updater),
            rate_func=linear,
        )

        self.play(FadeOut(self.funcTracer, self.angle, run_time=1))
        self.wait()

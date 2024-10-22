from manim import *
import random
import itertools
import numpy as np

class Animation_Test(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1])
        self.play(Write(ax))
        self.wait()

        random_points = [
            (5, 5),
            (0.5, 0.5)
        ]

        random_points += [(random.uniform(3, 7), random.uniform(3, 7)) for _ in range(3)]
        dots = []
        for idx, (x, y) in enumerate(random_points):
            dot = Dot(ax.c2p(x, y), color=BLUE)
            dots.append(dot)
            label = Text(f"P{idx+1}", font_size=24).next_to(dot, RIGHT)
            self.add(label)
        self.play(LaggedStart(*[Write(dot) for dot in dots], lag_ratio=.05))
        self.wait()


        # Create a Text object to display the variance
        variance_value = 0
        variance_prefix = Text("Variance: ", font_size=24)
        variance_prefix.to_corner(UL, buff=0.5)
        variance_text = Text(f"{variance_value:.2f}", font_size=24).next_to(variance_prefix, RIGHT)
        self.add(variance_prefix)
        self.add(variance_text)
        self.wait()
        variances = []
        points_column_table = []
        new_variance_value = 0
        selected_points = dots[:2]

        table_data = [["Points", "Variance"]]
        table = Table(table_data, include_outer_lines=True)
        table.scale(0.3)
        table.to_corner(UR)
        for i, point in enumerate(selected_points):
            angles = []
            focus_point = point
            other_points = [p for j,p in enumerate(dots) if j!= i]
            pairs = list(itertools.combinations(other_points, 2))
            self.play(focus_point.animate.set_color(RED))
            table_data = [["Points", "Variance"]]

            for pair in pairs:
                line_a = Line(focus_point, pair[0])
                line_b = Line(focus_point, pair[1])
                self.play(Create(line_a))
                self.play(Create(line_b))

                angle_1 = Angle(line_a, line_b, other_angle=True, radius=0.5)
                angle_2 = Angle(line_a, line_b, other_angle=False, radius=0.5)

                if abs(angle_1.get_value()) < abs(angle_2.get_value()):
                    smaller_angle = angle_1
                else:
                    smaller_angle = angle_2
                angles.append(np.degrees(smaller_angle.get_value()))
                self.play(Create(smaller_angle))
                new_variance_value = np.var(angles)
                group = VGroup(line_a, line_b, smaller_angle, variance_text)
                new_variance_text = Text(f"{new_variance_value:.2f}", font_size=24).next_to(variance_prefix, RIGHT)

                self.play(Transform(group, new_variance_text, replace_mobject_with_target_in_scene=True))
                self.wait()
                variance_text = new_variance_text

            variances.append(f"{np.var(angles):.2f}")
            points_table_text = f"P{i}"
            points_column_table.append(points_table_text)
            

            for p, v in zip(points_column_table, variances):
                table_data.append([p, v])

            new_table = Table(table_data, include_outer_lines=True)
            new_table.scale(0.3)
            new_table.to_corner(UR)

            self.play(Transform(table, new_table, replace_mobject_with_target_in_scene=True))
            self.wait()
            table= new_table
            


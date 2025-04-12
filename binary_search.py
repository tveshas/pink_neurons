from manim import *

class BinarySearchVisualization(Scene):
    def construct(self):
        # Array and parameters
        array = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        target = 23
        array_mobs = []
        box_width = 1
        box_height = 1

        # Draw array boxes
        for i, num in enumerate(array):
            rect = Square(side_length=box_width)
            rect.move_to(RIGHT * (i - len(array) / 2 + 0.5) * box_width)
            txt = Text(str(num), font_size=32).move_to(rect.get_center())
            g = VGroup(rect, txt)
            array_mobs.append(g)

        array_group = VGroup(*array_mobs).move_to(UP * 1)
        self.play(FadeIn(array_group))

        # Index labels
        index_labels = []
        for i in range(len(array)):
            idx = Text(str(i), font_size=24, color=GREY)
            idx.next_to(array_mobs[i], DOWN, buff=0.2)
            index_labels.append(idx)
        self.play(*[FadeIn(idx) for idx in index_labels])

        # Show target
        target_text = Text(f"Target = {target}", font_size=36).to_corner(UL)
        self.play(Write(target_text))

        # Binary search variables
        low = 0
        high = len(array) - 1

        # Pointers for low, mid, high
        low_arrow = Arrow(UP, DOWN, buff=0).scale(0.5).next_to(array_mobs[low], UP, buff=0.2).set_color(BLUE)
        mid = (low + high) // 2
        mid_arrow = Arrow(UP, DOWN, buff=0).scale(0.5).next_to(array_mobs[mid], UP, buff=0.2).set_color(YELLOW)
        high_arrow = Arrow(UP, DOWN, buff=0).scale(0.5).next_to(array_mobs[high], UP, buff=0.2).set_color(RED)

        low_label = Text("low", font_size=22, color=BLUE).next_to(low_arrow, UP, buff=0.1)
        mid_label = Text("mid", font_size=22, color=YELLOW).next_to(mid_arrow, UP, buff=0.1)
        high_label = Text("high", font_size=22, color=RED).next_to(high_arrow, UP, buff=0.1)

        self.play(
            GrowArrow(low_arrow), FadeIn(low_label),
            GrowArrow(mid_arrow), FadeIn(mid_label),
            GrowArrow(high_arrow), FadeIn(high_label)
        )

        # Step-by-step binary search
        steps = [
            {"low": 0, "high": 9},
            {"low": 0, "high": 4},
            {"low": 3, "high": 4},
            {"low": 4, "high": 4},
        ]

        explanations = [
            "1. Compare mid (index 4, value 16) with target 23.\n16 < 23, so search right half.",
            "2. Now, low=5, high=9. Mid is index 7 (value 56).\n56 > 23, so search left half.",
            "3. Now, low=5, high=6. Mid is index 5 (value 23).\n23 == 23. Target found!",
        ]

        # Initial pointers already set at low=0, mid=4, high=9
        explanation_box = RoundedRectangle(corner_radius=0.15, height=1.6, width=7, color=WHITE, fill_opacity=0.1)
        explanation_box.to_corner(DOWN).shift(UP*0.2)
        explanation_text = Text(explanations[0], font_size=28).move_to(explanation_box.get_center())
        self.play(FadeIn(explanation_box), Write(explanation_text))
        self.wait(2)

        # First step: 16 < 23
        # Highlight mid
        mid_rect = SurroundingRectangle(array_mobs[4], color=YELLOW)
        self.play(Create(mid_rect))
        self.wait(1)
        # Animate low and mid pointers
        self.play(
            low_arrow.animate.next_to(array_mobs[5], UP, buff=0.2),
            low_label.animate.next_to(array_mobs[5], UP, buff=0.45),
            mid_arrow.animate.next_to(array_mobs[7], UP, buff=0.2),
            mid_label.animate.next_to(array_mobs[7], UP, buff=0.45),
            FadeOut(mid_rect),
            run_time=1.5
        )
        high_arrow.save_state()
        mid_rect2 = SurroundingRectangle(array_mobs[7], color=YELLOW)
        self.play(
            Transform(explanation_text, Text(explanations[1], font_size=28).move_to(explanation_box.get_center())),
            Create(mid_rect2)
        )
        self.wait(1)

        # Second step: 56 > 23
        # Animate high and mid pointers
        self.play(
            high_arrow.animate.next_to(array_mobs[6], UP, buff=0.2),
            high_label.animate.next_to(array_mobs[6], UP, buff=0.45),
            mid_arrow.animate.next_to(array_mobs[5], UP, buff=0.2),
            mid_label.animate.next_to(array_mobs[5], UP, buff=0.45),
            FadeOut(mid_rect2),
            run_time=1.5
        )
        mid_rect3 = SurroundingRectangle(array_mobs[5], color=YELLOW)
        self.play(
            Transform(explanation_text, Text(explanations[2], font_size=28).move_to(explanation_box.get_center())),
            Create(mid_rect3)
        )
        self.wait(1)

        # Third step: Found!
        found_rect = SurroundingRectangle(array_mobs[5], color=GREEN, buff=0.1)
        checkmark = Tex(r"\checkmark", color=GREEN).scale(2).next_to(array_mobs[5], UP, buff=0.3)
        self.play(
            FadeOut(mid_rect3),
            Create(found_rect),
            FadeIn(checkmark),
        )
        self.wait(2)

        # Final annotation
        result_text = Text("Target 23 found at index 5!", font_size=36, color=GREEN).to_edge(DOWN).shift(UP*0.4)
        self.play(Write(result_text))
        self.wait(2)
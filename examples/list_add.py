from manim import *

class ListAdd(Scene):
    def construct(self):
        # Title
        title = Text("List Add Operation", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Initial list elements
        values = [3, 7, 12, 18]
        squares = []
        labels = []

        # Draw initial list as boxes
        for i, val in enumerate(values):
            square = Square(side_length=1, color=BLUE)
            square.shift(RIGHT * (i * 1.2) - RIGHT * 1.8)
            squares.append(square)
            label = Text(str(val), font_size=30).move_to(square.get_center())
            labels.append(label)

        self.play(*[Create(square) for square in squares])
        self.play(*[Write(label) for label in labels])
        self.wait(1)

        # Show annotation: "Add value 21 to the list"
        add_text = Text("Add value 21", font_size=32, color=YELLOW)
        add_text.next_to(squares[-1], DOWN, buff=1.2)
        self.play(Write(add_text))
        self.wait(1)

        # Create new square to represent the new value
        new_square = Square(side_length=1, color=GREEN)
        new_square.shift(RIGHT * ((len(values)) * 1.2) - RIGHT * 1.8 + DOWN * 2)
        new_label = Text("21", font_size=30).move_to(new_square.get_center())

        # Show the new box appearing below
        self.play(FadeIn(new_square), FadeIn(new_label))
        self.wait(0.5)

        # Arrow showing movement to the end of the list
        arrow = Arrow(
            start=new_square.get_top(),
            end=squares[-1].get_top() + RIGHT * 1.2,
            buff=0.15,
            color=GREEN
        )
        self.play(Create(arrow))
        self.wait(0.5)

        # Move the new square and label to the end of the list
        target_pos = RIGHT * ((len(values)) * 1.2) - RIGHT * 1.8
        self.play(
            new_square.animate.move_to(target_pos),
            new_label.animate.move_to(target_pos),
            FadeOut(arrow),
            run_time=1
        )
        self.wait(0.5)

        # Update the visuals: Add the new square and label to the list
        squares.append(new_square)
        labels.append(new_label)

        # Highlight the updated list
        highlight_rect = SurroundingRectangle(VGroup(*squares), color=YELLOW, buff=0.2)
        self.play(Create(highlight_rect))
        self.wait(0.5)

        # Annotation: "List after addition"
        after_text = Text("List after addition", font_size=32, color=GREEN)
        after_text.next_to(highlight_rect, DOWN, buff=0.5)
        self.play(Write(after_text))
        self.wait(1.5)

        # Clean up
        self.play(FadeOut(add_text), FadeOut(after_text), FadeOut(highlight_rect))
        self.wait(0.5)

        # Final message
        done_text = Text("List add: Value appended to end", font_size=32)
        done_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(done_text))
        self.wait(2)
from manim import *

class ListInsertionVisualization(Scene):
    def construct(self):
        # Title
        title = Text("List Insertion Visualization", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Initial list values
        values = [3, 7, 12, 18]
        squares = []
        labels = []

        # Draw the initial list as boxes
        for i, val in enumerate(values):
            rect = Square(side_length=1, color=BLUE)
            rect.shift(RIGHT * (i * 1.2) - RIGHT * 1.8)
            squares.append(rect)
            label = Text(str(val), font_size=32).move_to(rect.get_center())
            labels.append(label)
        
        # Animate creation of initial list
        self.play(*[Create(rect) for rect in squares])
        self.play(*[Write(label) for label in labels])
        self.wait(1)

        # Annotation - initial list
        initial_anno = Text("Initial List", font_size=28)
        initial_anno.next_to(squares[0], UP, buff=0.8)
        self.play(FadeIn(initial_anno))
        self.wait(1)

        # Highlight position for insertion (insert 9 at index 2)
        insertion_index = 2
        highlight_rect = SurroundingRectangle(squares[insertion_index], color=YELLOW, buff=0.12)
        arrow = Arrow(
            initial_anno.get_bottom(),
            squares[insertion_index].get_top() + UP * 0.1,
            buff=0.1,
            color=YELLOW
        )
        insert_text = Text("Insert 9 here", font_size=28, color=YELLOW)
        insert_text.next_to(squares[insertion_index], UP, buff=0.5)
        self.play(Create(highlight_rect), Create(arrow), Write(insert_text))
        self.wait(1.2)

        # Animate shifting elements to the right
        shifting = []
        for i in range(len(squares) - 1, insertion_index - 1, -1):
            shifting.append(
                squares[i].animate.shift(RIGHT * 1.2)
            )
            shifting.append(
                labels[i].animate.shift(RIGHT * 1.2)
            )
        self.play(*shifting, run_time=1)
        self.wait(0.5)

        # Insert new square and label at the position
        new_square = Square(side_length=1, color=GREEN)
        new_square.move_to(squares[insertion_index].get_center())
        new_label = Text("9", font_size=32, color=GREEN).move_to(new_square.get_center())
        self.play(
            FadeIn(new_square),
            Write(new_label),
        )
        self.wait(0.5)

        # Update list to include new value for future reference
        squares.insert(insertion_index, new_square)
        labels.insert(insertion_index, new_label)

        # Fade out highlight and annotation
        self.play(
            FadeOut(highlight_rect),
            FadeOut(arrow),
            FadeOut(insert_text),
            FadeOut(initial_anno)
        )
        self.wait(0.5)

        # Rearrange all squares and labels for alignment
        for i, sq in enumerate(squares):
            target_x = RIGHT * (i * 1.2) - RIGHT * 1.8
            self.play(
                sq.animate.move_to([target_x[0], 0, 0]),
                labels[i].animate.move_to([target_x[0], 0, 0]),
                run_time=0.2
            )

        self.wait(0.3)

        # Annotation - final list state
        final_anno = Text("List after Insertion", font_size=28)
        final_anno.next_to(squares[0], UP, buff=0.8)
        self.play(FadeIn(final_anno))
        self.wait(1.5)

        # Highlight inserted node
        self.play(
            new_square.animate.set_color(ORANGE),
            new_label.animate.set_color(ORANGE),
            run_time=0.5
        )
        self.wait(1.2)

        # Reset color
        self.play(
            new_square.animate.set_color(GREEN),
            new_label.animate.set_color(GREEN),
            run_time=0.5
        )

        # End scene
        self.wait(1.5)
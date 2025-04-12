from manim import *

class Node(Scene):
    def construct(self):
        # Title
        title = Text("Node Data Structure", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Draw a single node
        node_circle = Circle(radius=0.8, color=BLUE)
        node_label = Text("Data", font_size=28).move_to(node_circle.get_center())
        node_group = VGroup(node_circle, node_label).move_to(ORIGIN)
        self.play(Create(node_circle))
        self.play(Write(node_label))
        self.wait(0.8)

        # Annotation: "A node stores data"
        data_annot = Text("A node stores data", font_size=28)
        data_annot.next_to(node_group, DOWN, buff=1)
        arrow1 = Arrow(start=data_annot.get_top(), end=node_group.get_bottom(), buff=0.05)
        self.play(Write(data_annot), Create(arrow1))
        self.wait(1.2)
        self.play(FadeOut(data_annot), FadeOut(arrow1))
        self.wait(0.3)

        # Add "Next" pointer
        pointer_text = Text("Next", font_size=22)
        pointer_text.next_to(node_circle, RIGHT, buff=0.6)
        pointer_arrow = Arrow(
            start=node_circle.get_right(),
            end=node_circle.get_right() + RIGHT * 1.2,
            buff=0.1,
            color=GREEN
        )
        self.play(Write(pointer_text), Create(pointer_arrow))
        self.wait(0.7)

        # Annotation: "A node points to the next node"
        pointer_annot = Text("A node points to the next node", font_size=28)
        pointer_annot.next_to(pointer_arrow, UP, buff=0.7)
        self.play(Write(pointer_annot))
        self.wait(1.3)
        self.play(FadeOut(pointer_annot))
        self.wait(0.3)

        # Create a second node and show the connection
        node2_circle = Circle(radius=0.8, color=BLUE).move_to(node_circle.get_center() + RIGHT * 3)
        node2_label = Text("Data", font_size=28).move_to(node2_circle.get_center())
        node2_group = VGroup(node2_circle, node2_label)
        self.play(Create(node2_circle), Write(node2_label))
        self.wait(0.7)

        # Animate the pointer connecting to the new node
        pointer_arrow2 = Arrow(
            start=node_circle.get_right(),
            end=node2_circle.get_left(),
            buff=0.1,
            color=GREEN
        )
        self.play(Transform(pointer_arrow, pointer_arrow2))
        self.wait(0.7)

        # Annotation: "This forms a linked structure"
        linked_annot = Text("This forms a linked structure", font_size=28)
        linked_annot.next_to(VGroup(node_group, node2_group), DOWN, buff=1)
        self.play(Write(linked_annot))
        self.wait(1.5)

        # Highlight both nodes
        self.play(
            node_circle.animate.set_color(YELLOW),
            node2_circle.animate.set_color(YELLOW),
            node_label.animate.set_color(RED),
            node2_label.animate.set_color(RED),
            run_time=0.7
        )
        self.wait(1)

        # Reset colors
        self.play(
            node_circle.animate.set_color(BLUE),
            node2_circle.animate.set_color(BLUE),
            node_label.animate.set_color(WHITE),
            node2_label.animate.set_color(WHITE),
            run_time=0.7
        )

        # Conclusion
        conclusion = Text("A node is a basic building block of data structures", font_size=28)
        conclusion.next_to(title, DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(2)
from manim import *

class ListDelete(Scene):
    def construct(self):
        # Title
        title = Text("List Delete Operation", font_size=42).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # List values
        values = [8, 12, 5, 18, 7]
        node_width = 1.4
        nodes = []
        labels = []
        arrows = []
        
        # Create list nodes (rectangles) and values
        for i, val in enumerate(values):
            node = Rectangle(width=node_width, height=1, color=BLUE)
            node.shift(RIGHT * (i * (node_width + 0.3)) - RIGHT * 2.7)
            nodes.append(node)
            label = Text(str(val), font_size=32).move_to(node.get_center())
            labels.append(label)
        
        # Create arrows between nodes
        for i in range(len(values) - 1):
            start = nodes[i].get_right()
            end = nodes[i+1].get_left()
            arrow = Arrow(start, end, buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            arrows.append(arrow)
        
        # Show nodes and values
        self.play(*[Create(node) for node in nodes])
        self.play(*[Write(label) for label in labels])
        self.wait(0.5)
        self.play(*[Create(arrow) for arrow in arrows])
        self.wait(0.5)
        
        # Step 1: Highlight node to delete (for example, 5 at index 2)
        node_to_delete = 2
        highlight = nodes[node_to_delete].copy().set_color(YELLOW).set_z_index(1)
        self.play(FadeIn(highlight, run_time=0.6), labels[node_to_delete].animate.set_color(RED))
        info1 = Text("Delete value 5", font_size=32).next_to(nodes[node_to_delete], DOWN, buff=0.8)
        self.play(Write(info1))
        self.wait(1)
        
        # Step 2: Fade out node and label
        self.play(
            FadeOut(nodes[node_to_delete], shift=UP),
            FadeOut(labels[node_to_delete], shift=UP),
            FadeOut(highlight),
            FadeOut(arrows[node_to_delete-1] if node_to_delete > 0 else VGroup(), shift=UP),
            FadeOut(arrows[node_to_delete] if node_to_delete < len(arrows) else VGroup(), shift=UP),
            FadeOut(info1)
        )
        self.wait(0.5)
        
        # Step 3: Move the nodes after the deleted node to the left
        shift_amount = node_width + 0.3
        for i in range(node_to_delete+1, len(nodes)):
            self.play(
                nodes[i].animate.shift(LEFT * shift_amount),
                labels[i].animate.shift(LEFT * shift_amount),
                run_time=0.4
            )
        
        # Step 4: Update arrows
        # Fade out old arrows
        for arrow in arrows:
            self.remove(arrow)
        # Create new arrows
        new_arrows = []
        new_indices = list(range(len(values)))
        new_indices.pop(node_to_delete)
        for i in range(len(new_indices)-1):
            idx1 = new_indices[i]
            idx2 = new_indices[i+1]
            arrow = Arrow(nodes[idx1].get_right(), nodes[idx2].get_left(), buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            new_arrows.append(arrow)
        
        self.play(*[Create(arrow) for arrow in new_arrows])
        self.wait(0.5)
        
        # Step 5: Show result annotation
        result_text = Text("5 is deleted. List is now:", font_size=30)
        result_text.next_to(title, DOWN, buff=0.6)
        self.play(Write(result_text))
        self.wait(0.7)
        after_text = Text("8   12   18   7", font_size=34, color=GREEN)
        after_text.next_to(nodes[0], DOWN, buff=1.2)
        self.play(Write(after_text))
        self.wait(2)
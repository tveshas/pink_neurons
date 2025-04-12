from manim import *

class SimpleListVisualization(Scene):
    def construct(self):
        # Title
        title = Text("Simple List Data Structure", font_size=40).to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)

        # Draw empty list
        empty_list_text = Text("Start with an empty list", font_size=28).next_to(title, DOWN, buff=1)
        self.play(Write(empty_list_text))
        self.wait(1)

        # List box positions
        boxes = []
        box_width = 1.2
        start_x = -3
        y_pos = 0
        for i in range(5):
            rect = Square(box_width).move_to([start_x + i*box_width, y_pos, 0])
            boxes.append(rect)

        # Show empty slots
        boxes_group = VGroup(*boxes)
        self.play(Create(boxes_group), run_time=1.5)
        self.wait(0.5)
        hint = Text("Each box represents a list element", font_size=24).next_to(boxes_group, DOWN)
        self.play(FadeIn(hint))
        self.wait(1.2)
        self.play(FadeOut(hint), FadeOut(empty_list_text))

        # Step 1: Adding elements
        add_text = Text("Add elements: 3, 8, 1", font_size=28).next_to(title, DOWN, buff=1)
        self.play(Write(add_text))
        self.wait(0.5)

        elements = ["3", "8", "1"]
        element_mobs = []
        for i, elem in enumerate(elements):
            elem_mob = Text(elem, font_size=36)
            elem_mob.set_color(BLUE)
            elem_mob.move_to([-5, -2, 0]).shift(RIGHT*i*1.5)
            element_mobs.append(elem_mob)
        self.play(*[FadeIn(mob) for mob in element_mobs])
        self.wait(0.7)

        # Animate adding to list boxes
        for i, elem_mob in enumerate(element_mobs):
            target_pos = boxes[i].get_center()
            self.play(elem_mob.animate.move_to(target_pos), run_time=0.8)
            self.wait(0.3)
        self.wait(1)
        self.play(FadeOut(add_text))

        # Step 2: Accessing an element
        access_text = Text("Access element at index 1", font_size=28).next_to(title, DOWN, buff=1)
        self.play(Write(access_text))
        self.wait(0.7)

        index_label = Text("Index 1", font_size=22, color=YELLOW).next_to(boxes[1], DOWN)
        self.play(FadeIn(index_label))
        highlight = SurroundingRectangle(boxes[1], color=YELLOW, buff=0.05)
        self.play(Create(highlight), boxes[1].animate.set_fill(YELLOW, opacity=0.2))
        self.wait(1.2)
        self.play(FadeOut(highlight), boxes[1].animate.set_fill(WHITE, opacity=0.0), FadeOut(index_label), FadeOut(access_text))

        # Step 3: Modifying an element
        mod_text = Text("Modify element at index 2 to 5", font_size=28).next_to(title, DOWN, buff=1)
        self.play(Write(mod_text))
        self.wait(0.7)

        old_elem = element_mobs[2]
        new_value = Text("5", font_size=36, color=GREEN).move_to(old_elem.get_center())
        arrow = Arrow(start=[boxes[2].get_center()[0], boxes[2].get_center()[1]+0.6,0],
                      end=[boxes[2].get_center()[0], boxes[2].get_center()[1]+0.15,0], buff=0.1)
        self.play(Create(arrow))
        self.play(Transform(old_elem, new_value), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(arrow), FadeOut(mod_text))

        # Step 4: Removing an element
        rem_text = Text("Remove element at index 0", font_size=28).next_to(title, DOWN, buff=1)
        self.play(Write(rem_text))
        self.wait(0.7)

        cross = Cross(boxes[0], stroke_color=RED, stroke_width=4)
        self.play(Create(cross))
        self.wait(0.5)
        self.play(FadeOut(element_mobs[0]), FadeOut(cross), boxes[0].animate.set_fill(RED, opacity=0.15))
        self.wait(0.5)
        shift_group = VGroup(element_mobs[1], element_mobs[2])
        self.play(shift_group.animate.shift(LEFT*box_width), run_time=0.7)
        self.wait(1)

        # End
        end_text = Text("This is how a simple list works!", font_size=32).to_edge(DOWN)
        self.play(FadeIn(end_text))
        self.wait(2)
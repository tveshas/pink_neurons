from manim import *

class RadixSortVisualization(Scene):
    def construct(self):
        # Example list
        numbers = [170, 45, 75, 90, 802, 24, 2, 66]
        num_boxes = []
        box_width = 1.5
        box_height = 1
        start_x = -5.25
        y_level = 2
        
        # Title
        title = Text("Radix Sort Visualization", font_size=38).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Draw the number boxes
        for i, num in enumerate(numbers):
            box = Rectangle(width=box_width, height=box_height, color=BLUE).move_to([start_x + i*box_width, y_level, 0])
            num_text = Text(str(num), font_size=32).move_to(box.get_center())
            group = VGroup(box, num_text)
            num_boxes.append(group)
            self.add(group)
        
        self.wait(0.5)
        
        # Show process text
        step_text = Text("Sort by Least Significant Digit (units)", font_size=32).next_to(title, DOWN)
        self.play(FadeIn(step_text))
        self.wait(0.5)
        
        # Show buckets
        buckets = []
        bucket_labels = []
        bucket_y = -1.5
        for i in range(10):
            bucket = Rectangle(width=1.1*box_width, height=box_height*1.2, color=GREY).move_to([start_x + i*box_width, bucket_y, 0])
            label = Text(str(i), font_size=28).next_to(bucket, DOWN, buff=0.18)
            buckets.append(bucket)
            bucket_labels.append(label)
            self.add(bucket, label)
        self.wait(0.5)
        
        # Animation: Move boxes to buckets based on units digit
        bucket_positions = {i: [] for i in range(10)}
        for group, num in zip(num_boxes, numbers):
            digit = num % 10
            pos = buckets[digit].get_center() + UP*0.2 + DOWN*0.15*len(bucket_positions[digit])
            bucket_positions[digit].append(pos)
            self.play(group.animate.move_to(pos), run_time=0.5)
        self.wait(1)
        
        # Collect numbers from buckets (left to right)
        sorted_numbers = []
        sorted_boxes = []
        collect_y = -3
        collect_start_x = -5.25
        index = 0
        for i in range(10):
            for j, pos in enumerate(bucket_positions[i]):
                for group, num in zip(num_boxes, numbers):
                    if group.get_center() == pos:
                        new_pos = [collect_start_x + index*box_width, collect_y, 0]
                        self.play(group.animate.move_to(new_pos), run_time=0.5)
                        sorted_numbers.append(num)
                        sorted_boxes.append(group)
                        index += 1
        self.wait(0.7)
        
        # Clean up
        self.play(*[FadeOut(mob) for mob in buckets + bucket_labels + [step_text]])
        self.wait(0.3)
        
        # Next step text
        step2_text = Text("Sort by Next Digit (tens)", font_size=32).next_to(title, DOWN)
        self.play(FadeIn(step2_text))
        self.wait(0.5)
        
        # Draw buckets again
        buckets2 = []
        bucket_labels2 = []
        for i in range(10):
            bucket = Rectangle(width=1.1*box_width, height=box_height*1.2, color=GREY).move_to([start_x + i*box_width, bucket_y, 0])
            label = Text(str(i), font_size=28).next_to(bucket, DOWN, buff=0.18)
            buckets2.append(bucket)
            bucket_labels2.append(label)
            self.add(bucket, label)
        self.wait(0.4)
        
        # Move boxes to buckets based on tens digit
        bucket_positions2 = {i: [] for i in range(10)}
        for group, num in zip(sorted_boxes, sorted_numbers):
            digit = (num // 10) % 10
            pos = buckets2[digit].get_center() + UP*0.2 + DOWN*0.15*len(bucket_positions2[digit])
            bucket_positions2[digit].append(pos)
            self.play(group.animate.move_to(pos), run_time=0.5)
        self.wait(1)
        
        # Collect numbers from buckets again
        sorted_numbers2 = []
        sorted_boxes2 = []
        collect_y2 = -4.5
        index = 0
        for i in range(10):
            for j, pos in enumerate(bucket_positions2[i]):
                for group, num in zip(sorted_boxes, sorted_numbers):
                    if group.get_center() == pos:
                        new_pos = [collect_start_x + index*box_width, collect_y2, 0]
                        self.play(group.animate.move_to(new_pos), run_time=0.5)
                        sorted_numbers2.append(num)
                        sorted_boxes2.append(group)
                        index += 1
        self.wait(0.7)
        
        self.play(*[FadeOut(mob) for mob in buckets2 + bucket_labels2 + [step2_text]])
        self.wait(0.3)
        
        # Last step text
        step3_text = Text("Sort by Most Significant Digit (hundreds)", font_size=32).next_to(title, DOWN)
        self.play(FadeIn(step3_text))
        self.wait(0.5)
        
        # Draw buckets again
        buckets3 = []
        bucket_labels3 = []
        for i in range(10):
            bucket = Rectangle(width=1.1*box_width, height=box_height*1.2, color=GREY).move_to([start_x + i*box_width, bucket_y, 0])
            label = Text(str(i), font_size=28).next_to(bucket, DOWN, buff=0.18)
            buckets3.append(bucket)
            bucket_labels3.append(label)
            self.add(bucket, label)
        self.wait(0.4)
        
        # Move boxes to buckets based on hundreds digit
        bucket_positions3 = {i: [] for i in range(10)}
        for group, num in zip(sorted_boxes2, sorted_numbers2):
            digit = (num // 100) % 10
            pos = buckets3[digit].get_center() + UP*0.2 + DOWN*0.15*len(bucket_positions3[digit])
            bucket_positions3[digit].append(pos)
            self.play(group.animate.move_to(pos), run_time=0.5)
        self.wait(1)
        
        # Collect numbers from buckets for final sorted order
        final_y = 0
        final_sorted = []
        final_boxes = []
        index = 0
        for i in range(10):
            for j, pos in enumerate(bucket_positions3[i]):
                for group, num in zip(sorted_boxes2, sorted_numbers2):
                    if group.get_center() == pos:
                        new_pos = [collect_start_x + index*box_width, final_y, 0]
                        self.play(group.animate.move_to(new_pos), run_time=0.5)
                        final_sorted.append(num)
                        final_boxes.append(group)
                        index += 1
        self.wait(1)
        
        self.play(*[FadeOut(mob) for mob in buckets3 + bucket_labels3 + [step3_text]])
        self.wait(0.5)
        
        # Final text and highlight
        result_text = Text("Sorted Array:", font_size=36).next_to(title, DOWN)
        underline = Line(start=[collect_start_x-0.5, final_y-0.8, 0], end=[collect_start_x+index*box_width-1, final_y-0.8, 0], color=YELLOW)
        self.play(FadeIn(result_text), Create(underline))
        self.wait(1.5)
        self.play(*[group[0].animate.set_color(YELLOW) for group in final_boxes])
        self.wait(2)
        self.play(FadeOut(title), FadeOut(result_text), FadeOut(underline), *[FadeOut(group) for group in final_boxes])
        self.wait(0.5)
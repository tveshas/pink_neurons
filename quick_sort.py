from manim import *

class QuickSortScene(Scene):
    def construct(self):
        # Array to sort
        array = [6, 3, 8, 5, 2, 7, 4]
        n = len(array)
        array_mobs = self.create_array_mobjects(array)
        self.play(LaggedStart(*[FadeIn(mob) for mob in array_mobs], lag_ratio=0.1))
        self.wait(0.5)

        title = Text("Quick Sort", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Start the quicksort visualization
        self.quick_sort(array, array_mobs, 0, n-1, title)

        self.wait(2)

    def create_array_mobjects(self, array):
        array_mobs = VGroup()
        for i, num in enumerate(array):
            box = Square(side_length=1)
            num_text = Integer(num).move_to(box.get_center())
            group = VGroup(box, num_text)
            group.move_to(RIGHT * (i - len(array)/2 + 0.5))
            array_mobs.add(group)
        array_mobs.move_to(DOWN*1)
        return array_mobs

    def quick_sort(self, array, array_mobs, low, high, title, level=0):
        if low < high:
            # Partition step
            pivot_index = high
            pivot_value = array[pivot_index]

            # Highlight pivot
            pivot_rect = SurroundingRectangle(array_mobs[pivot_index], color=YELLOW, buff=0.1)
            pivot_label = Text("Pivot", font_size=28, color=YELLOW).next_to(array_mobs[pivot_index], UP)
            self.play(Create(pivot_rect), FadeIn(pivot_label))
            self.wait(0.5)

            # Partition label
            part_label = Text(f"Partition: {array[low:high+1]}", font_size=32, color=BLUE).next_to(title, DOWN)
            self.play(FadeIn(part_label))

            i = low - 1
            for j in range(low, high):
                # Highlight current element
                curr_rect = SurroundingRectangle(array_mobs[j], color=BLUE, buff=0.1)
                self.play(Create(curr_rect))
                self.wait(0.3)

                if array[j] < pivot_value:
                    i += 1
                    if i != j:
                        # Swap
                        self.swap(array, array_mobs, i, j)
                        self.wait(0.4)
                    # Annotate less-than-pivot
                    less_label = Text("< Pivot", font_size=24, color=GREEN).next_to(array_mobs[i], DOWN)
                    self.play(FadeIn(less_label))
                    self.wait(0.2)
                    self.play(FadeOut(less_label))

                self.play(FadeOut(curr_rect))

            # Final swap with pivot
            i += 1
            if i != pivot_index:
                self.swap(array, array_mobs, i, pivot_index)
                self.wait(0.5)
            # Move pivot rect to new position
            self.play(pivot_rect.animate.move_to(array_mobs[i]), pivot_label.animate.next_to(array_mobs[i], UP))
            self.wait(0.3)
            self.play(FadeOut(pivot_rect), FadeOut(pivot_label), FadeOut(part_label))

            # Mark the sorted pivot
            sorted_rect = SurroundingRectangle(array_mobs[i], color=GREEN, buff=0.1)
            sorted_label = Text("Pivot Sorted", font_size=24, color=GREEN).next_to(array_mobs[i], UP)
            self.play(Create(sorted_rect), FadeIn(sorted_label))
            self.wait(0.4)
            self.play(FadeOut(sorted_rect), FadeOut(sorted_label))

            # Recursive calls
            self.quick_sort(array, array_mobs, low, i-1, title, level+1)
            self.quick_sort(array, array_mobs, i+1, high, title, level+1)
        else:
            # Optionally highlight base case
            if low == high:
                rect = SurroundingRectangle(array_mobs[low], color=GREEN, buff=0.1)
                sorted_label = Text("Sorted", font_size=20, color=GREEN).next_to(array_mobs[low], UP)
                self.play(Create(rect), FadeIn(sorted_label))
                self.wait(0.3)
                self.play(FadeOut(rect), FadeOut(sorted_label))

    def swap(self, array, array_mobs, i, j):
        array[i], array[j] = array[j], array[i]
        mob_i, mob_j = array_mobs[i], array_mobs[j]
        array_mobs[i], array_mobs[j] = mob_j, mob_i
        self.play(
            mob_i.animate.move_to(mob_j.get_center()),
            mob_j.animate.move_to(mob_i.get_center()),
            run_time=0.5
        )
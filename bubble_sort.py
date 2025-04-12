from manim import *
from manim_dsa import *
import random

class BubbleSort(Scene):
    def construct(self):
        # Configuration
        num_elements = 10
        bar_colors = [
            "#B0B0B0",  # Gray
            "#A19D9D",  # Light Gray
            "#D49E9E",  # Light Red
            "#E58A8A",  # Medium Red
            "#D4A79E",  # Light Salmon
            "#81BCE0",  # Light Blue
            "#E0CD81",  # Light Yellow
            "#7BBF7B",  # Light Green
        ]
        
        # Create a randomly ordered array
        values = list(range(1, num_elements + 1))
        random.shuffle(values)
        
        # Create a title
        title = Text("Bubble Sort").scale(1.2).to_edge(UP, buff=0.5)
        
        # Create counters for passes, comparisons, and swaps
        pass_counter = Text("Pass 0/0", font_size=36, color=BLUE)
        comparison_counter = Text("Comparisons: 0", font_size=36, color=YELLOW)
        swap_counter = Text("Swaps: 0", font_size=36, color=YELLOW)
        
        # Position counters - improved positioning to avoid overlaps
        pass_counter.to_edge(LEFT, buff=1).shift(DOWN * 0.5)
        comparison_counter.to_edge(RIGHT, buff=1).shift(UP * 1.5)
        swap_counter.next_to(comparison_counter, DOWN, buff=0.3).align_to(comparison_counter, LEFT)
        
        # Create a visualization of the array as bars with their labels
        bars_group = self.create_bar_elements(values)
        bars_group.center().shift(DOWN * 0.5)
        
        # Create the scene
        self.play(
            Write(title),
            Write(pass_counter),
            Write(comparison_counter),
            Write(swap_counter),
            Create(bars_group)
        )
        self.wait(1)
        
        # Counters for statistics
        comparisons = 0
        swaps = 0
        
        # Perform bubble sort
        for i in range(len(values)):
            # Update pass counter
            new_pass_counter = Text(f"Pass {i+1}/{len(values)}", font_size=36, color=BLUE)
            new_pass_counter.move_to(pass_counter)
            self.play(Transform(pass_counter, new_pass_counter))
            
            # Flag to check if any swaps occurred in this pass
            swapped = False
            
            for j in range(0, len(values) - i - 1):
                # Update comparisons counter
                comparisons += 1
                new_comparison_counter = Text(f"Comparisons: {comparisons}", font_size=36, color=YELLOW)
                new_comparison_counter.move_to(comparison_counter)
                self.play(Transform(comparison_counter, new_comparison_counter), run_time=0.3)
                
                # Highlight bars being compared
                self.play(
                    bars_group[j][0].animate.set_color(RED),
                    bars_group[j+1][0].animate.set_color(RED),
                    run_time=0.5
                )
                
                # Check if swap is needed
                if values[j] > values[j+1]:
                    # Perform swap in the values list
                    values[j], values[j+1] = values[j+1], values[j]
                    swapped = True
                    swaps += 1
                    
                    # Update swaps counter
                    new_swap_counter = Text(f"Swaps: {swaps}", font_size=36, color=YELLOW)
                    new_swap_counter.move_to(swap_counter)
                    self.play(Transform(swap_counter, new_swap_counter), run_time=0.3)
                    
                    # Store current positions
                    pos_j = bars_group[j].get_center()
                    pos_j_plus_1 = bars_group[j+1].get_center()
                    
                    # Swap the entire bar groups (bar + label)
                    self.play(
                        bars_group[j].animate.move_to(pos_j_plus_1),
                        bars_group[j+1].animate.move_to(pos_j),
                        run_time=0.8
                    )
                    
                    # Update the bar groups in the list
                    bars_group[j], bars_group[j+1] = bars_group[j+1], bars_group[j]
                
                # Unhighlight the bars and return to their respective colors
                bar_color_index_j = min(values[j] % len(bar_colors), len(bar_colors) - 1)
                bar_color_index_j1 = min(values[j+1] % len(bar_colors), len(bar_colors) - 1)
                
                self.play(
                    bars_group[j][0].animate.set_color(bar_colors[bar_color_index_j]),
                    bars_group[j+1][0].animate.set_color(bar_colors[bar_color_index_j1]),
                    run_time=0.5
                )
            
            # If no swaps occurred, the array is sorted
            if not swapped:
                break
            
            # Highlight the largest element which is now in its correct position
            self.play(
                bars_group[len(values) - i - 1][0].animate.set_color(GREEN),
                run_time=0.5
            )
        
        # All elements are in their correct positions
        self.play(
            *[bar_group[0].animate.set_color(GREEN) for bar_group in bars_group],
            run_time=1
        )
        
        # Final message
        sorted_text = Text("Array Sorted!", font_size=40, color=GREEN)
        sorted_text.to_edge(DOWN, buff=0.5)
        self.play(Write(sorted_text))
        
        self.wait(2)
    
    def create_bar_elements(self, values):
        """Create bars with their labels grouped together."""
        bar_colors = [
            "#B0B0B0",  # Gray
            "#A19D9D",  # Light Gray
            "#D49E9E",  # Light Red
            "#E58A8A",  # Medium Red
            "#D4A79E",  # Light Salmon
            "#81BCE0",  # Light Blue
            "#E0CD81",  # Light Yellow
            "#7BBF7B",  # Light Green
        ]
        
        max_height = 4    # Maximum height of the bars
        width = 0.6       # Width of each bar
        spacing = 0.3     # Space between bars
        
        # Create bars with heights proportional to values
        bar_elements = VGroup()
        for i, val in enumerate(values):
            # Create the bar
            height = val * max_height / max(values)
            bar = Rectangle(
                height=height, 
                width=width,
                fill_opacity=1,
                color=bar_colors[val % len(bar_colors)]
            )
            
            # Create the label
            label = Text(str(val), font_size=24)
            
            # Group bar and label
            bar_group = VGroup()
            
            # Position the bar (bottom of bar at origin)
            bar.move_to(UP * height/2)
            
            # Position the label below the bar
            label.next_to(bar, DOWN, buff=0.2)
            
            # Add to group
            bar_group.add(bar, label)
            
            # Position the group
            bar_group.move_to(RIGHT * i * (width + spacing))
            
            # Add to collection
            bar_elements.add(bar_group)
        
        return bar_elements 
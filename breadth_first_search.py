from manim import *

class BFSVisualization(Scene):
    def construct(self):
        # Title
        title = Text("Breadth-First Search (BFS)", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Define the graph nodes positions
        positions = {
            "A": LEFT * 3 + UP * 1,
            "B": LEFT * 1 + UP * 2,
            "C": RIGHT * 1 + UP * 2,
            "D": LEFT * 2 + DOWN * 1,
            "E": ORIGIN,
            "F": RIGHT * 2 + DOWN * 1,
            "G": RIGHT * 3 + UP * 1,
        }

        # Create vertices
        vertices = {k: Circle(radius=0.4, color=BLUE).move_to(v) for k, v in positions.items()}
        labels = {k: Text(k, font_size=28).move_to(v) for k, v in positions.items()}

        # Edges as (start, end)
        edges = [
            ("A", "B"),
            ("A", "D"),
            ("B", "C"),
            ("B", "E"),
            ("C", "G"),
            ("D", "E"),
            ("E", "F"),
            ("F", "G"),
        ]
        edge_lines = []
        for u, v in edges:
            line = Line(positions[u], positions[v], color=GRAY)
            edge_lines.append(line)

        # Draw graph
        self.play(*[Create(edge) for edge in edge_lines])
        self.play(*[Create(vertices[k]) for k in vertices])
        self.play(*[Write(labels[k]) for k in labels])
        self.wait(0.5)

        # BFS Explanation
        explain = Text("Start BFS from node A", font_size=28).next_to(title, DOWN)
        self.play(Write(explain))
        self.wait(1)

        # BFS steps
        bfs_order = ["A", "B", "D", "C", "E", "F", "G"]
        bfs_edges = [
            ("A", "B"),
            ("A", "D"),
            ("B", "C"),
            ("B", "E"),
            ("E", "F"),
            ("C", "G"),
            ("F", "G"),
        ]
        visited_color = GREEN
        queue_color = YELLOW

        # Visualize queue
        queue_box = Rectangle(width=4, height=1, color=queue_color).to_corner(DOWN + LEFT)
        queue_text = Text("Queue:", font_size=28).next_to(queue_box, UP, buff=0.2).align_to(queue_box, LEFT)
        self.play(Create(queue_box), Write(queue_text))

        queue_elements = []

        # BFS animation
        visited = set()
        queue = []

        # Helper to add to queue
        def update_queue_display(queue):
            for elem in queue_elements:
                self.remove(elem)
            queue_elements.clear()
            for i, name in enumerate(queue):
                circ = Circle(radius=0.3, color=queue_color, fill_opacity=0.5).move_to(queue_box.get_left() + RIGHT*0.7 + RIGHT*i*0.8)
                label = Text(name, font_size=24).move_to(circ.get_center())
                self.add(circ, label)
                queue_elements.append(circ)
                queue_elements.append(label)

        # Start BFS from 'A'
        queue.append("A")
        update_queue_display(queue)
        self.wait(0.7)

        # BFS algorithm step by step
        parent = { "A": None }
        edges_drawn = set()
        while queue:
            current = queue.pop(0)
            update_queue_display(queue)
            # Highlight current node
            self.play(vertices[current].animate.set_fill(visited_color, opacity=0.7), run_time=0.4)
            self.wait(0.2)
            visited.add(current)
            # Find neighbors
            neighbors = []
            for u, v in edges:
                if u == current and v not in visited and v not in queue:
                    neighbors.append(v)
                    parent[v] = u
                elif v == current and u not in visited and u not in queue:
                    neighbors.append(u)
                    parent[u] = v
            # Enqueue
            for n in neighbors:
                queue.append(n)
                update_queue_display(queue)
                # Highlight neighbor
                self.play(vertices[n].animate.set_stroke(queue_color, width=6), run_time=0.3)
                self.wait(0.1)
            # Draw tree edge
            if parent[current]:
                edge_key = (parent[current], current) if (parent[current], current) in edges else (current, parent[current])
                if edge_key not in edges_drawn:
                    ind = edges.index(edge_key)
                    self.play(edge_lines[ind].animate.set_color(visited_color).set_stroke(width=8), run_time=0.4)
                    edges_drawn.add(edge_key)
            self.wait(0.2)
            # Remove queue highlight
            self.play(vertices[current].animate.set_stroke(BLUE, width=4), run_time=0.2)

        # Final annotation: traversal order
        traversal_text = Text("BFS Traversal Order: " + " → ".join(bfs_order), font_size=28)
        traversal_text.next_to(queue_box, UP, buff=1.2)
        self.play(Write(traversal_text))
        self.wait(2)
# sandy.g.cabanes
# Title:
# Date:
# ------------------------------------------------------------
"""

"""
# Streamlined Flowchart Builder
# Simplified and optimized version focusing on core functionality

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

class NodeType(Enum):
    REGULAR = "regular"
    MERGE = "merge"

class Direction(Enum):
    DOWN = "down"
    RIGHT = "right"

@dataclass
class Node:
    """Simple node representation."""
    id: str
    text: List[str]
    node_type: NodeType
    connections: List[str]
    direction: Direction = Direction.DOWN
    is_loop: bool = False
    loop_target: str = ""
    is_end: bool = False

    def display_text(self) -> str:
        return f"{self.text[0]} (ID: {self.id.split('-')[1]})"

class FlowchartBuilder:
    """Main application class - simplified MVC approach."""

    def __init__(self):
        self.root = tk.Tk()
        self.nodes: List[Node] = []
        self.node_counter = 0
        self.flowchart_ended = False

        # UI Constants
        self.NODE_WIDTH = 25
        self.NODE_HEIGHT = 5
        self.V_SPACING = 3
        self.H_SPACING = 7
        self.MAX_LINE_LENGTH = 21

        self._setup_ui()
        self._bind_events()
        self._update_ui_state()

    def _setup_ui(self):
        """Setup the user interface."""
        self.root.title("Flowchart Builder")
        self.root.geometry("1200x700")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

        # Left panel (input)
        self.input_frame = ttk.Frame(self.root, padding="15")
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Right panel (output)
        self.output_frame = ttk.Frame(self.root, padding="15")
        self.output_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.output_frame.grid_rowconfigure(1, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        self._create_input_widgets()
        self._create_output_widgets()

    def _create_input_widgets(self):
        """Create input panel widgets."""
        # Title
        self.title_label = ttk.Label(self.input_frame, text="Flowchart Builder",
                                   font=("TkDefaultFont", 16, "bold"))

        # Start section
        self.start_label = ttk.Label(self.input_frame,
                                   text="Enter text for the start step (1-2 lines):")
        self.start_text = tk.Text(self.input_frame, height=2, width=50, wrap=tk.WORD)
        self.add_start_btn = ttk.Button(self.input_frame, text="Add Start Node",
                                      command=self.add_start_node)

        # Node type
        self.node_type_label = ttk.Label(self.input_frame, text="Node Type:")
        self.node_type_var = tk.StringVar(value="regular")
        self.regular_radio = ttk.Radiobutton(self.input_frame, text="Regular Step",
                                           variable=self.node_type_var, value="regular",
                                           command=self._on_node_type_change)
        self.merge_radio = ttk.Radiobutton(self.input_frame, text="Merge Step",
                                         variable=self.node_type_var, value="merge",
                                         command=self._on_node_type_change)

        # Next node text
        self.next_label = ttk.Label(self.input_frame,
                                  text="Enter text for the next step (1-2 lines):")
        self.next_text = tk.Text(self.input_frame, height=2, width=50, wrap=tk.WORD)

        # Connection selection
        self.connect_label = ttk.Label(self.input_frame, text="Connect from:")
        self.source_combo = ttk.Combobox(self.input_frame, state="readonly")

        self.merge_label1 = ttk.Label(self.input_frame, text="Merge Source 1:")
        self.merge_combo1 = ttk.Combobox(self.input_frame, state="readonly")
        self.merge_label2 = ttk.Label(self.input_frame, text="Merge Source 2:")
        self.merge_combo2 = ttk.Combobox(self.input_frame, state="readonly")

        # Direction
        self.direction_label = ttk.Label(self.input_frame, text="Connection direction:")
        self.direction_var = tk.StringVar(value="down")
        self.down_radio = ttk.Radiobutton(self.input_frame, text="Down",
                                        variable=self.direction_var, value="down")
        self.right_radio = ttk.Radiobutton(self.input_frame, text="Right",
                                         variable=self.direction_var, value="right")

        # Loop option
        self.is_loop_var = tk.BooleanVar()
        self.loop_check = ttk.Checkbutton(self.input_frame, text="Is this step part of a loop?",
                                        variable=self.is_loop_var, command=self._on_loop_change)
        self.loop_target_label = ttk.Label(self.input_frame, text="Loop to:")
        self.loop_target_combo = ttk.Combobox(self.input_frame, state="readonly")

        # Buttons
        self.add_step_btn = ttk.Button(self.input_frame, text="Add Step",
                                     command=self.add_step)
        self.end_label = ttk.Label(self.input_frame,
                                 text='Before clicking "Add End of Flowchart" choose the final step/s before the end step.',
                                 wraplength=400)
        self.end_combo = ttk.Combobox(self.input_frame, state="readonly")
        self.end_btn = ttk.Button(self.input_frame, text="Add End of Flowchart",
                                command=self.end_flowchart)
        self.delete_btn = ttk.Button(self.input_frame, text="Delete Last Step",
                                   command=self.delete_last)
        # Status bar for messages instead of popups
        self.status_frame = ttk.Frame(self.input_frame)
        self.status_label = ttk.Label(self.status_frame, text="Ready",
                                    relief="sunken", anchor="w",
                                    font=("TkDefaultFont", 9))
        self.status_label.pack(fill="x", padx=2, pady=2)

    def _create_output_widgets(self):
        """Create output panel widgets."""
        ttk.Label(self.output_frame, text="Generated Unicode Flowchart",
                 font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, pady=(0, 10))

        self.flowchart_display = scrolledtext.ScrolledText(
            self.output_frame, wrap=tk.NONE, width=120, height=25,
            font=("Consolas", 10), bg="#1e1e1e", fg="#33ff33"
        )
        self.flowchart_display.grid(row=1, column=0, sticky="nsew")
        self.flowchart_display.insert(tk.END, "The flowchart will appear here.")
        self.flowchart_display.config(state=tk.DISABLED)

        # Export buttons
        button_frame = ttk.Frame(self.output_frame)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        button_frame.grid_columnconfigure((0, 1), weight=1)

        ttk.Button(button_frame, text="Copy to Clipboard",
                  command=self.copy_to_clipboard).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(button_frame, text="Export to .txt",
                  command=self.export_to_txt).grid(row=0, column=1, padx=5, sticky="ew")

    def _bind_events(self):
        """Bind event handlers (already done in widget creation)."""
        pass

    def _update_ui_state(self):
        """Update UI based on current state."""
        # Hide all widgets first
        for widget in self.input_frame.winfo_children():
            widget.grid_forget()

        row = 0
        self.title_label.grid(row=row, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        row += 1

        if not self.nodes:
            # Start state
            self.start_label.grid(row=row, column=0, columnspan=2, pady=(10, 2), sticky="w")
            row += 1
            self.start_text.grid(row=row, column=0, columnspan=2, pady=(0, 5), sticky="ew")
            row += 1
            self.add_start_btn.grid(row=row, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        elif self.flowchart_ended:
            # Ended state
            ended_label = ttk.Label(self.input_frame, text="Flowchart completed!",
                                  font=("TkDefaultFont", 12), foreground="green")
            ended_label.grid(row=row, column=0, columnspan=2, pady=(20, 10), sticky="ew")
            row += 2
            self.delete_btn.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
            row += 1
            self.reset_btn.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")

        else:
            # Regular state
            self._show_regular_layout(row)

        self._update_combos()
        self._refresh_flowchart()

    def _show_regular_layout(self, start_row):
        """Show layout for adding regular nodes."""
        row = start_row

        # Node type
        self.node_type_label.grid(row=row, column=0, columnspan=2, pady=(10, 2), sticky="w")
        row += 1
        self.regular_radio.grid(row=row, column=0, sticky="w", padx=(0, 10))
        self.merge_radio.grid(row=row, column=1, sticky="w")
        row += 1

        # Next node text
        self.next_label.grid(row=row, column=0, columnspan=2, pady=(10, 2), sticky="w")
        row += 1
        self.next_text.grid(row=row, column=0, columnspan=2, pady=(0, 5), sticky="ew")
        row += 1

        # Connection selection
        if self.node_type_var.get() == "regular":
            self.connect_label.grid(row=row, column=0, columnspan=2, pady=(0, 2), sticky="w")
            row += 1
            self.source_combo.grid(row=row, column=0, columnspan=2, pady=(0, 5), sticky="ew")
            row += 1
        else:
            self.merge_label1.grid(row=row, column=0, pady=(0, 2), sticky="w")
            self.merge_combo1.grid(row=row, column=1, pady=(0, 5), sticky="ew")
            row += 1
            self.merge_label2.grid(row=row, column=0, pady=(0, 2), sticky="w")
            self.merge_combo2.grid(row=row, column=1, pady=(0, 5), sticky="ew")
            row += 1

        # Direction
        self.direction_label.grid(row=row, column=0, columnspan=2, pady=(10, 2), sticky="w")
        row += 1
        self.down_radio.grid(row=row, column=0, sticky="w", padx=(0, 10))
        self.right_radio.grid(row=row, column=1, sticky="w")
        row += 1

        # Loop option
        self.loop_check.grid(row=row, column=0, columnspan=2, pady=(10, 2), sticky="w")
        row += 1
        if self.is_loop_var.get():
            self.loop_target_label.grid(row=row, column=0, columnspan=2, pady=(0, 2), sticky="w")
            row += 1
            self.loop_target_combo.grid(row=row, column=0, columnspan=2, pady=(0, 5), sticky="ew")
            row += 1

        # Add step button
        self.add_step_btn.grid(row=row, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        row += 1

        # End section
        self.end_label.grid(row=row, column=0, columnspan=2, pady=(10, 2), sticky="w")
        row += 1
        self.end_combo.grid(row=row, column=0, columnspan=2, pady=(0, 5), sticky="ew")
        row += 1
        self.end_btn.grid(row=row, column=0, columnspan=2, pady=(10, 5), sticky="ew")
        row += 1
        self.delete_btn.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")
        row += 1
        self.reset_btn.grid(row=row, column=0, columnspan=2, pady=5, sticky="ew")

    def _update_combos(self):
        """Update combobox values."""
        connectable = [node for node in self.nodes if not node.is_end]
        options = [node.display_text() for node in connectable]

        # Update all combo boxes
        for combo in [self.source_combo, self.merge_combo1, self.merge_combo2, self.loop_target_combo]:
            combo['values'] = options
            if options and not combo.get():
                combo.set(options[-1])

        # End combo - unconnected nodes
        all_connected = set()
        for node in self.nodes:
            all_connected.update(node.connections)

        unconnected = [node for node in self.nodes if node.id not in all_connected and not node.is_end]
        end_options = [node.display_text() for node in unconnected]
        self.end_combo['values'] = [", ".join(end_options)] if end_options else []
        if end_options:
            self.end_combo.set(", ".join(end_options))

    def _on_node_type_change(self):
        """Handle node type change."""
        self._update_ui_state()

    def _on_loop_change(self):
        """Handle loop checkbox change."""
        self._update_ui_state()

    def _get_next_id(self) -> str:
        """Generate next node ID."""
        self.node_counter += 1
        return f"node-{self.node_counter}"

    def _extract_node_id(self, selection: str) -> str:
        """Extract node ID from combo selection."""
        try:
            return f"node-{selection.split('(ID: ')[1][:-1]}"
        except:
            return ""

    def _validate_text(self, text: str) -> List[str]:
        """Validate and process text input."""
        lines = [line.strip() for line in text.split('\n') if line.strip()][:2]
        if not lines:
            raise ValueError("Please enter text")

        for line in lines:
            if len(line) > self.MAX_LINE_LENGTH:
                raise ValueError(f"Line too long (max {self.MAX_LINE_LENGTH} chars): {line}")

        return lines

    def add_start_node(self):
        """Add start node."""
        try:
            text = self.start_text.get("1.0", tk.END).strip()
            lines = self._validate_text(text)

            node = Node(
                id=self._get_next_id(),
                text=lines,
                node_type=NodeType.REGULAR,
                connections=[]
            )

            self.nodes.append(node)
            self.start_text.delete("1.0", tk.END)
            self._update_ui_state()
            messagebox.showinfo("Success", f"Start node '{lines[0]}' added")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_step(self):
        """Add next step."""
        try:
            if self.flowchart_ended:
                raise ValueError("Flowchart already ended")

            text = self.next_text.get("1.0", tk.END).strip()
            lines = self._validate_text(text)

            # Get connections
            connections = []
            if self.node_type_var.get() == "regular":
                if not self.source_combo.get():
                    raise ValueError("Please select a source connection")
                connections.append(self._extract_node_id(self.source_combo.get()))
            else:  # merge
                if not self.merge_combo1.get() or not self.merge_combo2.get():
                    raise ValueError("Please select both merge sources")
                id1 = self._extract_node_id(self.merge_combo1.get())
                id2 = self._extract_node_id(self.merge_combo2.get())
                if id1 == id2:
                    raise ValueError("Merge sources must be different")
                connections.extend([id1, id2])

            # Get loop target if applicable
            loop_target = ""
            if self.is_loop_var.get():
                if not self.loop_target_combo.get():
                    raise ValueError("Please select loop target")
                loop_target = self.loop_target_combo.get().split(' (ID:')[0]

            node = Node(
                id=self._get_next_id(),
                text=lines,
                node_type=NodeType.MERGE if self.node_type_var.get() == "merge" else NodeType.REGULAR,
                connections=connections,
                direction=Direction.RIGHT if self.direction_var.get() == "right" else Direction.DOWN,
                is_loop=self.is_loop_var.get(),
                loop_target=loop_target
            )

            self.nodes.append(node)
            self.next_text.delete("1.0", tk.END)
            self.is_loop_var.set(False)
            self._update_ui_state()
            messagebox.showinfo("Success", f"Step '{lines[0]}' added")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def end_flowchart(self):
        """Add end node."""
        try:
            if self.flowchart_ended:
                raise ValueError("Flowchart already ended")

            if not self.nodes:
                raise ValueError("Add at least one node first")

            if not self.end_combo.get():
                raise ValueError("Please select steps to connect to 'End'")

            # Parse end connections
            selections = [s.strip() for s in self.end_combo.get().split(',')]
            connections = [self._extract_node_id(sel) for sel in selections]
            connections = [c for c in connections if c]  # Filter empty

            end_node = Node(
                id=self._get_next_id(),
                text=["End of Flowchart"],
                node_type=NodeType.REGULAR,
                connections=connections,
                is_end=True
            )

            self.nodes.append(end_node)
            self.flowchart_ended = True
            self._update_ui_state()
            messagebox.showinfo("Success", "End of Flowchart added")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_last(self):
        """Delete last node."""
        try:
            if len(self.nodes) <= 1:
                raise ValueError("Cannot delete the start node")

            deleted = self.nodes.pop()
            if deleted.is_end:
                self.flowchart_ended = False

            # Update counter
            if self.nodes:
                last_id = self.nodes[-1].id
                self.node_counter = int(last_id.split('-')[1])
            else:
                self.node_counter = 0

            self._update_ui_state()
            messagebox.showinfo("Success", f"Deleted '{deleted.text[0]}'")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def reset_flowchart(self):
        """Reset everything."""
        self.nodes.clear()
        self.node_counter = 0
        self.flowchart_ended = False

        # Clear inputs
        self.start_text.delete("1.0", tk.END)
        self.next_text.delete("1.0", tk.END)
        self.is_loop_var.set(False)
        self.node_type_var.set("regular")
        self.direction_var.set("down")

        self._update_ui_state()
        messagebox.showinfo("Success", "Flowchart reset")

    def _refresh_flowchart(self):
        """Refresh the flowchart display."""
        try:
            if not self.nodes:
                flowchart_text = "The flowchart will appear here."
            else:
                positions = self._calculate_positions()
                flowchart_text = self._render_flowchart(positions)

            self.flowchart_display.config(state=tk.NORMAL)
            self.flowchart_display.delete(1.0, tk.END)
            self.flowchart_display.insert(tk.END, flowchart_text)
            self.flowchart_display.config(state=tk.DISABLED)

        except Exception as e:
            self.flowchart_display.config(state=tk.NORMAL)
            self.flowchart_display.delete(1.0, tk.END)
            self.flowchart_display.insert(tk.END, f"Error rendering flowchart: {e}")
            self.flowchart_display.config(state=tk.DISABLED)

    def _calculate_positions(self) -> Dict[str, Tuple[int, int]]:
        """Calculate node positions - simplified algorithm."""
        if not self.nodes:
            return {}

        positions = {}
        y_offset = 0

        for i, node in enumerate(self.nodes):
            if i == 0:  # Start node
                positions[node.id] = (0, 0)
            else:
                # Simple positioning: stack vertically with some horizontal offset for branches
                if node.connections:
                    # Get source positions
                    source_positions = [positions.get(conn_id, (0, 0)) for conn_id in node.connections]

                    if len(source_positions) == 1:
                        src_x, src_y = source_positions[0]
                        if node.direction == Direction.RIGHT:
                            positions[node.id] = (src_x + self.NODE_WIDTH + self.H_SPACING, src_y)
                        else:
                            positions[node.id] = (src_x, src_y + self.NODE_HEIGHT + self.V_SPACING)
                    else:  # Merge node
                        # Position at center of sources
                        avg_x = sum(pos[0] for pos in source_positions) // len(source_positions)
                        max_y = max(pos[1] for pos in source_positions)
                        positions[node.id] = (avg_x, max_y + self.NODE_HEIGHT + self.V_SPACING)
                else:
                    positions[node.id] = (0, y_offset)

            # Avoid overlaps
            while any(self._positions_overlap(positions[node.id], pos)
                     for other_id, pos in positions.items() if other_id != node.id):
                x, y = positions[node.id]
                positions[node.id] = (x, y + 1)

        return positions

    def _positions_overlap(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """Check if two positions overlap."""
        x1, y1 = pos1
        x2, y2 = pos2
        return (abs(x1 - x2) < self.NODE_WIDTH and abs(y1 - y2) < self.NODE_HEIGHT)

    def _render_flowchart(self, positions: Dict[str, Tuple[int, int]]) -> str:
        """Render flowchart to text - simplified rendering."""
        if not positions:
            return "No nodes to render."

        grid = {}

        # Draw nodes
        for node in self.nodes:
            x, y = positions[node.id]
            self._draw_node_box(grid, x, y, node)

        # Draw connections
        for node in self.nodes:
            if node.connections:
                self._draw_connections(grid, positions, node)

        return self._grid_to_string(grid)

    def _draw_node_box(self, grid: Dict[Tuple[int, int], str], x: int, y: int, node: Node):
        """Draw a node box in the grid."""
        w, h = self.NODE_WIDTH, self.NODE_HEIGHT

        # Box corners and borders
        grid[(x, y)] = '┌'
        grid[(x + w - 1, y)] = '┐'
        grid[(x, y + h - 1)] = '└'
        grid[(x + w - 1, y + h - 1)] = '┘'

        # Horizontal lines
        for i in range(1, w - 1):
            grid[(x + i, y)] = '─'
            grid[(x + i, y + h - 1)] = '─'

        # Vertical lines
        for i in range(1, h - 1):
            grid[(x, y + i)] = '│'
            grid[(x + w - 1, y + i)] = '│'

        # Text content
        text_lines = list(node.text)
        if node.is_loop and node.loop_target:
            text_lines.append(f"*Loop to: {node.loop_target}")

        start_y = y + (h - len(text_lines)) // 2
        for line_idx, line in enumerate(text_lines):
            display_text = line[:w-2].center(w-2)
            for char_idx, char in enumerate(display_text):
                if char != ' ':
                    grid[(x + 1 + char_idx, start_y + line_idx)] = char

    def _draw_connections(self, grid: Dict[Tuple[int, int], str],
                         positions: Dict[str, Tuple[int, int]], node: Node):
        """Draw connections to a node."""
        target_x, target_y = positions[node.id]
        target_center_x = target_x + self.NODE_WIDTH // 2

        if len(node.connections) > 1:
            # Merge connections - draw convergence
            source_positions = [(positions[conn_id]) for conn_id in node.connections if conn_id in positions]
            if len(source_positions) > 1:
                # Draw horizontal merge line
                source_centers = [pos[0] + self.NODE_WIDTH // 2 for pos in source_positions]
                min_x, max_x = min(source_centers), max(source_centers)
                merge_y = target_y - (self.V_SPACING // 2) - 1

                for x in range(min_x, max_x + 1):
                    grid[(x, merge_y)] = '─'

                # Draw vertical lines from sources to merge line
                for i, (source_x, source_y) in enumerate(source_positions):
                    source_center_x = source_x + self.NODE_WIDTH // 2
                    for y in range(source_y + self.NODE_HEIGHT, merge_y):
                        grid[(source_center_x, y)] = '│'
                    grid[(source_center_x, merge_y)] = '┴'

                # Draw line from merge to target
                for y in range(merge_y + 1, target_y):
                    grid[(target_center_x, y)] = '│'
                grid[(target_center_x, target_y - 1)] = '▼'
        else:
            # Single connection
            for conn_id in node.connections:
                if conn_id in positions:
                    source_x, source_y = positions[conn_id]
                    source_center_x = source_x + self.NODE_WIDTH // 2

                    if node.direction == Direction.DOWN:
                        # Vertical connection
                        for y in range(source_y + self.NODE_HEIGHT, target_y):
                            grid[(source_center_x, y)] = '│'
                        if target_y > source_y + self.NODE_HEIGHT:
                            grid[(source_center_x, target_y - 1)] = '▼'
                    else:
                        # Horizontal connection
                        source_center_y = source_y + self.NODE_HEIGHT // 2
                        for x in range(source_x + self.NODE_WIDTH, target_x):
                            grid[(x, source_center_y)] = '─'
                        if target_x > source_x + self.NODE_WIDTH:
                            grid[(target_x - 1, source_center_y)] = '►'

    def _grid_to_string(self, grid: Dict[Tuple[int, int], str]) -> str:
        """Convert grid to string."""
        if not grid:
            return "Empty flowchart."

        max_x = max(pos[0] for pos in grid.keys())
        max_y = max(pos[1] for pos in grid.keys())

        lines = []
        for y in range(max_y + 1):
            line = ""
            for x in range(max_x + 1):
                line += grid.get((x, y), ' ')
            lines.append(line.rstrip())

        return '\n'.join(lines)

    def copy_to_clipboard(self):
        """Copy flowchart to clipboard."""
        try:
            content = self.flowchart_display.get("1.0", tk.END).strip()
            if content and content != "The flowchart will appear here.":
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                messagebox.showinfo("Success", "Copied to clipboard")
            else:
                messagebox.showwarning("Warning", "No content to copy")
        except Exception as e:
            messagebox.showerror("Error", f"Copy failed: {e}")

    def export_to_txt(self):
        """Export flowchart to text file."""
        try:
            content = self.flowchart_display.get("1.0", tk.END).strip()
            if not content or content == "The flowchart will appear here.":
                messagebox.showwarning("Warning", "No content to export")
                return

            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )

            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Exported to {filepath}")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    def run(self):
        """Run the application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    app = FlowchartBuilder()
    app.run()

if __name__ == "__main__":
    main()
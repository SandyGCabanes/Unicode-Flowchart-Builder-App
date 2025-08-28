# sandy.g.cabanes
# Title: Flowchart Builder
# Date: 2025-08-16
# ------------------------------------------------------------
"""
A GUI application using tkinter to build and display Unicode-based flowcharts.
Users can add steps with one or two lines of text, and the application
will generate a text-based visual representation that can be copied or exported.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import textwrap # NEW: Importing the textwrap module for automatic text wrapping

class FlowchartBuilderApp:
    # Defining a UNIFORM BOX SIZE for all nodes
    UNIFORM_NODE_WIDTH = 25 # Characters wide
    # Increased height to accommodate two lines of text + borders.
    UNIFORM_NODE_HEIGHT = 5 # Lines high - now has room for a third line of text for loop note
    VERTICAL_SPACING = 3 # Lines between nodes
    HORIZONTAL_SPACING = 7 # Characters between nodes

    def __init__(self, master):
        self.master = master
        master.title("Unicode Flowchart Builder")
        master.geometry("1200x700") # Setting a wider initial window size
        master.resizable(True, True) # Allowing resizing

        # Configuring grid for main window to allow resizing
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1) # Left panel weight
        master.grid_columnconfigure(1, weight=3) # Right panel weight

        self.nodes = []
        self.node_id_counter = 0
        self.flowchart_ended = False

        # --- Input Panel (Left Side) ---
        self.input_frame = ttk.Frame(master, padding="15", relief="groove", borderwidth=2)
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.input_frame.grid_rowconfigure(20, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.input_frame, text="Flowchart Builder", font=("TkDefaultFont", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="ew")

        # Initializing ALL widgets at the start
        self.lbl_start_node = ttk.Label(self.input_frame, text="1. Enter text for the start step:")
        self.start_node_text_input = tk.Text(self.input_frame, height=2, width=50, wrap=tk.WORD, font=("TkDefaultFont", 9))
        self.btn_add_start_node = ttk.Button(self.input_frame, text="Add Start Node", command=self.add_start_node)

        self.lbl_node_type_select = ttk.Label(self.input_frame, text="2. Choose Node Type:")
        self.node_type_var = tk.StringVar(value="regular")
        self.rb_regular_step = ttk.Radiobutton(self.input_frame, text="Regular Step", variable=self.node_type_var, value="regular", command=self._update_input_layout)
        self.rb_merge_step = ttk.Radiobutton(self.input_frame, text="Merge Step", variable=self.node_type_var, value="merge", command=self._update_input_layout)

        self.lbl_next_node = ttk.Label(self.input_frame, text="3. Enter text for the next step:")
        self.next_node_text_input = tk.Text(self.input_frame, height=2, width=50, wrap=tk.WORD, font=("TkDefaultFont", 9))

        # NEW: Adding a persistent label to inform the user about auto-wrapping.
        self.lbl_char_limit_note = ttk.Label(self.input_frame, text=f"(Max {self.UNIFORM_NODE_WIDTH - 4} chars per line - text will auto-wrap)", font=("TkDefaultFont", 8, "italic"))

        self.lbl_connect_to = ttk.Label(self.input_frame, text="4. Connect from which previous step?")
        self.source_node_combobox = ttk.Combobox(self.input_frame, state="readonly")
        self.lbl_merge_source1 = ttk.Label(self.input_frame, text="4a. Connect Source 1:")
        self.merge_source1_combobox = ttk.Combobox(self.input_frame, state="readonly")
        self.lbl_merge_source2 = ttk.Label(self.input_frame, text="4b. Connect Source 2:")
        self.merge_source2_combobox = ttk.Combobox(self.input_frame, state="readonly")
        self.lbl_branch_direction = ttk.Label(self.input_frame, text="5. How should the connection branch?")
        self.branch_direction_var = tk.StringVar(value="down")
        self.rb_down = ttk.Radiobutton(self.input_frame, text="Down", variable=self.branch_direction_var, value="down")
        self.rb_right = ttk.Radiobutton(self.input_frame, text="Right", variable=self.branch_direction_var, value="right")
        self.is_loop_var = tk.BooleanVar(value=False)
        self.chk_is_loop = ttk.Checkbutton(self.input_frame, text="Is this step part of a loop?", variable=self.is_loop_var, command=self._update_input_layout)
        self.lbl_loop_target = ttk.Label(self.input_frame, text="*Loop to:")
        self.loop_target_combobox = ttk.Combobox(self.input_frame, state="readonly")
        self.btn_add_step = ttk.Button(self.input_frame, text="Add Step", command=self.add_next_node)
        self.lbl_end_node_source = ttk.Label(self.input_frame, text='6. Before clicking "Add End of Flowchart", choose the step/s where to add the "End of Flowchart".', wraplength=400)
        self.end_node_combobox = ttk.Combobox(self.input_frame, state="readonly")
        self.btn_end_flowchart = ttk.Button(self.input_frame, text='Add "End of Flowchart"', command=self.end_flowchart, state=tk.DISABLED)

        self.btn_delete_last_step = ttk.Button(self.input_frame, text="Delete Last Step", command=self.delete_last_node, state=tk.DISABLED)
        self.btn_reset = ttk.Button(self.input_frame, text="Reset Flowchart", command=self.reset_flowchart)

        self.status_text_var = tk.StringVar(value="")
        self.status_bar = ttk.Label(self.input_frame, textvariable=self.status_text_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=21, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        self._update_input_layout()

        # --- Output Panel (Right Side) ---
        self.output_frame = ttk.Frame(master, padding="15", relief="groove", borderwidth=2)
        self.output_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.output_frame.grid_rowconfigure(1, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(self.output_frame, text="Generated Unicode Flowchart", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, pady=(0, 10), sticky="ew")
        self.flowchart_text = scrolledtext.ScrolledText(self.output_frame, wrap=tk.NONE, width=120, height=25, font=("Consolas", 10), bg="#1e1e1e", fg="#33ff33", insertbackground="#33ff33")
        self.flowchart_text.grid(row=1, column=0, sticky="nsew")
        self.flowchart_text.insert(tk.END, "Your flowchart will appear here.")
        self.flowchart_text.config(state=tk.DISABLED)

        self.output_actions_frame = ttk.Frame(self.output_frame)
        self.output_actions_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.output_actions_frame.grid_columnconfigure((0, 1), weight=1)
        self.btn_copy = ttk.Button(self.output_actions_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.btn_copy.grid(row=0, column=0, padx=5, sticky="ew")
        self.btn_export = ttk.Button(self.output_actions_frame, text="Export to .txt", command=self.export_to_txt)
        self.btn_export.grid(row=0, column=1, padx=5, sticky="ew")

    def _update_status(self, message, is_warning=False):
        """Displays a message in the status bar for a few seconds."""
        self.status_text_var.set(message)
        self.master.after(3000, lambda: self.status_text_var.set(""))

    def _update_input_layout(self):
        """
        Consolidates all layout logic into a single method.
        This method is called to show or hide widgets based on the current state.
        """
        for widget in self.input_frame.winfo_children():
            if widget.grid_info() and int(widget.grid_info().get('row', 0)) != 0:
                widget.grid_forget()

        current_row = 1
        if not self.nodes:
            self.lbl_start_node.grid(row=current_row, column=0, columnspan=2, pady=(10, 2), sticky="w"); current_row += 1
            self.start_node_text_input.grid(row=current_row, column=0, columnspan=2, pady=(0, 2), sticky="ew"); current_row += 1
            self.lbl_char_limit_note.grid(row=current_row, column=0, columnspan=2, pady=(0, 5), sticky="w"); current_row += 1
            self.btn_add_start_node.grid(row=current_row, column=0, columnspan=2, pady=(0, 10), sticky="ew"); current_row += 1
            self.btn_end_flowchart.config(state=tk.DISABLED)
        else:
            self.lbl_node_type_select.grid(row=current_row, column=0, columnspan=2, pady=(10, 2), sticky="w"); current_row += 1
            self.rb_regular_step.grid(row=current_row, column=0, sticky="w", padx=(0, 10))
            self.rb_merge_step.grid(row=current_row, column=1, sticky="w"); current_row += 1
            self.lbl_next_node.grid(row=current_row, column=0, columnspan=2, pady=(10, 2), sticky="w"); current_row += 1
            self.next_node_text_input.grid(row=current_row, column=0, columnspan=2, pady=(0, 2), sticky="ew"); current_row += 1
            self.lbl_char_limit_note.grid(row=current_row, column=0, columnspan=2, pady=(0, 5), sticky="w"); current_row += 1

            if self.node_type_var.get() == "regular":
                self.lbl_connect_to.grid(row=current_row, column=0, columnspan=2, pady=(0, 2), sticky="w"); current_row += 1
                self.source_node_combobox.grid(row=current_row, column=0, columnspan=2, pady=(0, 5), sticky="ew"); current_row += 1
                self.update_source_node_combobox(is_merge=False)
            else: # merge
                self.lbl_merge_source1.grid(row=current_row, column=0, pady=(0, 2), sticky="w")
                self.merge_source1_combobox.grid(row=current_row, column=1, pady=(0, 5), sticky="ew"); current_row += 1
                self.lbl_merge_source2.grid(row=current_row, column=0, pady=(0, 2), sticky="w")
                self.merge_source2_combobox.grid(row=current_row, column=1, pady=(0, 5), sticky="ew"); current_row += 1
                self.update_source_node_combobox(is_merge=True)

            self.lbl_branch_direction.grid(row=current_row, column=0, columnspan=2, pady=(10, 2), sticky="w"); current_row += 1
            self.rb_down.grid(row=current_row, column=0, sticky="w", padx=(0, 10))
            self.rb_right.grid(row=current_row, column=1, sticky="w"); current_row += 1
            self.chk_is_loop.grid(row=current_row, column=0, columnspan=2, pady=(10, 2), sticky="w"); current_row += 1

            if self.is_loop_var.get():
                self.lbl_loop_target.grid(row=current_row, column=0, columnspan=2, pady=(0, 2), sticky="w"); current_row += 1
                self.loop_target_combobox.grid(row=current_row, column=0, columnspan=2, pady=(0, 5), sticky="ew"); current_row += 1
                self.update_loop_target_combobox()

            self.btn_add_step.grid(row=current_row, column=0, columnspan=2, pady=(20, 10), sticky="ew"); current_row += 1
            self.lbl_end_node_source.grid(row=current_row, column=0, columnspan=2, pady=(10, 2), sticky="w"); current_row += 1
            self.end_node_combobox.grid(row=current_row, column=0, columnspan=2, pady=(0, 5), sticky="ew"); current_row += 1
            self.btn_end_flowchart.config(state=tk.NORMAL if not self.flowchart_ended else tk.DISABLED)

        self.btn_end_flowchart.grid(row=current_row + 1, column=0, columnspan=2, pady=(10, 5), sticky="ew")
        self.btn_delete_last_step.grid(row=current_row + 2, column=0, columnspan=2, pady=(5, 5), sticky="ew")
        self.btn_reset.grid(row=current_row + 3, column=0, columnspan=2, pady=(5, 0), sticky="ew")

        self._update_delete_button_state()
        self._update_end_node_combobox()

    def _update_delete_button_state(self):
        if len(self.nodes) > 1 and not self.flowchart_ended:
            self.btn_delete_last_step.config(state=tk.NORMAL)
        else:
            self.btn_delete_last_step.config(state=tk.DISABLED)

    # NEW: Helper function to wrap text to fit within node width.
    def _wrap_text(self, text, width):
        """Wraps text from a single string into a list of strings."""
        lines = text.split('\n')
        wrapped_lines = []
        for line in lines:
            # Using textwrap to handle wrapping long lines gracefully.
            wrapped_lines.extend(textwrap.wrap(line, width=width, break_long_words=True))
        return wrapped_lines

    def add_start_node(self):
        raw_text = self.start_node_text_input.get("1.0", tk.END).strip()

        # MODIFIED: Removed manual length check and implemented auto-wrapping.
        # The node box can comfortably fit 2 lines of text after wrapping.
        node_text_lines = self._wrap_text(raw_text, self.UNIFORM_NODE_WIDTH - 4)[:2]

        if not node_text_lines:
            self._update_status("Input Error: Please enter text for the start node.", is_warning=True)
            return

        self.node_id_counter += 1
        node_id = f"node-{self.node_id_counter}"
        self.nodes.append({
            "id": node_id, "text": node_text_lines, "type": "regular",
            "connections": [], "direction": None, "isLoop": False,
            "loopTarget": "", "is_end": False
        })
        self.start_node_text_input.delete("1.0", tk.END)
        self._update_input_layout()
        self.update_source_node_combobox()
        self._update_delete_button_state()
        self._update_end_node_combobox()
        self.generate_flowchart()
        self._update_status(f"Start node '{node_text_lines[0]}' added.")

    def add_next_node(self):
        if self.flowchart_ended:
            self._update_status("Flowchart Ended: Please reset to create a new one.", is_warning=True)
            return

        raw_text = self.next_node_text_input.get("1.0", tk.END).strip()
        # MODIFIED: Removed manual length check and implemented auto-wrapping.
        node_text_lines = self._wrap_text(raw_text, self.UNIFORM_NODE_WIDTH - 4)[:2]

        if not node_text_lines:
            self._update_status("Input Error: Please enter text for the next step.", is_warning=True)
            return

        connections = []
        if self.node_type_var.get() == "regular":
            selected_source_id_text = self.source_node_combobox.get()
            if not selected_source_id_text and self.nodes:
                self._update_status("Input Error: Please select a previous step to connect to.", is_warning=True)
                return
            parsed_source_id = self._parse_combobox_selection(selected_source_id_text)
            if parsed_source_id: connections.append(parsed_source_id)
        else: # merge
            s1_text = self.merge_source1_combobox.get(); s2_text = self.merge_source2_combobox.get()
            if not s1_text or not s2_text:
                self._update_status("Input Error: Please select both sources for the merge step.", is_warning=True)
                return
            p1_id = self._parse_combobox_selection(s1_text); p2_id = self._parse_combobox_selection(s2_text)
            if p1_id and p2_id: connections.extend([p1_id, p2_id])
            if p1_id == p2_id:
                self._update_status("Input Error: Merge sources must be distinct.", is_warning=True)
                return

        is_loop = self.is_loop_var.get()
        loop_target_text = ""
        if is_loop:
            loop_target_text = self.loop_target_combobox.get().strip()
            if not loop_target_text:
                 self._update_status("Input Error: Please choose the loop target text.", is_warning=True)
                 return
            loop_target_node_id = self._parse_combobox_selection(loop_target_text)
            loop_target_node = next((n for n in self.nodes if n['id'] == loop_target_node_id), None)
            if not loop_target_node:
                self._update_status(f"Input Error: Loop target '{loop_target_text}' does not match any existing step.", is_warning=True)
                return
            loop_target_text = loop_target_node['text'][0]

        self.node_id_counter += 1; node_id = f"node-{self.node_id_counter}"
        self.nodes.append({
            "id": node_id, "text": node_text_lines, "type": self.node_type_var.get(),
            "connections": connections, "direction": self.branch_direction_var.get(),
            "isLoop": is_loop, "loopTarget": loop_target_text, "is_end": False
        })
        self.next_node_text_input.delete("1.0", tk.END); self.is_loop_var.set(False);
        self._update_input_layout()
        self.update_source_node_combobox()
        self._update_delete_button_state()
        self._update_end_node_combobox()
        self.generate_flowchart()
        self._update_status(f"Step '{node_text_lines[0]}' added.")

    def delete_last_node(self):
        if len(self.nodes) == 1:
            self._update_status("Delete Error: The start node cannot be deleted.", is_warning=True)
            return

        last_node = self.nodes.pop()

        if last_node['is_end']:
            self.flowchart_ended = False
            for widget in [self.next_node_text_input, self.source_node_combobox, self.merge_source1_combobox, self.merge_source2_combobox, self.btn_add_step, self.rb_regular_step, self.rb_merge_step, self.chk_is_loop, self.loop_target_combobox]:
                widget.config(state=tk.NORMAL)
            for combo in [self.source_node_combobox, self.merge_source1_combobox, self.merge_source2_combobox, self.loop_target_combobox]:
                combo.config(state="readonly")
            self.btn_end_flowchart.config(state=tk.NORMAL)

        if self.nodes:
            self.node_id_counter = int(self.nodes[-1]['id'].split('-')[1])
        else:
            self.node_id_counter = 0

        self.update_source_node_combobox()
        self.update_loop_target_combobox()
        self._update_delete_button_state()
        self._update_end_node_combobox()
        self.generate_flowchart()
        self._update_status("Last step has been deleted.")

    def _parse_combobox_selection(self, selected_text):
        try: return "node-" + selected_text.split('(ID: ')[1][:-1]
        except IndexError: return None

    def end_flowchart(self):
        if self.flowchart_ended:
            self._update_status("Flowchart Ended: Flowchart already ended.", is_warning=True)
            return
        if not self.nodes:
            self._update_status("Cannot End: Please add at least one node.", is_warning=True)
            return

        selected_nodes_text = self.end_node_combobox.get()
        # MODIFIED: Removed the error check for an empty selection.
        # The application's logic pre-fills this combobox, so a user would
        # have to intentionally delete the content for it to be empty.
        # This change streamlines the process based on the expected workflow.

        selected_nodes_list = selected_nodes_text.split(', ')
        end_connections = [self._parse_combobox_selection(s) for s in selected_nodes_list if self._parse_combobox_selection(s)]

        if not end_connections:
            self._update_status("Input Error: No valid steps were selected to connect to 'End'.", is_warning=True)
            return

        self.node_id_counter += 1
        end_node_id = f"node-{self.node_id_counter}"
        self.nodes.append({
            "id": end_node_id, "text": ["End of Flowchart"], "type": "regular",
            "connections": end_connections, "direction": "down",
            "isLoop": False, "loopTarget": "", "is_end": True
        })
        self.flowchart_ended = True
        self._update_status("'End of Flowchart' step has been added.")
        for widget in [self.next_node_text_input, self.source_node_combobox, self.merge_source1_combobox, self.merge_source2_combobox, self.btn_add_step, self.btn_end_flowchart, self.rb_regular_step, self.rb_merge_step, self.chk_is_loop, self.loop_target_combobox, self.end_node_combobox]:
            widget.config(state=tk.DISABLED)

        self.generate_flowchart()
        self._update_delete_button_state()

    def update_source_node_combobox(self, is_merge=False):
        node_options = [f"{node['text'][0]} (ID: {node['id'].split('-')[1]})" for node in self.nodes if not node['is_end']]
        if is_merge:
            self.merge_source1_combobox['values'] = node_options; self.merge_source2_combobox['values'] = node_options
            if node_options:
                if len(node_options) >= 1: self.merge_source1_combobox.set(node_options[-1])
                if len(node_options) >= 2: self.merge_source2_combobox.set(node_options[-2])
                elif len(node_options) == 1: self.merge_source2_combobox.set(node_options[-1])
            else: self.merge_source1_combobox.set(""); self.merge_source2_combobox.set("")
        else:
            self.source_node_combobox['values'] = node_options
            if node_options: self.source_node_combobox.set(node_options[-1])
            else: self.source_node_combobox.set("")

    def update_loop_target_combobox(self):
        node_options = [f"{node['text'][0]} (ID: {node['id'].split('-')[1]})" for node in self.nodes if not node['is_end']]
        self.loop_target_combobox['values'] = node_options
        if node_options:
            self.loop_target_combobox.set(node_options[-1])
        else:
            self.loop_target_combobox.set("")

    def _update_end_node_combobox(self):
        all_source_ids = set(conn for node in self.nodes for conn in node['connections'])
        unconnected_node_options = [f"{node['text'][0]} (ID: {node['id'].split('-')[1]})" for node in self.nodes if node['id'] not in all_source_ids and not node['is_end']]
        self.end_node_combobox['values'] = unconnected_node_options
        self.end_node_combobox.set(", ".join(unconnected_node_options))

    def reset_flowchart(self):
        self.nodes = []; self.node_id_counter = 0; self.flowchart_ended = False
        self.start_node_text_input.delete("1.0", tk.END); self.next_node_text_input.delete("1.0", tk.END)
        self.is_loop_var.set(False); self.loop_target_combobox.set(""); self.node_type_var.set("regular")
        self.flowchart_text.config(state=tk.NORMAL)
        self.flowchart_text.delete(1.0, tk.END); self.flowchart_text.insert(tk.END, "Your flowchart will appear here.")
        self.flowchart_text.config(state=tk.DISABLED)
        for widget in [self.start_node_text_input, self.next_node_text_input, self.btn_add_step, self.rb_regular_step, self.rb_merge_step, self.chk_is_loop]:
             widget.config(state=tk.NORMAL)
        for combo in [self.source_node_combobox, self.merge_source1_combobox, self.merge_source2_combobox, self.loop_target_combobox, self.end_node_combobox]:
             combo.config(state="readonly")
        self.btn_end_flowchart.config(state=tk.DISABLED)
        self._update_input_layout()
        self.update_source_node_combobox()
        self.update_loop_target_combobox()
        self._update_delete_button_state()
        self._update_end_node_combobox()
        self._update_status("Flowchart has been reset.")

    def copy_to_clipboard(self):
        flowchart_content = self.flowchart_text.get("1.0", tk.END).strip()
        if flowchart_content and flowchart_content != "Your flowchart will appear here.":
            sanitized_content = flowchart_content.replace('\xa0', ' ')
            self.master.clipboard_clear()
            self.master.clipboard_append(sanitized_content)
            self._update_status("Flowchart content has been copied to the clipboard.")
        else:
            self._update_status("Empty: There is no flowchart to copy.", is_warning=True)

    def export_to_txt(self):
        flowchart_content = self.flowchart_text.get("1.0", tk.END).strip()
        if not flowchart_content or flowchart_content == "Your flowchart will appear here.":
            self._update_status("Empty: There is no flowchart to export.", is_warning=True)
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Save Flowchart As")
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f: f.write(flowchart_content)
                self._update_status(f"Flowchart successfully saved to:\n{filepath}")
            except Exception as e:
                self._update_status(f"Error: Failed to save file: {e}", is_warning=True)

    def generate_flowchart(self):
        if not self.nodes:
            self.flowchart_text.config(state=tk.NORMAL); self.flowchart_text.delete(1.0, tk.END)
            self.flowchart_text.insert(tk.END, "No nodes added yet. Start by adding a node!"); self.flowchart_text.config(state=tk.DISABLED)
            return

        node_positions = {}; max_x, max_y = 0, 0
        node_width, node_height = self.UNIFORM_NODE_WIDTH, self.UNIFORM_NODE_HEIGHT

        def is_overlapping(r1, r2): return not (r1['x'] + r1['width'] < r2['x'] or r1['x'] > r2['x'] + r2['width'] or r1['y'] + r1['height'] < r2['y'] or r1['y'] > r2['y'] + r2['height'])

        for node in self.nodes:
            x, y = 0, 0
            if not node['connections']: x, y = 0, 0
            else:
                sources_pos = [node_positions[s_id] for s_id in node['connections'] if s_id in node_positions]
                if not sources_pos: continue
                if node['type'] == 'merge' or (node['is_end'] and len(sources_pos) > 1):
                    avg_x = sum(p['x'] for p in sources_pos) // len(sources_pos); max_source_y = max(p['y'] + p['height'] for p in sources_pos)
                    x, y = avg_x, max_source_y + self.VERTICAL_SPACING
                else:
                    source_pos = sources_pos[0]
                    if node['direction'] == 'down': x, y = source_pos['x'], source_pos['y'] + source_pos['height'] + self.VERTICAL_SPACING
                    else: x, y = source_pos['x'] + source_pos['width'] + self.HORIZONTAL_SPACING, source_pos['y']

            new_node_rect = {'x': x, 'y': y, 'width': node_width, 'height': node_height}
            collided = True
            while collided:
                collided = False
                for placed_pos in node_positions.values():
                    if is_overlapping(new_node_rect, placed_pos): new_node_rect['y'] = placed_pos['y'] + placed_pos['height'] + 1; collided = True; break
            x, y = new_node_rect['x'], new_node_rect['y']
            node_positions[node['id']] = {'x': x, 'y': y, 'width': node_width, 'height': node_height, 'node': node}
            max_x = max(max_x, x + node_width); max_y = max(max_y, y + node_height)

        grid_height = max_y + 5; grid_width = max_x + self.HORIZONTAL_SPACING * 2 + 20
        grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]
        def draw_char(x, y, char):
            if 0 <= y < grid_height and 0 <= x < grid_width: grid[y][x] = char

        for pos_data in node_positions.values():
            x, y, w, h, node = pos_data['x'], pos_data['y'], pos_data['width'], pos_data['height'], pos_data['node']

            draw_char(x, y, '┌'); draw_char(x + w - 1, y, '┐'); draw_char(x, y + h - 1, '└'); draw_char(x + w - 1, y + h - 1, '┘')
            for i in range(1, w - 1): draw_char(x + i, y, '─'); draw_char(x + i, y + h - 1, '─')
            for i in range(1, h - 1): draw_char(x, y + i, '│'); draw_char(x + w - 1, y + i, '│')

            text_lines = node['text']
            if node['isLoop'] and node['loopTarget']:
                loop_note = f"*Loop to: {node['loopTarget']}"
                text_lines = text_lines + [loop_note]

            start_y = y + (h - len(text_lines)) // 2
            for line_num, line in enumerate(text_lines):
                display_text = line[:w-2].center(w-2)
                for i, char in enumerate(display_text):
                    draw_char(x + 1 + i, start_y + line_num, char)

            sources_pos = [node_positions[s_id] for s_id in node['connections'] if s_id in node_positions]
            if not sources_pos: continue

            target_x_center = x + w // 2
            if node['type'] == 'merge' or (node['is_end'] and len(sources_pos) > 1):
                merge_y = y - (self.VERTICAL_SPACING // 2) - 1
                min_sx = min(s['x'] + s['width'] // 2 for s in sources_pos); max_sx = max(s['x'] + s['width'] // 2 for s in sources_pos)
                for i in range(min_sx, max_sx + 1): draw_char(i, merge_y, '─')
                for s_pos in sources_pos:
                    sx_center = s_pos['x'] + s_pos['width'] // 2
                    for i in range(s_pos['y'] + h, merge_y): draw_char(sx_center, i, '│')
                    draw_char(sx_center, merge_y, '┴')
                for i in range(merge_y + 1, y): draw_char(target_x_center, i, '│')
                draw_char(target_x_center, y - 1, '▼')
            else:
                s_pos = sources_pos[0]
                sx_center, sy_center = s_pos['x'] + s_pos['width']//2, s_pos['y'] + h//2
                if node['direction'] == 'down':
                    for i in range(s_pos['y'] + h, y): draw_char(sx_center, i, '│'); draw_char(sx_center, y-1, '▼')
                else:
                    for i in range(s_pos['x'] + w, x): draw_char(i, sy_center, '─'); draw_char(x - 1, sy_center, '►')

        final_flowchart_text = "\n".join("".join(row) for row in grid)
        self.flowchart_text.config(state=tk.NORMAL); self.flowchart_text.delete(1.0, tk.END)
        self.flowchart_text.insert(tk.END, final_flowchart_text); self.flowchart_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = FlowchartBuilderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
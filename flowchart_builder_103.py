# sandy.g.cabanes
# Title:
# Date: September 9, 2025
# ------------------------------------------------------------
"""
Alternative code with classes: NodeType(Enum), Direction(Enum)
FlowchartBuilder: Model View Controller (MVC)
"""
# Streamlined Flowchart Builder
# No added abstraction layer and optimized version focusing on core functionality

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

SECTION UNDER CONSTRUCTION

def main():
    """Main entry point."""
    app = FlowchartBuilder()
    app.run()

if __name__ == "__main__":

    main()

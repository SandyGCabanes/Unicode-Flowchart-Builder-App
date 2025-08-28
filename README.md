# Unicode Flowchart Builder App
This project provides a GUI application for building and displaying Unicode-based flowcharts, allowing users to visually represent processes easily.

## Objective
The primary objective is to offer a user-friendly tool for generating simple flowcharts from textual inputs. It automates the layout and rendering of flowchart steps, eliminating the need for manual drawing or specialized software for basic diagramming needs.  The design emphasizes ease of use, allowing users to define steps, connect them, and indicate decision points or loops through an intuitive graphical interface.

## Automated Output from User Input
The application automatically constructs a text-based visual representation of the flowchart using Unicode characters based on user input. This output can be directly copied to the clipboard or exported as a .txt file, making it highly portable and compatible across various platforms and documents. The system handles node placement, connection lines, and basic branching logic to produce a clear and readable diagram based on user-defined steps and connections.  User inputs each step and specifies if it's a Regular Step or a Merge Step, source (Connect from which step), how the connection should branch (Down or Right arrow), and if it's part of a loop (Additional text box appears where it should loop to.)

### Background
I started creating lots of Unicode-based flowcharts for easy communication of workflows, code workflows, and data pipelines for my own use.  I decided to automate the process given the laborious process of creating flowcharts in draw.io and mermaid.  Both of these require a website to render the charts. My Unicode Flowchart Builder uses python's Tkinter library, addressing the need for a quick and accessible way to create flowcharts without complex tools. It's particularly useful for documenting processes, outlining algorithms, or illustrating workflows where a simple, shareable text-based diagram is enough. It's also effective with AI-assisted coding.  

### Managing Expectations
Design choice:  I decided to forgo the option to include arrows for loops.  Instead, I designed an option to insert text if the next step is part of a loop box. The text will indicate where the loop ends up.

**SGC. Beyond surveys. Data-driven decisions.**

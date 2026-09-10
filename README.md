# Unicode Flowchart Builder App
## Python

A lightweight, Tkinter-based GUI for creating Unicode flowcharts: no browser, no complex diagramming tools, just instant, portable text diagrams.

![Start UI](https://github.com/SandyGCabanes/Unicode-Flowchart-Builder-App/blob/main/flowchart_demo_full.gif)
---

## Problem
- Creating flowcharts in draw.io or Mermaid is slow and requires browser rendering.
- Needed a fast, shareable, text-based diagram format for workflows, algorithms, and pipelines.
- Unicode characters make diagrams portable. They work in plain text, emails, code comments, and documentation.

---

## Solution
- Build flowcharts from text input : no manual drawing.
- Automates layout : user defines steps, connections, and loops; the app handles spacing and alignment.
- Exports anywhere : copy to clipboard or save as `.txt` for universal compatibility.

---

## How It Works
1. Add Start button. Output is generated real-time on the right panel.
2. Add Steps  
   - Choose Regular Step or Merge Step  
   - Select source (1 for Regular, 2 for Merge step)
   - Select branch direction (Down, Right or Left)
   - Add Step
3. Handle Loops  
   - If part of a loop, add a label showing where it returns.
   - If need explicit arrow to loop back, add manually after exporting the file.
4. Delete step if needed
   - Only the latest step is allowed to be deleted
5. Add End step  
6. Export as text or copy to clipboard

---

## Design Choices
### These are the decisions I made to balance simplicity with usefulness.
- An input panel on the left with input fields, the output rendering on the right panel, real-time.
- No loop arrows, replaced with labeled loop text for simplicity and readability.
- Loop arrows can be hand-drawn into the exported .txt afterward, if a visual loop connector is wanted beyond the labeled text.
- Three arrow directions: Down, Right and Left only for simplicity.
- Merge step is included for two flows only.
- Delete step is allowed only for the most recent, to avoid orphan blocks.
- Portable output: `.txt` ensures diagrams survive copy-paste across platforms.
---

## Key Features
- GUI built with Tkinter — no external dependencies.
- Unicode-based rendering — works in any text environment.
- Loop-friendly — uses text labels instead of arrows that loop back for a clean look.
- Audit-friendly — output is plain text, easy to version-control.

---

## Example Use Cases
- Documenting code workflows.
- Outlining data pipelines.
- Creating process diagrams for reports.

---

## Background
Built to speed up workflow documentation and augment learning.  
Instead of wrestling with browser-based tools, this provides a local, instant, reproducible way to create diagrams that can live in:
- GitHub READMEs
- Audit documentation
- Plain-text project notes
- Understanding data pipelines

---

Block Diagram of [Workflow](https://github.com/SandyGCabanes/Unicode-Flowchart-Builder-App/blob/main/workflow.txt)



# 3D Geometry System Engine

An interactive, terminal-based Python utility designed to calculate the volumetric and surface area properties of 3D geometric shapes. The tool includes features for material weight estimation, multi-unit conversion matrices, a built-in formula reference guide, and session history exporting.

---

## Key Features

- **14 Supported Geometries:** Calculates volume, surface area, lateral area, and derived properties (e.g., slant heights, space diagonals, and circumferences).
- **Post-Calculation Tools:** 
  - Estimate material weight using 12 pre-configured material densities (like Steel, Aluminum, Concrete, Gold, and Oak).
  - Generate a multi-unit comparison table instantly.
- **Dimensional Converter:** Standalone utility to convert values across Length, Area, and Volume units (`mm`, `cm`, `m`, `in`, `ft`, `yd`, `liters`, `gallons`).
- **Interactive Formula Encyclopedia:** An on-demand mathematical dossier explaining the equations and variables for each shape.
- **Session History & Export:** Saves your calculations to an in-memory database and lets you export them to structured **JSON** or spreadsheet-ready **CSV** files.
- **Customizable Interface:** Toggle visual decimal precision (1 to 9 places), active measurement units, and ANSI color styles.

---

## Supported Shapes

| Polyhedrons & Prisms | Curved & Revolution Solids |
| :--- | :--- |
| - Cube / Cuboid | - Cylinder / Cone |
| - Regular Tetrahedron / Octahedron | - Sphere / Hemisphere |
| - Square Pyramid | - Truncated Cone (Frustum) |
| - Regular Triangular Prism | - Ellipsoid |
| - Regular Hexagonal Prism | - Torus |

---

## Getting Started

### Prerequisites
- Python 3.6 or higher.
- No external libraries required (uses only Python standard library modules: `math`, `os`, `sys`, `re`, `csv`, `json`, `datetime`).

### Running the Application

1. Clone or download this repository:
   ```
   git clone https://github.com/yourusername/geometry-system-engine.git
   cd geometry-system-engine
   ```

2. Run the script directly from your terminal:
   ```
   python main.py
   ```

*Note: On Windows systems, the utility automatically initializes VT100 terminal sequence support to display ANSI colors.*

---

## Console Interface Preview

```
┌────────────────────────────────────────────────────────────────────────┐
│                       3D GEOMETRY SYSTEM ENGINE                        │
├────────────────────────────────────────────────────────────────────────┤
│  Active Unit: cm  │  Precision: 4 decimals  │  Colors: ON              │
│  History Log: 0 calculations recorded                                  │
└────────────────────────────────────────────────────────────────────────┘

⚡ MAIN CONTROL CONSOLE
────────────────────────────────────────────────────────────────────────
 [1] Run 3D Shape Solver (14 Geometries)
 [2] Unit Quick-Converter (Length/Area/Volume)
 [3] Interactive Density & Weight Estimator (Standalone)
 [4] View Math Formulas & Theory
 [5] Show Calculation History Table
 [6] Export History Logs (CSV / JSON)
 [7] System Configurations
 [8] Exit System
────────────────────────────────────────────────────────────────────────
Enter menu action (1-8):
```

---

## Project Structure

- **Core Math Engine:** Handles formulation logic and mathematical constants (including Thomsen's ellipsoid constant).
- **UI Builders:** Contains grid tables and panel border logic constructed using box-drawing characters.
- **Conversion Utility:** Manages factors across metric and imperial systems.
- **Weight Management:** Translates volumetric units into mass units using material density variables.

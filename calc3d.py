import math
import os
import sys
import re
import csv
import json
import datetime

# --- Color Engine & Terminal Configuration ---

class Colors:
    ENABLED = True
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'
    
    @classmethod
    def disable(cls):
        cls.ENABLED = False
        cls.HEADER = ''
        cls.OKBLUE = ''
        cls.OKCYAN = ''
        cls.OKGREEN = ''
        cls.WARNING = ''
        cls.FAIL = ''
        cls.ENDC = ''
        cls.BOLD = ''
        cls.UNDERLINE = ''
        cls.GRAY = ''

    @classmethod
    def enable(cls):
        cls.ENABLED = True
        cls.HEADER = '\033[95m'
        cls.OKBLUE = '\033[94m'
        cls.OKCYAN = '\033[96m'
        cls.OKGREEN = '\033[92m'
        cls.WARNING = '\033[93m'
        cls.FAIL = '\033[91m'
        cls.ENDC = '\033[0m'
        cls.BOLD = '\033[1m'
        cls.UNDERLINE = '\033[4m'
        cls.GRAY = '\033[90m'

def init_terminal():
    """Forces Windows command prompts to interpret VT100 sequences."""
    if os.name == 'nt':
        try:
            os.system('')
        except Exception:
            pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# --- Utility Functions & Regex Helpers ---

def strip_ansi(text):
    """Filters ANSI characters so column layout calculations remain aligned."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

class GoBackException(Exception):
    """Custom exception allowing clean traversal back out of nested input paths."""
    pass

def get_validated_input(prompt_text, cast_type=float, validation_fn=None, allow_back=True):
    """Standardized validation loop with inline recovery and back routing."""
    while True:
        try:
            val = input(prompt_text).strip()
            if allow_back and val.lower() in ('b', 'back'):
                raise GoBackException()
            
            if not val:
                print(f"{Colors.WARNING}⚠️ Input cannot be empty. Try again.{Colors.ENDC}")
                continue
                
            casted = cast_type(val)
            if validation_fn and not validation_fn(casted):
                continue
            return casted
        except ValueError:
            if cast_type == float:
                print(f"{Colors.FAIL}❌ Invalid input. Please enter a valid number.{Colors.ENDC}")
            elif cast_type == int:
                print(f"{Colors.FAIL}❌ Invalid input. Please enter a valid integer.{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}❌ Invalid input format.{Colors.ENDC}")

def is_positive(val):
    if val <= 0:
        print(f"{Colors.WARNING}⚠️ Value must be greater than zero.{Colors.ENDC}")
        return False
    return True


# --- Custom UI Grid & Table Builders ---

def print_panel(title, content_lines, border_color=Colors.OKCYAN):
    """Generates dynamically sized Unicode border panels around list content."""
    raw_title = strip_ansi(title)
    max_len = max(len(strip_ansi(line)) for line in content_lines) if content_lines else 0
    max_len = max(max_len, len(raw_title) + 4)
    max_len = min(max_len, 76)
    
    print(border_color + "┌" + "─" * (max_len + 4) + "┐" + Colors.ENDC)
    
    if title:
        left_pad = (max_len + 4 - len(raw_title)) // 2
        right_pad = max_len + 4 - len(raw_title) - left_pad
        print(border_color + "│" + Colors.ENDC + " " * left_pad + Colors.BOLD + title + Colors.ENDC + " " * right_pad + border_color + "│" + Colors.ENDC)
        print(border_color + "├" + "─" * (max_len + 4) + "┤" + Colors.ENDC)
        
    for line in content_lines:
        line_len = len(strip_ansi(line))
        if line_len > max_len:
            truncated = line[:max_len+10] + "..."
            padding = " " * (max_len - len(strip_ansi(truncated)))
            print(border_color + "│" + Colors.ENDC + "  " + truncated + padding + "  " + border_color + "│" + Colors.ENDC)
        else:
            padding = " " * (max_len - line_len)
            print(border_color + "│" + Colors.ENDC + "  " + line + padding + "  " + border_color + "│" + Colors.ENDC)
            
    print(border_color + "└" + "─" * (max_len + 4) + "┘" + Colors.ENDC)

def print_table(headers, rows, alignments=None):
    """Draws custom aligned grid sheets utilizing box-drawing blocks."""
    col_widths = [len(strip_ansi(h)) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            if idx < len(col_widths):
                col_widths[idx] = max(col_widths[idx], len(strip_ansi(str(cell))))
            
    border_top = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    border_mid = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    border_bot = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
    
    print(Colors.GRAY + border_top + Colors.ENDC)
    
    header_line = "│"
    for idx, h in enumerate(headers):
        w = col_widths[idx]
        header_line += f" {Colors.BOLD}{Colors.OKCYAN}{h.center(w)}{Colors.ENDC} │"
    print(header_line)
    
    print(Colors.GRAY + border_mid + Colors.ENDC)
    
    for row in rows:
        row_line = "│"
        for idx, cell in enumerate(row):
            w = col_widths[idx]
            cell_str = str(cell)
            clean_cell = strip_ansi(cell_str)
            padding = w - len(clean_cell)
            
            align = alignments[idx] if alignments else 'L'
            if align == 'R':
                row_line += f" {padding * ' '}{cell_str} │"
            elif align == 'C':
                left_pad = padding // 2
                right_pad = padding - left_pad
                row_line += f" {left_pad * ' '}{cell_str}{right_pad * ' '} │"
            else:
                row_line += f" {cell_str}{padding * ' '} │"
        print(row_line)
        
    print(Colors.GRAY + border_bot + Colors.ENDC)


# --- Geometry Formulations Registry ---

# Knud Thomsen ellipsoid constant
THOMSEN_P = 1.6075

def calculate_shape(shape_id, params):
    """Core mathematical calculator returning (volume, total_sa, lateral_sa, derived_metrics)."""
    pi = math.pi
    derived = []
    
    if shape_id == "1":
        s = params["s"]
        volume = s ** 3
        sa = 6 * (s ** 2)
        la = 4 * (s ** 2)
        derived.append(("Face Area", s ** 2))
        derived.append(("Space Diagonal", s * (3 ** 0.5)))
        return volume, sa, la, derived
        
    elif shape_id == "2":
        l, w, h = params["l"], params["w"], params["h"]
        volume = l * w * h
        sa = 2 * (l * w + l * h + w * h)
        la = 2 * h * (l + w)
        derived.append(("Base Area", l * w))
        derived.append(("Space Diagonal", (l**2 + w**2 + h**2) ** 0.5))
        return volume, sa, la, derived
        
    elif shape_id == "3":
        r, h = params["r"], params["h"]
        slant = (r**2 + h**2) ** 0.5
        volume = (1/3) * pi * (r ** 2) * h
        sa = pi * r * (r + slant)
        la = pi * r * slant
        derived.append(("Slant Height (L)", slant))
        derived.append(("Base Area", pi * (r ** 2)))
        return volume, sa, la, derived
        
    elif shape_id == "4":
        R, r, h = params["R"], params["r"], params["h"]
        slant = (h**2 + (R - r)**2) ** 0.5
        volume = (1/3) * pi * h * (R**2 + R*r + r**2)
        sa = pi * (R**2 + r**2 + slant * (R + r))
        la = pi * slant * (R + r)
        derived.append(("Slant Height (L)", slant))
        derived.append(("Base Area", pi * (R ** 2)))
        derived.append(("Top Area", pi * (r ** 2)))
        return volume, sa, la, derived
        
    elif shape_id == "5":
        r = params["r"]
        volume = (4/3) * pi * (r ** 3)
        sa = 4 * pi * (r ** 2)
        la = None
        derived.append(("Diameter", 2 * r))
        derived.append(("Circumference", 2 * pi * r))
        return volume, sa, la, derived
        
    elif shape_id == "6":
        r = params["r"]
        volume = (2/3) * pi * (r ** 3)
        sa = 3 * pi * (r ** 2)
        la = 2 * pi * (r ** 2)
        derived.append(("Diameter", 2 * r))
        derived.append(("Base Surface Area", pi * (r ** 2)))
        return volume, sa, la, derived
        
    elif shape_id == "7":
        r, h = params["r"], params["h"]
        volume = pi * (r ** 2) * h
        sa = 2 * pi * r * (r + h)
        la = 2 * pi * r * h
        derived.append(("Base Area", pi * (r ** 2)))
        derived.append(("Circumference", 2 * pi * r))
        return volume, sa, la, derived
        
    elif shape_id == "8":
        b, h = params["b"], params["h"]
        slant = (h**2 + (b / 2)**2) ** 0.5
        volume = (1/3) * (b ** 2) * h
        sa = (b ** 2) + 2 * b * slant
        la = 2 * b * slant
        derived.append(("Slant Height (L)", slant))
        derived.append(("Base Area", b ** 2))
        return volume, sa, la, derived
        
    elif shape_id == "9":
        a = params["a"]
        volume = (a ** 3) * (2 ** 0.5) / 12
        sa = (a ** 2) * (3 ** 0.5)
        la = (a ** 2) * (3 ** 0.5) * 0.75
        derived.append(("Single Face Area", (3**0.5) / 4 * (a ** 2)))
        derived.append(("Altitude (Height)", a * (6**0.5) / 3))
        return volume, sa, la, derived
        
    elif shape_id == "10":
        a, h = params["a"], params["h"]
        base_area = ((3 ** 0.5) / 4) * (a ** 2)
        volume = base_area * h
        sa = 2 * base_area + 3 * a * h
        la = 3 * a * h
        derived.append(("Base Area", base_area))
        derived.append(("Base Perimeter", 3 * a))
        return volume, sa, la, derived
        
    elif shape_id == "11":
        a, h = params["a"], params["h"]
        base_area = (1.5 * (3 ** 0.5)) * (a ** 2)
        volume = base_area * h
        sa = 2 * base_area + 6 * a * h
        la = 6 * a * h
        derived.append(("Base Area", base_area))
        derived.append(("Base Perimeter", 6 * a))
        return volume, sa, la, derived
        
    elif shape_id == "12":
        a = params["a"]
        volume = ((2 ** 0.5) / 3) * (a ** 3)
        sa = 2 * (3 ** 0.5) * (a ** 2)
        la = None
        derived.append(("Single Face Area", (3**0.5) / 4 * (a ** 2)))
        return volume, sa, la, derived
        
    elif shape_id == "13":
        a, b, c = params["a"], params["b"], params["c"]
        volume = (4/3) * pi * a * b * c
        p = THOMSEN_P
        sa = 4 * pi * ((( (a*b)**p + (a*c)**p + (b*c)**p ) / 3) ** (1/p))
        la = None
        return volume, sa, la, derived
        
    elif shape_id == "14":
        R, r = params["R"], params["r"]
        volume = 2 * (pi ** 2) * R * (r ** 2)
        sa = 4 * (pi ** 2) * R * r
        la = None
        derived.append(("Tube Cross-section Area", pi * (r ** 2)))
        derived.append(("Inner Diameter", 2 * (R - r)))
        derived.append(("Outer Diameter", 2 * (R + r)))
        return volume, sa, la, derived

    return 0, 0, 0, []

def validate_shape_params(shape_id, params):
    if shape_id == "14":
        if params["R"] < params["r"]:
            print(f"{Colors.FAIL}❌ Validation Error: Major Radius (R) must be greater than or equal to Minor Radius (r).{Colors.ENDC}")
            return False
    if shape_id == "4":
        if params["R"] < params["r"]:
            print(f"{Colors.FAIL}❌ Validation Error: Bottom Radius (R) must be greater than or equal to Top Radius (r).{Colors.ENDC}")
            return False
    return True

def get_derived_unit(name, active_unit):
    name_lower = name.lower()
    if "area" in name_lower:
        return f"{active_unit}²"
    elif "volume" in name_lower:
        return f"{active_unit}³"
    else:
        lengths = ["height", "diagonal", "diameter", "circumference", "perimeter", "slant"]
        if any(l in name_lower for l in lengths):
            return active_unit
    return ""


# --- Unit Systems & Conversion Engines ---

CONVERSION_CATEGORIES = {
    "1": {
        "name": "Length",
        "units": ['mm', 'cm', 'm', 'in', 'ft', 'yd'],
        "factors": {
            'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144
        }
    },
    "2": {
        "name": "Area",
        "units": ['mm', 'cm', 'm', 'in', 'ft', 'yd'],
        "factors": {
            'mm': 1e-6, 'cm': 1e-4, 'm': 1.0, 'in': 0.00064516, 'ft': 0.09290304, 'yd': 0.83612736
        }
    },
    "3": {
        "name": "Volume",
        "units": ['mm', 'cm', 'm', 'in', 'ft', 'yd', 'liters', 'gallons'],
        "factors": {
            'mm': 1e-9, 'cm': 1e-6, 'm': 1.0, 'in': 1.6387064e-5, 'ft': 0.028316846592, 'yd': 0.764554857984,
            'liters': 0.001, 'gallons': 0.003785411784
        }
    }
}

def convert_value(val, category, unit_from, unit_to):
    factors = {
        'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144
    }
    f_from = factors[unit_from.lower()]
    f_to = factors[unit_to.lower()]
    ratio = f_from / f_to
    
    if category == 'length':
        return val * ratio
    elif category == 'area':
        return val * (ratio ** 2)
    elif category == 'volume':
        return val * (ratio ** 3)
    return val

def convert_volume_to_cm3(vol, unit):
    factors = {
        "mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.54, "ft": 30.48, "yd": 91.44
    }
    f = factors.get(unit.lower(), 1.0)
    return vol * (f ** 3)


# --- Material Weight Management ---

MATERIALS = {
    "1": ("Water (H2O)", 1.00),
    "2": ("Steel (Carbon)", 7.85),
    "3": ("Aluminum (Pure)", 2.70),
    "4": ("Gold (24k)", 19.30),
    "5": ("Copper (Structural)", 8.96),
    "6": ("Concrete (Standard)", 2.40),
    "7": ("Glass (Standard)", 2.50),
    "8": ("Oak Wood (Dry)", 0.75),
    "9": ("Ice (H2O)", 0.92),
    "10": ("Lead (Pure)", 11.34),
    "11": ("Titanium (Alloy)", 4.54),
    "12": ("Silver (Sterling)", 10.49),
}

def format_weight(weight_g):
    lines = []
    if weight_g >= 1000.0:
        lines.append(f"Kilograms (kg): {weight_g / 1000.0:,.4f}")
    lines.append(f"Grams (g): {weight_g:,.2f}")
    
    lbs = weight_g / 453.59237
    oz = weight_g / 28.349523125
    lines.append(f"Pounds (lbs): {lbs:,.4f}")
    lines.append(f"Ounces (oz): {oz:,.2f}")
    return lines


# --- Main Sub-Menu Pipelines ---

def run_weight_estimator(pre_calculated_vol=None, unit="cm"):
    """Dedicated module computing density scales and gravity masses."""
    clear_screen()
    print_panel("MATERIAL WEIGHT ESTIMATOR", [
        "Calculate structural weight based on volumetric metrics and density scaling.",
        "Compatible with standard metallurgical, geologic, and biochemical materials."
    ], border_color=Colors.OKGREEN)
    
    try:
        if pre_calculated_vol is None:
            vol_unit = get_validated_input(
                f"Enter volume unit (mm, cm, m, in, ft, yd) [default: {unit}]: ",
                cast_type=str,
                validation_fn=lambda u: u.lower() in ('mm', 'cm', 'm', 'in', 'ft', 'yd', '')
            )
            if not vol_unit:
                vol_unit = unit
                
            vol = get_validated_input(
                f"Enter the total Volume (in {vol_unit}³): ",
                cast_type=float,
                validation_fn=is_positive
            )
        else:
            vol = pre_calculated_vol
            vol_unit = unit
            
        print(f"\n{Colors.BOLD}Select Material Density Pattern:{Colors.ENDC}")
        print(f"{Colors.GRAY}────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
        for k, (name, density) in MATERIALS.items():
            print(f"  [{Colors.OKCYAN}{k.rjust(2)}{Colors.ENDC}] {name.ljust(22)} ({density:.2f} g/cm³)")
        print(f"{Colors.GRAY}────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
        
        choice = get_validated_input(
            "Select material option (1-12) or 'B' to abort: ",
            cast_type=str,
            validation_fn=lambda c: c in MATERIALS or c.lower() in ('b', 'back')
        )
        
        material_name, density = MATERIALS[choice]
        
        vol_cm3 = convert_volume_to_cm3(vol, vol_unit)
        weight_g = vol_cm3 * density
        
        weight_lines = format_weight(weight_g)
        
        panel_lines = [
            f"Shape Volume: {vol:,.4f} {vol_unit}³",
            f"Equivalent:   {vol_cm3:,.4f} cm³",
            f"Material:     {Colors.BOLD}{material_name}{Colors.ENDC} ({density} g/cm³)",
            "────────────────────────────────────────"
        ] + weight_lines
        
        print()
        print_panel("ESTIMATED TOTAL MASS & WEIGHT", panel_lines, border_color=Colors.OKGREEN)
        
        input(f"\n{Colors.GRAY}Press Enter to return...{Colors.ENDC}")
        return material_name, weight_g
    except GoBackException:
        return None, None

def show_unit_comparison(area, volume, unit_from, precision):
    """Prints dimension tables scaling original answers across all measurement standards."""
    clear_screen()
    print_panel("MULTI-UNIT COMPARISON TABLE", [
        f"Original values measured in {Colors.OKCYAN}{unit_from}{Colors.ENDC}:",
        f"Surface Area: {area:,.{precision}f} {unit_from}²",
        f"Volume:       {volume:,.{precision}f} {unit_from}³"
    ], border_color=Colors.OKBLUE)
    
    headers = ["Unit", "Surface Area", "Volume"]
    rows = []
    
    for u in ['mm', 'cm', 'm', 'in', 'ft', 'yd']:
        if u == unit_from:
            rows.append([
                f"{Colors.BOLD}{Colors.OKGREEN}{u} (Original){Colors.ENDC}",
                f"{Colors.BOLD}{Colors.OKGREEN}{area:,.{precision}f} {u}²{Colors.ENDC}",
                f"{Colors.BOLD}{Colors.OKGREEN}{volume:,.{precision}f} {u}³{Colors.ENDC}"
            ])
        else:
            conv_area = convert_value(area, 'area', unit_from, u)
            conv_vol = convert_value(volume, 'volume', unit_from, u)
            rows.append([
                u,
                f"{conv_area:,.{precision}f} {u}²",
                f"{conv_vol:,.{precision}f} {u}³"
            ])
            
    print_table(headers, rows, alignments=['L', 'R', 'R'])
    input(f"\n{Colors.GRAY}Press Enter to return...{Colors.ENDC}")


# --- Formulas Reference Book ---

FORMULAS_GUIDE = {
    "1": {
        "name": "Cube",
        "formulas": ["Volume (V) = s³", "Total Surface Area (SA) = 6 * s²", "Lateral Surface Area (LA) = 4 * s²"],
        "vars": ["s : Length of a side"],
        "desc": "A regular solid polyhedral shape with six congruent square faces."
    },
    "2": {
        "name": "Cuboid (Rectangular Prism)",
        "formulas": ["Volume (V) = l * w * h", "Total Surface Area (SA) = 2 * (l*w + l*h + w*h)", "Lateral Surface Area (LA) = 2 * h * (l + w)"],
        "vars": ["l : Length", "w : Width", "h : Height"],
        "desc": "A convex polyhedron bounded by six rectangular faces."
    },
    "3": {
        "name": "Cone",
        "formulas": ["Volume (V) = (1/3) * π * r² * h", "Total Surface Area (SA) = π * r * (r + L)", "Lateral Surface Area (LA) = π * r * L", "Slant Height (L) = √(r² + h²)"],
        "vars": ["r : Base radius", "h : Vertical height", "L : Slant height"],
        "desc": "A three-dimensional geometric shape tapering smoothly from a flat base to a point."
    },
    "4": {
        "name": "Truncated Cone (Frustum)",
        "formulas": ["Volume (V) = (1/3) * π * h * (R² + R*r + r²)", "Total Surface Area (SA) = π * (R² + r² + L * (R + r))", "Lateral Surface Area (LA) = π * L * (R + r)", "Slant Height (L) = √(h² + (R - r)²)"],
        "vars": ["R : Base bottom radius", "r : Top surface radius", "h : Vertical height", "L : Slant height"],
        "desc": "A cone with the top portion cut off parallel to the base."
    },
    "5": {
        "name": "Sphere",
        "formulas": ["Volume (V) = (4/3) * π * r³", "Total Surface Area (SA) = 4 * π * r²", "Lateral Surface Area (LA) = N/A"],
        "vars": ["r : Radius"],
        "desc": "A round geometrical object in three-dimensional space."
    },
    "6": {
        "name": "Hemisphere",
        "formulas": ["Volume (V) = (2/3) * π * r³", "Total Surface Area (SA) = 3 * π * r²  (solid base)", "Lateral Surface Area (LA) = 2 * π * r²  (curved area)"],
        "vars": ["r : Radius"],
        "desc": "Half of a sphere, bounded by a circular base."
    },
    "7": {
        "name": "Cylinder",
        "formulas": ["Volume (V) = π * r² * h", "Total Surface Area (SA) = 2 * π * r * (r + h)", "Lateral Surface Area (LA) = 2 * π * r * h"],
        "vars": ["r : Base radius", "h : Height"],
        "desc": "A three-dimensional solid with two congruent, parallel circular bases."
    },
    "8": {
        "name": "Square Pyramid",
        "formulas": ["Volume (V) = (1/3) * b² * h", "Total Surface Area (SA) = b² + 2 * b * L", "Lateral Surface Area (LA) = 2 * b * L", "Slant Height (L) = √(h² + (b/2)²)"],
        "vars": ["b : Base side length", "h : Height", "L : Slant height"],
        "desc": "A pyramid with a square base and four triangular lateral faces meeting at an apex."
    },
    "9": {
        "name": "Regular Tetrahedron",
        "formulas": ["Volume (V) = (a³ * √2) / 12", "Total Surface Area (SA) = a² * √3", "Lateral Surface Area (LA) = (3/4) * a² * √3"],
        "vars": ["a : Edge length"],
        "desc": "A triangular pyramid composed of four equilateral triangular faces."
    },
    "10": {
        "name": "Regular Triangular Prism",
        "formulas": ["Volume (V) = (√3 / 4) * a² * h", "Total Surface Area (SA) = (√3 / 2) * a² + 3*a*h", "Lateral Surface Area (LA) = 3 * a * h"],
        "vars": ["a : Base edge length", "h : Height (length of the prism)"],
        "desc": "A prism with two parallel equilateral triangular bases and three rectangular lateral faces."
    },
    "11": {
        "name": "Regular Hexagonal Prism",
        "formulas": ["Volume (V) = (3√3 / 2) * a² * h", "Total Surface Area (SA) = 3√3 * a² + 6*a*h", "Lateral Surface Area (LA) = 6 * a * h"],
        "vars": ["a : Base edge length", "h : Height"],
        "desc": "A prism with two parallel regular hexagonal bases and six rectangular lateral faces."
    },
    "12": {
        "name": "Regular Octahedron",
        "formulas": ["Volume (V) = (√2 / 3) * a³", "Total Surface Area (SA) = 2√3 * a²", "Lateral Surface Area (LA) = N/A"],
        "vars": ["a : Edge length"],
        "desc": "A regular polyhedron with eight equilateral triangular faces."
    },
    "13": {
        "name": "Ellipsoid",
        "formulas": ["Volume (V) = (4/3) * π * a * b * c", f"Total Surface Area (SA) ≈ 4π * ((( (ab)^p + (ac)^p + (bc)^p ) / 3) ^ (1/p))  [p={THOMSEN_P}]"],
        "vars": ["a : Semi-axis 1", "b : Semi-axis 2", "c : Semi-axis 3"],
        "desc": "A three-dimensional quadratic surface analogous to an ellipse."
    },
    "14": {
        "name": "Torus",
        "formulas": ["Volume (V) = 2 * π² * R * r²", "Total Surface Area (SA) = 4 * π² * R * r"],
        "vars": ["R : Major radius (center to tube center)", "r : Minor radius (radius of the tube)"],
        "desc": "A ring-shaped surface of revolution generated by rotating a circle in three-dimensional space."
    }
}

def run_formulas_guide():
    """Interactive dossier browsing geometric formulations."""
    while True:
        clear_screen()
        print_panel("GEOMETRIC FORMULA ENCYCLOPEDIA", [
            "Read exact mathematical formulations, derivations, and descriptions."
        ], border_color=Colors.OKCYAN)
        
        print(f"\n{Colors.BOLD}Select Shape to view Formulas:{Colors.ENDC}")
        print(f"{Colors.GRAY}────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
        
        shapes = list(FORMULAS_GUIDE.items())
        half = (len(shapes) + 1) // 2
        for i in range(half):
            left_id, left_data = shapes[i]
            left_str = f" [{Colors.OKCYAN}{left_id.rjust(2)}{Colors.ENDC}] {left_data['name']}"
            if i + half < len(shapes):
                right_id, right_data = shapes[i + half]
                right_str = f" [{Colors.OKCYAN}{right_id.rjust(2)}{Colors.ENDC}] {right_data['name']}"
                print(f"{left_str.ljust(45)}{right_str}")
            else:
                print(left_str)
                
        print(f"\n [{Colors.FAIL} B{Colors.ENDC}] Return to Main Console")
        print(f"{Colors.GRAY}────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
        
        try:
            choice = get_validated_input(
                "Enter option: ",
                cast_type=str,
                validation_fn=lambda c: c in FORMULAS_GUIDE or c.lower() in ("b", "back")
            )
            
            data = FORMULAS_GUIDE[choice]
            clear_screen()
            
            panel_lines = [
                f"{Colors.BOLD}Description:{Colors.ENDC} {data['desc']}",
                "──────────────────────────────────────────────────────────────────────",
                f"{Colors.BOLD}Equations & Formulas:{Colors.ENDC}"
            ]
            for formula in data["formulas"]:
                panel_lines.append(f"  • {formula}")
                
            panel_lines.append("──────────────────────────────────────────────────────────────────────")
            panel_lines.append(f"{Colors.BOLD}Variables Key:{Colors.ENDC}")
            for v in data["vars"]:
                panel_lines.append(f"  • {v}")
                
            print_panel(f"GEOMETRY DOSSIER: {data['name'].upper()}", panel_lines, border_color=Colors.OKCYAN)
            input(f"\n{Colors.GRAY}Press Enter to return to Encyclopedia...{Colors.ENDC}")
            
        except GoBackException:
            break


# --- Standalone Converter Submenu ---

def run_quick_converter():
    """Dynamic, category-driven dimensional conversion shell."""
    while True:
        clear_screen()
        print_panel("QUICK DIMENSIONAL CONVERTER", [
            "Convert values across dimensional units.",
            "Select measurement format category or return to the main console."
        ], border_color=Colors.OKBLUE)
        
        print(f"\n{Colors.BOLD}Select Conversion Type:{Colors.ENDC}")
        print(f" [1] Length")
        print(f" [2] Area")
        print(f" [3] Volume")
        print(f" [B] Back to Dashboard")
        
        try:
            choice = get_validated_input(
                "\nYour choice: ",
                cast_type=str,
                validation_fn=lambda c: c in ("1", "2", "3") or c.lower() in ("b", "back")
            )
            
            cat_data = CONVERSION_CATEGORIES[choice]
            units_list = cat_data["units"]
            factors = cat_data["factors"]
            cat_name = cat_data["name"]
            
            clear_screen()
            print_panel(f"{cat_name.upper()} CONVERSION UTILITY", [
                f"Supported units: {', '.join(units_list)}"
            ], border_color=Colors.OKBLUE)
            
            unit_from = get_validated_input(
                f"Enter source unit ({'/'.join(units_list)}): ",
                cast_type=str,
                validation_fn=lambda u: u.lower() in units_list
            ).lower()
            
            unit_to = get_validated_input(
                f"Enter target unit ({'/'.join(units_list)}): ",
                cast_type=str,
                validation_fn=lambda u: u.lower() in units_list
            ).lower()
            
            value = get_validated_input(
                f"Enter {cat_name} value: ",
                cast_type=float,
                validation_fn=lambda x: True
            )
            
            val_base = value * factors[unit_from]
            target_val = val_base / factors[unit_to]
            
            clear_screen()
            print_panel("CONVERSION RESULT", [
                f"Source: {value:,.4f} {unit_from}",
                f"Target: {Colors.BOLD}{Colors.OKGREEN}{target_val:,.6f} {unit_to}{Colors.ENDC}"
            ], border_color=Colors.OKGREEN)
            
            print(f"\n{Colors.BOLD}Equivalency Matrix:{Colors.ENDC}")
            headers = ["Unit", "Equivalent Value"]
            rows = []
            for u in units_list:
                eq_val = val_base / factors[u]
                if u == unit_to:
                    rows.append([
                        f"{Colors.BOLD}{Colors.OKGREEN}{u}{Colors.ENDC}",
                        f"{Colors.BOLD}{Colors.OKGREEN}{eq_val:,.6f}{Colors.ENDC}"
                    ])
                elif u == unit_from:
                    rows.append([
                        f"{Colors.BOLD}{Colors.OKBLUE}{u} (Source){Colors.ENDC}",
                        f"{Colors.BOLD}{Colors.OKBLUE}{eq_val:,.6f}{Colors.ENDC}"
                    ])
                else:
                    rows.append([u, f"{eq_val:,.6f}"])
            
            print_table(headers, rows, alignments=['L', 'R'])
            input(f"\n{Colors.GRAY}Press Enter to convert another or B to exit category...{Colors.ENDC}")
            
        except GoBackException:
            break


# --- Main Solver Logic & Core Controller ---

def run_post_calc_actions(shape_id, shape_name, inputs, vol, sa, la, derived, config, history):
    """Post-solving flow supporting weight lookups, scale matrices, and DB saves."""
    weight_log_str = "N/A"
    saved = False
    
    while True:
        clear_screen()
        p = config["precision"]
        u = config["unit"]
        
        results_lines = [
            f"Shape Geometry:       {Colors.BOLD}{shape_name}{Colors.ENDC}",
            "──────────────────────────────────────────────"
        ]
        
        dims_str = ", ".join(f"{k}={v:,.{p}f}" for k, v in inputs.items())
        results_lines.append(f"Input Parameters:     {dims_str} ({u})")
        results_lines.append(f"Calculated Volume:    {Colors.BOLD}{Colors.OKGREEN}{vol:,.{p}f}{Colors.ENDC} {u}³")
        results_lines.append(f"Total Surface Area:   {Colors.BOLD}{Colors.OKGREEN}{sa:,.{p}f}{Colors.ENDC} {u}²")
        
        if la is not None:
            results_lines.append(f"Lateral Surface Area: {la:,.{p}f} {u}²")
            
        if derived:
            results_lines.append("──────────────────────────────────────────────")
            results_lines.append("Derived Metrics:")
            for key, val in derived:
                unit_str = get_derived_unit(key, u)
                results_lines.append(f"  • {key.ljust(22)}: {val:,.{p}f} {unit_str}")
                
        if weight_log_str != "N/A":
            results_lines.append("──────────────────────────────────────────────")
            results_lines.append(f"Estimated Weight:     {Colors.BOLD}{Colors.OKCYAN}{weight_log_str}{Colors.ENDC}")
            
        if saved:
            results_lines.append(f"Status:               {Colors.BOLD}{Colors.OKGREEN}✔ Saved to History Log{Colors.ENDC}")
            
        print_panel("CALCULATION DETAILED RESOLUTION", results_lines, border_color=Colors.OKGREEN)
        
        print(f"\n{Colors.BOLD}Choose Post-Calculation Option:{Colors.ENDC}")
        print(f" [1] Estimate Material Mass / Weight of this shape")
        print(f" [2] Run Comprehensive Multi-Unit Comparison Matrix")
        print(f" [3] Save Calculation Session to History Database")
        print(f" [B] Back to Solver Menu")
        
        try:
            choice = get_validated_input(
                "\nSelect option: ",
                cast_type=str,
                validation_fn=lambda c: c in ("1", "2", "3") or c.lower() in ("b", "back")
            )
            
            if choice == "1":
                mat, weight_g = run_weight_estimator(pre_calculated_vol=vol, unit=u)
                if mat and weight_g:
                    if weight_g >= 1000.0:
                        weight_log_str = f"{weight_g / 1000.0:,.3f} kg ({mat})"
                    else:
                        weight_log_str = f"{weight_g:,.2f} g ({mat})"
                        
            elif choice == "2":
                show_unit_comparison(sa, vol, u, p)
                
            elif choice == "3":
                if saved:
                    print(f"\n{Colors.WARNING}⚠ This calculation is already recorded in history.{Colors.ENDC}")
                    input(f"{Colors.GRAY}Press Enter to continue...{Colors.ENDC}")
                    continue
                    
                label = input(f"\nEnter custom record label/name (e.g. 'Support Pillar') or press Enter: ").strip()
                label_str = f" [{label}]" if label else ""
                
                history_entry = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "shape": shape_name + label_str,
                    "inputs": ", ".join(f"{k}={v:,.{p}f}" for k, v in inputs.items()),
                    "volume": vol,
                    "surface_area": sa,
                    "lateral_area": la if la is not None else 0.0,
                    "unit": u,
                    "mass_info": weight_log_str
                }
                history.append(history_entry)
                saved = True
                print(f"\n{Colors.OKGREEN}✔ Recorded successfully!{Colors.ENDC}")
                input(f"{Colors.GRAY}Press Enter to continue...{Colors.ENDC}")
                
        except GoBackException:
            break

def run_shape_solver_menu(config, history):
    """Dynamic form builder loading shapes, inputs, and validation properties."""
    while True:
        clear_screen()
        print_panel("3D GEOMETRICAL SOLVER ENGINE", [
            "Select a three-dimensional polygon model to compute metrics.",
            f"Input values are assumed to be in the active unit: {Colors.OKGREEN}{config['unit']}{Colors.ENDC}."
        ], border_color=Colors.OKBLUE)
        
        print(f"{Colors.BOLD}Select Geometry Model:{Colors.ENDC}")
        print(f"{Colors.GRAY}────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
        shapes = [
            ("1", "Cube"), ("8", "Square Pyramid"),
            ("2", "Cuboid (Rect Prism)"), ("9", "Regular Tetrahedron"),
            ("3", "Cone"), ("10", "Regular Triangular Prism"),
            ("4", "Truncated Cone (Frustum)"), ("11", "Regular Hexagonal Prism"),
            ("5", "Sphere"), ("12", "Regular Octahedron"),
            ("6", "Hemisphere"), ("13", "Ellipsoid"),
            ("7", "Cylinder"), ("14", "Torus")
        ]
        
        half = 7
        for i in range(half):
            left_id, left_name = shapes[i]
            right_id, right_name = shapes[i + half]
            left_str = f" [{Colors.OKCYAN}{left_id.rjust(2)}{Colors.ENDC}] {left_name}"
            right_str = f" [{Colors.OKCYAN}{right_id.rjust(2)}{Colors.ENDC}] {right_name}"
            print(f"{left_str.ljust(45)}{right_str}")
            
        print(f"\n [{Colors.FAIL} B{Colors.ENDC}] Return to Main Console")
        print(f"{Colors.GRAY}────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
        
        try:
            choice = get_validated_input(
                "Enter option: ",
                cast_type=str,
                validation_fn=lambda c: c in [str(i) for i in range(1, 15)] or c.lower() in ("b", "back")
            )
            
            shape_name = FORMULAS_GUIDE[choice]["name"]
            
            shape_params_def = {
                "1": [("s", "Enter side length (s): ")],
                "2": [("l", "Enter length (l): "), ("w", "Enter width (w): "), ("h", "Enter height (h): ")],
                "3": [("r", "Enter base radius (r): "), ("h", "Enter vertical height (h): ")],
                "4": [("R", "Enter bottom base radius (R): "), ("r", "Enter top base radius (r): "), ("h", "Enter height (h): ")],
                "5": [("r", "Enter sphere radius (r): ")],
                "6": [("r", "Enter hemisphere radius (r): ")],
                "7": [("r", "Enter cylinder radius (r): "), ("h", "Enter height (h): ")],
                "8": [("b", "Enter base edge length (b): "), ("h", "Enter vertical height (h): ")],
                "9": [("a", "Enter regular edge length (a): ")],
                "10": [("a", "Enter base triangular edge (a): "), ("h", "Enter height/length (h): ")],
                "11": [("a", "Enter base hexagonal edge (a): "), ("h", "Enter height (h): ")],
                "12": [("a", "Enter regular edge length (a): ")],
                "13": [("a", "Enter semi-axis a: "), ("b", "Enter semi-axis b: "), ("c", "Enter semi-axis c: ")],
                "14": [("R", "Enter major radius (R): "), ("r", "Enter minor radius (r): ")]
            }
            
            clear_screen()
            print_panel(f"GEOMETRY INPUT MATRIX: {shape_name.upper()}", [
                f"Active Unit: {config['unit']}",
                "Type 'B' or 'back' at any prompt to cancel."
            ], border_color=Colors.OKCYAN)
            
            inputs = {}
            for param_key, prompt_msg in shape_params_def[choice]:
                inputs[param_key] = get_validated_input(
                    prompt_msg,
                    cast_type=float,
                    validation_fn=is_positive
                )
                
            if not validate_shape_params(choice, inputs):
                input(f"\n{Colors.GRAY}Validation failed. Press Enter to retry...{Colors.ENDC}")
                continue
                
            vol, sa, la, derived = calculate_shape(choice, inputs)
            run_post_calc_actions(choice, shape_name, inputs, vol, sa, la, derived, config, history)
            
        except GoBackException:
            break


# --- Session History & Exporters ---

def show_history_menu(history, precision):
    """Prints and manages stored session records."""
    while True:
        clear_screen()
        if not history:
            print_panel("CALCULATION HISTORY LOG", [
                "The history database is currently empty.",
                "Solve shape dimensions to record entries automatically."
            ], border_color=Colors.WARNING)
            input(f"\n{Colors.GRAY}Press Enter to return to Main Console...{Colors.ENDC}")
            break
            
        print_panel("CALCULATION HISTORY LOG", [
            f"Displaying {len(history)} stored entries.",
            "Type 'clear' to purge the database, or press Enter to return."
        ], border_color=Colors.OKBLUE)
        
        headers = ["ID", "Shape Name", "Inputs", f"Volume ({history[0]['unit']}³)", f"Surface Area ({history[0]['unit']}²)"]
        rows = []
        for idx, entry in enumerate(history, 1):
            rows.append([
                str(idx),
                entry["shape"],
                entry["inputs"],
                f"{entry['volume']:,.{precision}f}",
                f"{entry['surface_area']:,.{precision}f}"
            ])
            
        print_table(headers, rows, alignments=['C', 'L', 'L', 'R', 'R'])
        
        action = input(f"\nType {Colors.FAIL}'clear'{Colors.ENDC} to purge all, or press {Colors.BOLD}Enter{Colors.ENDC} to go back: ").strip().lower()
        if action == 'clear':
            history.clear()
            print(f"{Colors.OKGREEN}✔ History cleared successfully!{Colors.ENDC}")
            input(f"{Colors.GRAY}Press Enter to continue...{Colors.ENDC}")
            break
        else:
            break

def export_history(history):
    """Outputs stored history buffers into localized CSV or parsed JSON structures."""
    if not history:
        clear_screen()
        print_panel("LOG EXPORTER", [
            "Export failed: History log is empty.",
            "Run calculations before attempting to export data."
        ], border_color=Colors.FAIL)
        input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.ENDC}")
        return
        
    while True:
        clear_screen()
        print_panel("DATA EXPORT ENGINE", [
            "Save session logs to the current workspace.",
            "Choose a structured file format to proceed:"
        ], border_color=Colors.OKBLUE)
        
        print(f" [1] Export to JSON (Highly detailed, structured)")
        print(f" [2] Export to CSV (Spreadsheet compatible)")
        print(f" [B] Back to Main Console")
        
        try:
            choice = get_validated_input(
                "\nSelect Export Format: ",
                cast_type=str,
                validation_fn=lambda c: c in ("1", "2") or c.lower() in ("b", "back")
            )
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if choice == "1":
                filename = f"geometry_history_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(history, f, indent=4)
                full_path = os.path.abspath(filename)
                
                clear_screen()
                print_panel("EXPORT SUCCESSFUL", [
                    f"Format: JSON",
                    f"File Name: {filename}",
                    f"Full Path:",
                    f"{Colors.OKGREEN}{full_path}{Colors.ENDC}"
                ], border_color=Colors.OKGREEN)
                input(f"\n{Colors.GRAY}Press Enter to return...{Colors.ENDC}")
                break
                
            elif choice == "2":
                filename = f"geometry_history_{timestamp}.csv"
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Index", "Timestamp", "Shape", "Inputs", "Unit", "Volume", "Surface Area", "Lateral Area", "Weight Log"])
                    for idx, entry in enumerate(history, 1):
                        writer.writerow([
                            idx,
                            entry.get("timestamp", ""),
                            entry.get("shape", ""),
                            entry.get("inputs", ""),
                            entry.get("unit", ""),
                            entry.get("volume", 0.0),
                            entry.get("surface_area", 0.0),
                            entry.get("lateral_area", 0.0),
                            entry.get("mass_info", "N/A")
                        ])
                full_path = os.path.abspath(filename)
                
                clear_screen()
                print_panel("EXPORT SUCCESSFUL", [
                    f"Format: CSV",
                    f"File Name: {filename}",
                    f"Full Path:",
                    f"{Colors.OKGREEN}{full_path}{Colors.ENDC}"
                ], border_color=Colors.OKGREEN)
                input(f"\n{Colors.GRAY}Press Enter to return...{Colors.ENDC}")
                break
                
        except GoBackException:
            break


# --- Configurations & Console Panel ---

def run_config_menu(config):
    """Visual panel managing display precision, units, and ANSI features."""
    while True:
        clear_screen()
        print_panel("SYSTEM CONFIGURATION MATRIX", [
            f"1. Active Measurement Unit:  {Colors.OKGREEN}{config['unit']}{Colors.ENDC}",
            f"2. Decimal Float Precision: {Colors.OKGREEN}{config['precision']} places{Colors.ENDC}",
            f"3. ANSI Visual Styling:     {Colors.OKGREEN}{'ENABLED' if config['colors'] else 'DISABLED'}{Colors.ENDC}"
        ], border_color=Colors.OKBLUE)
        
        print(f" [1] Change Active Unit (mm, cm, m, in, ft, yd)")
        print(f" [2] Edit Display Precision (1 - 9 decimal places)")
        print(f" [3] Toggle ANSI Graphic Colors")
        print(f" [B] Save & Return")
        
        try:
            choice = get_validated_input(
                "\nSelect field to update: ",
                cast_type=str,
                validation_fn=lambda c: c in ("1", "2", "3") or c.lower() in ("b", "back")
            )
            
            if choice == "1":
                units = ['mm', 'cm', 'm', 'in', 'ft', 'yd']
                new_unit = get_validated_input(
                    f"Choose active unit ({'/'.join(units)}): ",
                    cast_type=str,
                    validation_fn=lambda u: u.lower() in units
                ).lower()
                config["unit"] = new_unit
                
            elif choice == "2":
                new_prec = get_validated_input(
                    "Set visual decimal places (1 - 9): ",
                    cast_type=int,
                    validation_fn=lambda p: 1 <= p <= 9
                )
                config["precision"] = new_prec
                
            elif choice == "3":
                config["colors"] = not config["colors"]
                if config["colors"]:
                    Colors.enable()
                    print(f"{Colors.OKGREEN}✔ System styles set to: Full ANSI Color{Colors.ENDC}")
                else:
                    Colors.disable()
                    print("✔ System styles set to: Monochromatic Plaintext")
                input(f"\n{Colors.GRAY}Style configuration updated. Press Enter...{Colors.ENDC}")
                
        except GoBackException:
            break

def print_dashboard(config, history_len):
    clear_screen()
    print_panel(
        "3D GEOMETRY SYSTEM ENGINE",
        [
            f"Active Unit: {Colors.OKGREEN}{config['unit']}{Colors.ENDC}  │  Precision: {Colors.OKGREEN}{config['precision']} decimals{Colors.ENDC}  │  Colors: {Colors.OKGREEN}{'ON' if config['colors'] else 'OFF'}{Colors.ENDC}",
            f"History Log: {Colors.OKGREEN}{history_len} calculations recorded{Colors.ENDC}",
        ],
        border_color=Colors.OKBLUE
    )
    
    print(f"\n{Colors.BOLD}⚡ MAIN CONTROL CONSOLE{Colors.ENDC}")
    print(f"{Colors.GRAY}────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
    print(f" {Colors.OKCYAN}[1]{Colors.ENDC} Run 3D Shape Solver (14 Geometries)")
    print(f" {Colors.OKCYAN}[2]{Colors.ENDC} Unit Quick-Converter (Length/Area/Volume)")
    print(f" {Colors.OKCYAN}[3]{Colors.ENDC} Interactive Density & Weight Estimator (Standalone)")
    print(f" {Colors.OKCYAN}[4]{Colors.ENDC} View Math Formulas & Theory")
    print(f" {Colors.OKCYAN}[5]{Colors.ENDC} Show Calculation History Table")
    print(f" {Colors.OKCYAN}[6]{Colors.ENDC} Export History Logs (CSV / JSON)")
    print(f" {Colors.OKCYAN}[7]{Colors.ENDC} System Configurations")
    print(f" {Colors.OKCYAN}[8]{Colors.ENDC} Exit System")
    print(f"{Colors.GRAY}────────────────────────────────────────────────────────────────────────{Colors.ENDC}")


# --- System Initialization & Event Loop ---

def main():
    init_terminal()
    history = []
    config = {
        "unit": "cm",
        "precision": 4,
        "colors": True
    }
    
    while True:
        print_dashboard(config, len(history))
        try:
            choice = get_validated_input(
                "Enter menu action (1-8): ",
                cast_type=str,
                validation_fn=lambda c: c in [str(i) for i in range(1, 9)] or c.lower() in ("e", "exit")
            )
            
            if choice == "1":
                run_shape_solver_menu(config, history)
            elif choice == "2":
                run_quick_converter()
            elif choice == "3":
                run_weight_estimator(unit=config["unit"])
            elif choice == "4":
                run_formulas_guide()
            elif choice == "5":
                show_history_menu(history, config["precision"])
            elif choice == "6":
                export_history(history)
            elif choice == "7":
                run_config_menu(config)
            elif choice in ("8", "e", "exit"):
                clear_screen()
                print_panel("SYSTEM SHUTDOWN", [
                    "Exiting Advanced 3D Shape Solver.",
                    "Session closed. Goodbye!"
                ], border_color=Colors.OKCYAN)
                break
                
        except GoBackException:
            continue

if __name__ == "__main__":
    main()

# ====================================================================================
# 3D SHAPE CALCULATOR
# ====================================================================================
# This program calculates the surface area and volume of various 3D shapes.
# It will ask the user to choose a shape, enter its dimensions, and then
# it will display the calculated results.
# ====================================================================================

# We need the 'math' module, but only to get the precise value of Pi (π).
import math

# --- Helper Function ---

def get_pi():
    """
    A simple function that just returns the value of Pi.
    We created a function for this to follow the user's request of only using
    the 'math' module for Pi and nothing else inside the calculation functions.
    """
    return math.pi

# --- Shape Calculation Functions ---
# Each function below is responsible for one shape. It handles:
# 1. Getting input from the user.
# 2. Calculating the surface area and volume.
# 3. Printing the final results.

def calculate_cube():
    """Calculates the surface area and volume of a cube."""
    # A 'try...except' block is used for error handling.
    # We will 'try' to run the code inside this block.
    try:
        # Ask the user for the side length and convert the input string to a number (float).
        side = float(input("Enter the side length of the cube: "))

        # --- Formulas for a Cube ---
        # Surface Area = 6 * (side * side)
        # Volume = side * side * side
        surface_area = 6 * side**2  # Using **2 is the same as side * side
        volume = side**3            # Using **3 is the same as side * side * side

        # Print the results. The f-string formats the output nicely.
        # The ':.2f' part means "format this number as a float with 2 decimal places".
        print(f"\nSurface Area of the cube is: {surface_area:.2f}")
        print(f"Volume of the cube is: {volume:.2f}")

    # If the user enters something that is not a number (like "hello"),
    # a 'ValueError' will happen, and the code inside 'except' will run.
    except ValueError:
        print("\nError: Invalid input. Please enter a number for the side length.")

def calculate_cuboid():
    """Calculates the surface area and volume of a cuboid (a box)."""
    try:
        # Get the three dimensions for the cuboid from the user.
        length = float(input("Enter the length of the cuboid: "))
        width = float(input("Enter the width of the cuboid: "))
        height = float(input("Enter the height of the cuboid: "))

        # --- Formulas for a Cuboid ---
        # Surface Area = 2 * (lw + lh + wh)
        # Volume = l * w * h
        surface_area = 2 * (length * width + length * height + width * height)
        volume = length * width * height

        # Display the results.
        print(f"\nSurface Area of the cuboid is: {surface_area:.2f}")
        print(f"Volume of the cuboid is: {volume:.2f}")

    except ValueError:
        # This message will show if any of the inputs were not valid numbers.
        print("\nError: Invalid input. Please enter numbers for the dimensions.")

def calculate_cone():
    """Calculates the surface area and volume of a cone."""
    try:
        # Get the radius and height from the user.
        radius = float(input("Enter the radius of the cone's base: "))
        height = float(input("Enter the height of the cone: "))
        pi = get_pi() # Get the value of Pi

        # --- Formulas for a Cone ---
        # To get the surface area, we first need the 'slant height' (the diagonal length
        # from the tip of the cone to the edge of its base).
        # We calculate it using the Pythagorean theorem: a² + b² = c²
        # Here, slant_height² = radius² + height², so slant_height = sqrt(radius² + height²)
        slant_height = (radius**2 + height**2)**0.5  # **0.5 is the same as taking the square root.

        # Surface Area = π * radius * (radius + slant_height)
        surface_area = pi * radius * (radius + slant_height)
        # Volume = (1/3) * π * radius² * height
        volume = (1/3) * pi * radius**2 * height

        # Display the results.
        print(f"\nSurface Area of the cone is: {surface_area:.2f}")
        print(f"Volume of the cone is: {volume:.2f}")

    except ValueError:
        print("\nError: Invalid input. Please enter numbers for the dimensions.")

def calculate_sphere():
    """Calculates the surface area and volume of a sphere."""
    try:
        # A sphere only needs one dimension: its radius.
        radius = float(input("Enter the radius of the sphere: "))
        pi = get_pi() # Get the value of Pi

        # --- Formulas for a Sphere ---
        # Surface Area = 4 * π * radius²
        # Volume = (4/3) * π * radius³
        surface_area = 4 * pi * radius**2
        volume = (4/3) * pi * radius**3

        # Display the results.
        print(f"\nSurface Area of the sphere is: {surface_area:.2f}")
        print(f"Volume of the sphere is: {volume:.2f}")

    except ValueError:
        print("\nError: Invalid input. Please enter a number for the radius.")

def calculate_square_pyramid():
    """Calculates the surface area and volume of a square pyramid."""
    try:
        # Get the dimensions from the user.
        base_side = float(input("Enter the base side length of the square pyramid: "))
        height = float(input("Enter the height of the square pyramid: "))

        # --- Formulas for a Square Pyramid ---
        # Just like the cone, we need the slant height for the surface area.
        # slant_height = sqrt(height² + (base_side / 2)²)
        slant_height = (height**2 + (base_side / 2)**2)**0.5

        # The area of the square base.
        base_area = base_side**2
        # The area of the four triangular sides.
        lateral_area = 2 * base_side * slant_height
        # Total Surface Area = Base Area + Area of the 4 Sides
        surface_area = base_area + lateral_area

        # Volume = (1/3) * base_area * height
        volume = (1/3) * base_area * height

        # Display the results.
        print(f"\nSurface Area of the square pyramid is: {surface_area:.2f}")
        print(f"Volume of the square pyramid is: {volume:.2f}")

    except ValueError:
        print("\nError: Invalid input. Please enter numbers for the dimensions.")

def calculate_cylinder():
    """Calculates the surface area and volume of a cylinder."""
    try:
        # Get the dimensions from the user.
        radius = float(input("Enter the radius of the cylinder's base: "))
        height = float(input("Enter the height of the cylinder: "))
        pi = get_pi() # Get the value of Pi

        # --- Formulas for a Cylinder ---
        # Surface Area = 2 * π * radius * (radius + height)
        # Volume = π * radius² * height
        surface_area = 2 * pi * radius * (radius + height)
        volume = pi * radius**2 * height

        # Display the results.
        print(f"\nSurface Area of the cylinder is: {surface_area:.2f}")
        print(f"Volume of the cylinder is: {volume:.2f}")

    except ValueError:
        print("\nError: Invalid input. Please enter numbers for the dimensions.")


# --- Main Program Logic ---

def display_menu():
    """A simple function to print the menu options."""
    print("\n" + "-"*37)  # Prints a line of dashes for visual separation.
    print("      3D Shape Calculator Menu")
    print("-"*37)
    print("1. Cube")
    print("2. Cuboid")
    print("3. Cone")
    print("4. Sphere")
    print("5. Square Pyramid")
    print("6. Cylinder")
    print("7. Exit")
    print("-"*37)

def main():
    """
    This is the main function that runs the program.
    It will loop forever, showing the menu and waiting for user input.
    """
    # This dictionary maps the user's choice (e.g., '1') to the function that
    # should be called (e.g., calculate_cube). This is a cleaner way to handle
    # the menu choices than a long series of if/elif/else statements.
    shape_functions = {
        '1': calculate_cube,
        '2': calculate_cuboid,
        '3': calculate_cone,
        '4': calculate_sphere,
        '5': calculate_square_pyramid,
        '6': calculate_cylinder,
    }

    # The 'while True' creates an infinite loop. The program will only stop
    # if the user chooses to exit, which triggers the 'break' command.
    while True:
        display_menu() # Show the user the list of options.

        # Get the user's choice.
        choice = input("Enter your choice (1-7): ")

        if choice in shape_functions:
            # If the user's choice is a key in our dictionary (e.g., '1', '2', etc.),
            # then call the corresponding function.
            shape_functions[choice]()
        elif choice == '7':
            # If the user chooses '7', print a goodbye message and exit the loop.
            print("Exiting the program. Goodbye!")
            break
        else:
            # If the user enters anything else, show an error message.
            print("Invalid choice. Please enter a number between 1 and 7.")

# This is a standard Python convention.
# The code inside this 'if' statement will only run when you execute this
# script directly (e.g., by running 'python your_file_name.py').
# It won't run if this file is imported as a module into another script.
# It's the official entry point of our program.
if __name__ == "__main__":
    main()

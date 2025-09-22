import sympy
import numpy as np
import re
import antlr4
from sympy.parsing.latex import parse_latex

# Firstly, to make this program work, we need to install `sympy`, `numpy`, and `antlr4-python3-runtime`.
# To do this, run:
# pip install sympy numpy antlr4-python3-runtime
def approximate_integral(latex_string: str, n: int):
    """
    Approximates a definite integral using the Trapezoidal, Midpoint, and Simpson's rules.

    Args:
        latex_string (str): The integral in LaTeX format, e.g., r"\\int_{1}^{4} \\frac{6}{\\sqrt{x}} dx".
        n (int): The number of subintervals (must be even for Simpson's rule).

    Returns:
        dict: A dictionary containing the approximations and their errors, rounded to 6 decimal places.
    """
    # 1. Parse the LaTeX string to extract limits and the function
    try:
        # This regex captures the lower limit, upper limit, function body, and variable
        # Improved regex: matches both \int and \\int, allows optional spaces
        pattern = r"\\\\?int_\{(.+?)\}\^\{(.+?)\}\s*(.+?)\s*d(\w)"
        match = re.search(pattern, latex_string)
        if not match:
            raise ValueError("Invalid LaTeX integral format provided. Please use the format: \\int_{a}^{b} <function> dx")

        a_str, b_str, func_str, var_str = match.groups()
        print(f"[DEBUG] Lower limit: {a_str}")
        print(f"[DEBUG] Upper limit: {b_str}")
        print(f"[DEBUG] Function: {func_str}")
        print(f"[DEBUG] Variable: {var_str}")

        # Convert limits to floating-point numbers
        a = float(sympy.sympify(a_str))
        b = float(sympy.sympify(b_str))

        # Create a symbolic variable (e.g., x, t, etc.)
        var = sympy.symbols(var_str)

        # 2. Convert the LaTeX function string into a callable Python function
        # Some inputs (and testing harnesses) escape backslashes. Normalize doubled
        # backslashes to single before parsing so SymPy's parser sees normal LaTeX.
        func_str_for_parse = func_str.strip().replace('\\\\', '\\')
        print(f"[DEBUG] Function (for parse): {func_str_for_parse}")
        symbolic_func = parse_latex(func_str_for_parse)
        # Use sympy.lambdify to create a fast numerical function using numpy
        f = sympy.lambdify(var, symbolic_func, 'numpy')

    except Exception as e:
        err_msg = f"Failed to parse the LaTeX string. Details: {e}"
        lower_e = str(e).lower()
        if "antlr" in lower_e or "requires the antlr4" in lower_e:
            err_msg += (
                "\nLaTeX parsing requires the ANTLR4 Python runtime (version 4.11). "
                "Install it with: `python -m pip install antlr4-python3-runtime==4.11` "
                "using the same Python interpreter you run this script with."
            )
        return {"error": err_msg}

    # 3. Calculate the exact value of the integral for error computation
    try:
        exact_value = float(sympy.integrate(symbolic_func, (var, a, b)))
    except Exception as e:
        # Return an error if the integral cannot be solved symbolically
        return {"error": f"Could not compute the exact integral. Details: {e}"}

    # Simpson's rule requires an even number of intervals
    if n % 2 != 0:
        return {"error": "n must be an even number for Simpson's Rule."}

    # 4. Implement the numerical approximation rules
    delta_x = (b - a) / n
    # Generate points for calculations
    points = np.linspace(a, b, n + 1)
    midpoints = points[:-1] + delta_x / 2

    # Trapezoidal Rule
    t_n = (delta_x / 2) * (f(points[0]) + 2 * np.sum(f(points[1:-1])) + f(points[-1]))

    # Midpoint Rule
    m_n = delta_x * np.sum(f(midpoints))

    # Simpson's Rule
    s_n = (delta_x / 3) * (f(points[0]) + 4 * np.sum(f(points[1:-1:2])) + 2 * np.sum(f(points[2:-2:2])) + f(points[-1]))

    # 5. Calculate the corresponding absolute errors
    e_t = exact_value - t_n
    e_m = exact_value - m_n
    e_s = exact_value - s_n

    # 6. Return the results, rounded to 6 decimal places
    results = {
        "T_n": round(t_n, 6),
        "M_n": round(m_n, 6),
        "S_n": round(s_n, 6),
        "E_T": round(e_t, 6),
        "E_M": round(e_m, 6),
        "E_S": round(e_s, 6)
    }

    return results
# Now we need to receive user input to receive our Latex string and n value
if __name__ == "__main__":
    print("Numerical Integration Approximator")
    latex_integral = input("Enter the definite integral in LaTeX format (e.g., \\int_{1}^{4} \\frac{6}{\\sqrt{x}} dx): ")
    n_str = input("Enter the number of subintervals (even number for Simpson's rule): ")
    try:
        n = int(n_str)
    except ValueError:
        print("Error: n must be an integer.")
        exit(1)
    results = approximate_integral(latex_integral, n)
    print("\nResults:")
    if "error" in results:
        print(results["error"])
    else:
        print("Trapezoidal Rule Approximation (T_n):", results["T_n"])
        print("Midpoint Rule Approximation (M_n):", results["M_n"])
        print("Simpson's Rule Approximation (S_n):", results["S_n"])
        print("Error in Trapezoidal Rule (E_T):", results["E_T"])
        print("Error in Midpoint Rule (E_M):", results["E_M"])
        print("Error in Simpson's Rule (E_S):", results["E_S"])
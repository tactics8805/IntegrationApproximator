# Integration by Tech Algorithm

Small utility to approximate definite integrals provided as LaTeX strings using the Trapezoidal, Midpoint and Simpson's numerical rules, along with their respective errors (deviations from the exact solution).

## Requirements
- Python 3.11 (or compatible 3.11.x)
- Packages (see `requirements.txt`):
  - `sympy==1.14.0`
  - `numpy`
  - `antlr4-python3-runtime==4.11.0`

Install dependencies with:

```powershell
python -m pip install -r requirements.txt
```

Make sure you install the requirements using the same `python` interpreter you use to run the script (you can verify with `python -c "import sys; print(sys.executable)"`).

## Usage
Run the script and enter the LaTeX integral and number of subintervals when prompted:

```powershell
python Integration_script.py
# Example input when prompted:
# Enter the definite integral in LaTeX format (e.g., \int_{1}^{4} \frac{6}{\sqrt{x}} dx): \int_{1}^{4} \frac{6}{\sqrt{x}} dx
# Enter the number of subintervals (even number for Simpson's rule): 100
```

The script returns the Trapezoidal, Midpoint, and Simpson approximations and their absolute errors compared to the symbolic integral (if computable).

## Troubleshooting
- SyntaxError when running the script: ensure the top of `Integration_script.py` contains `import antlr4` (no hyphens) and that the file is saved.
- If `sympy.parsing.latex.parse_latex` raises an error about ANTLR, make sure the ANTLR runtime is installed for the same interpreter:

```powershell
python -m pip install --upgrade antlr4-python3-runtime==4.11
```

- If the package was installed for a different Python installation, install it explicitly with that Python's executable, for example:

```powershell
'C:\Path\To\other\python.exe' -m pip install antlr4-python3-runtime==4.11
```

## Development notes
- The script includes a regex-based LaTeX extractor and uses SymPy's `parse_latex`. Complex LaTeX may not parse cleanly.
- To avoid the interactive prompt for testing, import the module from a Python one-liner instead:

```powershell
python -c "import importlib.util; spec=importlib.util.spec_from_file_location('integration', 'Integration_script.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print('Imported OK')"
```




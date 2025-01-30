import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sympy import symbols, Eq, sympify, solve

# Main application window
class FunctionSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Solver and Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Input fields for functions
        self.function1_input = QLineEdit(self)
        self.function1_input.setPlaceholderText("Enter first function of x, e.g., 5*x^3 + 2*x")
        self.layout.addWidget(self.function1_input)

        self.function2_input = QLineEdit(self)
        self.function2_input.setPlaceholderText("Enter second function of x, e.g., x^2 - 4")
        self.layout.addWidget(self.function2_input)

        # Solve and plot button
        self.solve_button = QPushButton("Solve and Plot", self)
        self.solve_button.clicked.connect(self.solve_and_plot)
        self.layout.addWidget(self.solve_button)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def solve_and_plot(self):
        """Solve the functions and plot them."""
        try:
            # Get user input
            func1_str = self.function1_input.text().strip()
            func2_str = self.function2_input.text().strip()

            # Validate input
            if not func1_str or not func2_str:
                raise ValueError("Please enter both functions.")

            # Validate allowed operators and functions
            allowed_pattern = re.compile(r'^[0-9x+\-*/^()log10()sqrt()\s]+$')
            if not allowed_pattern.match(func1_str) or not allowed_pattern.match(func2_str):
                raise ValueError("Invalid characters in function. Only +, -, *, /, ^, log10(), sqrt() are allowed.")

            # Define symbol
            x = symbols('x')

            # Parse functions
            func1 = sympify(func1_str)
            func2 = sympify(func2_str)

            # Solve for intersection
            equation = Eq(func1, func2)
            solutions = solve(equation, x)

            # Filter out complex solutions
            real_solutions = [sol.evalf() for sol in solutions if sol.is_real]
            if not real_solutions:
                raise ValueError("No real solutions found for the given functions.")

            # Generate x values for plotting
            x_vals = np.linspace(-10, 10, 400)
            y1_vals = [float(func1.subs(x, val).evalf()) for val in x_vals]
            y2_vals = [float(func2.subs(x, val).evalf()) for val in x_vals]

            # Clear previous plot
            self.ax.clear()

            # Plot functions
            self.ax.plot(x_vals, y1_vals, label=f"Function 1: {func1_str}")
            self.ax.plot(x_vals, y2_vals, label=f"Function 2: {func2_str}")

            # Plot real solution points
            for sol in real_solutions:
                y_sol = float(func1.subs(x, sol).evalf())
                self.ax.plot(sol, y_sol, 'ro')  # Red dot for solution
                self.ax.annotate(f'({sol:.2f}, {y_sol:.2f})', (sol, y_sol), textcoords="offset points", xytext=(10, 10), ha='center')

            # Add labels and legend
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.legend()
            self.ax.grid(True)

            # Refresh canvas
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionSolverApp()
    window.show()
    sys.exit(app.exec_())
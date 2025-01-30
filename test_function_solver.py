import pytest
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from function_solver import FunctionSolverApp

@pytest.fixture
def app(qtbot):
    """Fixture to initialize the application."""
    test_app = QApplication.instance()
    if test_app is None:
        test_app = QApplication([])
    window = FunctionSolverApp()
    qtbot.addWidget(window)
    return window

def test_input_validation(app, qtbot):
    """Test input validation for invalid characters."""
    # Simulate invalid input
    app.function1_input.setText("5*x^3 + 2*x + invalid")
    app.function2_input.setText("x^2 - 4")
    qtbot.mouseClick(app.solve_button, Qt.LeftButton)

    # Check if error message is shown
    assert app.function1_input.text() == "5*x^3 + 2*x + invalid"
    assert app.function2_input.text() == "x^2 - 4"

def test_solution_and_plot(app, qtbot):
    """Test solving and plotting valid functions."""
    # Simulate valid input
    app.function1_input.setText("5*x^3 + 2*x")
    app.function2_input.setText("x^2 - 4")
    qtbot.mouseClick(app.solve_button, Qt.LeftButton)

    # Check if plot is generated
    assert len(app.ax.lines) > 0  # Ensure lines are plotted
    assert len(app.ax.texts) > 0  # Ensure annotations are added
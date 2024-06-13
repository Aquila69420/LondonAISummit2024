from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap
import pandas as pd

def calculate_pension(raw_data, selected_date):
    """
    Calculate the current pension, reevaluated pension, and explanation based on the raw data and selected date.

    Args:
        raw_data (list): The raw user data.
        selected_date (datetime): The selected date.

    Returns:
        tuple: A tuple containing the current pension, reevaluated pension, and explanation.
    """
    current_pension = "Not Calculated"
    reevaluated_pension = "Not Calculated"
    explanation = "Enter user data and select a date to calculate pension."
    return current_pension, reevaluated_pension, explanation

def process_user_data(uploaded_file):
    """
    Processes uploaded user data (Excel) and returns a list of lists.

    Args:
        uploaded_file (FileStorage): The uploaded user data file.

    Returns:
        list: A list of lists representing the processed user data.
        str: An error message if an error occurs during processing.
    """
    try:
        data = pd.read_excel(uploaded_file, header=0)
        # Ensure 2 rows are present
        if data.shape[0] != 2:
            raise ValueError("Invalid user data format. Please upload a file with exactly 2 rows.")
        # Convert data to a list of lists for easier use in the template
        return data.values.tolist()
    except Exception as e:
        return None, f"Error processing user data: {str(e)}"

def show_modified_data(dictionary):
    """
    Show modified user data table with dictionary key as header on top row and value on bottom row.

    Args:
        dictionary (dict): The dictionary containing the modified user data.

    Returns:
        list: A list of lists representing the modified user data table.
    """
    modified_data = []
    for key, value in dictionary.items():
        modified_data.append([key, value])
    return modified_data

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # 16 MB max file size
Bootstrap(app)

@app.errorhandler(400)
def bad_request(error):
    """
    Error handler for invalid file uploads.

    Args:
        error (Exception): The error that occurred.

    Returns:
        str: The rendered template with the error message.
    """
    return render_template("index.html", error_message="Invalid file format.")

@app.route("/", methods=["GET", "POST"])
def index():
    """
    The main route of the Flask application.

    Returns:
        str: The rendered template with the processed data and calculated pension information.
    """
    raw_data = []
    modified_data = []
    selected_date = None
    current_pension = ""
    reevaluated_pension = ""
    explanation = ""
    error_message = None

    if request.method == "POST":
        if "pension_scheme" in request.files: # Upload pension scheme
            file = request.files["pension_scheme"]
            print(file)
        if "process_data_button" in request.form:
            modified_data = show_modified_data({'Date of Birth': 'COULD NOT DETERMINE', 'Date joined company': 'COULD NOT DETERMINE', 'Gender': 'COULD NOT DETERMINE', 'Marital Status': 'Single', 'Pension Status': 'Pensioner', 'No. of Children': '2', 'Retirement Date': 'COULD NOT DETERMINE', 'Retirement Type': 'Normal', 'Current Pension Amount': '50000'})

        if "user_data" in request.files: # Upload user data
            uploaded_file = request.files["user_data"]
            print(uploaded_file.filename)
            if uploaded_file.filename.endswith(".xlsx"):
                processed_data, error_message = process_user_data(uploaded_file)
                if processed_data:
                    raw_data = processed_data
                    modified_data = show_modified_data(processed_data)
                    modified_data = show_modified_data({'Date of Birth': 'COULD NOT DETERMINE', 'Date joined company': 'COULD NOT DETERMINE', 'Gender': 'COULD NOT DETERMINE', 'Marital Status': 'Single', 'Pension Status': 'Pensioner', 'No. of Children': '2', 'Retirement Date': 'COULD NOT DETERMINE', 'Retirement Type': 'Normal', 'Current Pension Amount': '50000'})
                else:
                    error_message = error_message or "Error processing user data."

    selected_date_str = request.form.get("selected_date")
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
        except ValueError:
            error_message = "Invalid date format. Please use YYYY-MM-DD."

    if raw_data and selected_date and not error_message:
        current_pension, reevaluated_pension, explanation = calculate_pension(raw_data, selected_date)

    return render_template("index.html", raw_data=raw_data, modified_data=modified_data, 
                            selected_date=selected_date.strftime("%Y-%m-%d") if selected_date else None,
                            current_pension=current_pension, reevaluated_pension=reevaluated_pension,
                            explanation=explanation, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=False)

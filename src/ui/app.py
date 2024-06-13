from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap
import pandas as pd

rules=[] #pension scheme rules

def compute(modified_data, selected_date):
    # do something with rules to produce the below output dictionary
    return {'Initial': '50000.0', 'Adjusted': '53750.0', 'Explanation': 'The provided information indicates the individual is a "Pensioner" with a "Current Pension Amount" of 50000.  Since the date is 1987, we can assume the pension is already in payment.  Given the lack of information about the pension\'s origin (GMP, pre/post 1997, etc.),  we must default to the most common scenario for pensions in payment in 1987.\n\nThe most common pension type in 1987 would be "Pre 6/4/1988 GMP, in payment". This is because Guaranteed Minimum Pensions (GMPs) were introduced in 1988, and before that, pensions were typically calculated based on a standard formula. \n\nTherefore, the appropriate pension readjustment is:\n\n* *Criteria:* "Pre 6/4/1988 GMP, in payment"\n* *Description:* "Fixed 7.5% increase"\n* *Adjustment about:*  The pension should be increased by 7.5%.\n* *Amount:* 0.075 \n\nThis means the individual\'s pension would be increased by 7.5% of their current pension amount (50000) in the following year. \n'}

def calculate_pension(modified_data, selected_date):
    """
    Calculate the current pension, reevaluated pension, and explanation based on the raw data and selected date.

    Args:
        modified_data (list): The raw user data.
        selected_date (datetime): The selected date.

    Returns:
        tuple: A tuple containing the current pension, reevaluated pension, and explanation.
    """
    values = compute(modified_data, selected_date)
    current_pension = values.get("Initial")
    reevaluated_pension = values.get("Adjusted")
    explanation = values.get("Explanation")
    return current_pension, reevaluated_pension, explanation

#TODO: Get the path to pension scheme file, increase text input width, get fields on pressing reeval button, user data upload?

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
            raw_data = request.form.get('user_data_input')
            # modified_data = show_modified_data({raw_data})
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

    if request.method == "GET":
        # if "process_data_button" in request.form:
        #     raw_data = request.form.get('user_data_input')
        #     modified_data = show_modified_data({raw_data})
        if "reevaluate_pension_button" in request.form:
            pension_scheme_path = request.form.get('pension_scheme_path').trim()
            selected_date_str = request.form.get("selected_date")
            if selected_date_str:
                try:
                    selected_date = datetime.strptime(selected_date_str, "%d-%m-%Y")
                except ValueError:
                    error_message = "Invalid date format. Please use DD-MM-YYYY."
            modified_data = request.form.get('modified_data')
            if raw_data and selected_date and not error_message:
                current_pension, reevaluated_pension, explanation = calculate_pension(modified_data, selected_date)

    return render_template("index.html", raw_data=raw_data, modified_data=modified_data, 
                            selected_date=selected_date.strftime("%d-%m-%Y") if selected_date else None,
                            current_pension=current_pension, reevaluated_pension=reevaluated_pension,
                            explanation=explanation, error_message=error_message)

if __name__ == "__main__":
    #threading.Thread(target=app.run, kwargs={"debug": False}).start()
    app.run(debug=False)

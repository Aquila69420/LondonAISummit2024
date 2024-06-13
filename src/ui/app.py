from flask import *
from datetime import datetime
from flask_bootstrap import Bootstrap
import pandas as pd

rules = None #pension scheme rules

def compute(modified_data, selected_date):
    return [{'Initial': '50000.0', 'Adjusted': '53750.0', 'Explanation': 'The provided information indicates the individual is a "Pensioner" with a "Current Pension Amount" of 50000.  Since the date is 1987, we can assume the pension is already in payment.  Given the lack of information about the pension\'s origin (GMP, pre/post 1997, etc.),  we must default to the most common scenario for pensions in payment in 1987.\n\nThe most common pension type in 1987 would be "Pre 6/4/1988 GMP, in payment". This is because Guaranteed Minimum Pensions (GMPs) were introduced in 1988, and before that, pensions were typically calculated based on a standard formula. \n\nTherefore, the appropriate pension readjustment is:\n\n* *Criteria:* "Pre 6/4/1988 GMP, in payment"\n* *Description:* "Fixed 7.5% increase"\n* *Adjustment about:*  The pension should be increased by 7.5%.\n* *Amount:* 0.075 \n\nThis means the individual\'s pension would be increased by 7.5% of their current pension amount (50000) in the following year. \n'}]

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
    current_pension = "50000.0"
    reevaluated_pension = "53750.0"
    explanation = """The provided information indicates the individual is a "Pensioner" with a "Current Pension Amount" of 50000.  Since the date is 1987, we can assume the pension is already in payment.  Given the lack of information about the pension\'s origin (GMP, pre/post 1997, etc.),  we must default to the most common scenario for pensions in payment in 1987.\n\nThe most common pension type in 1987 would be "Pre 6/4/1988 GMP, in payment". This is because Guaranteed Minimum Pensions (GMPs) were introduced in 1988, and before that, pensions were typically calculated based on a standard formula. \n\nTherefore, the appropriate pension readjustment is:\n\n* *Criteria:* "Pre 6/4/1988 GMP, in payment"\n* *Description:* "Fixed 7.5% increase"\n* *Adjustment about:*  The pension should be increased by 7.5%.\n* *Amount:* 0.075 \n\nThis means the individual\'s pension would be increased by 7.5% of their current pension amount (50000) in the following year. \n"""
    vars['current_pension'] = current_pension
    vars['reevaluated_pension'] = reevaluated_pension
    vars['explanation'] = explanation
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
app.secret_key = "khdfgsfkdsgfsjfhjsdfjskgf"
Bootstrap(app)

vars={}

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
            print("process_data_button clicked")
            raw_data = request.form.get('user_data_input')
            vars['raw_data'] = raw_data
            modified_data = show_modified_data({'Date of Birth': 'COULD NOT DETERMINE', 'Date joined company': 'COULD NOT DETERMINE', 'Gender': 'COULD NOT DETERMINE', 'Marital Status': 'Single', 'Pension Status': 'Pensioner', 'No. of Children': '2', 'Retirement Date': 'COULD NOT DETERMINE', 'Retirement Type': 'Normal', 'Current Pension Amount': '50000'})
            vars['modified_data'] = modified_data
            print('raw_data', vars.get('raw_data'))
            print('modified_data', vars.get('modified_data'))

        if "reevaluate_pension_button" in request.form:
            global rules
            print(request.form)
            print("reevaluate_pension_button clicked")
            pension_scheme_path = request.form.get('pension_scheme_path').strip() if request.form.get('pension_scheme_path')!=None else None
            vars[pension_scheme_path]=pension_scheme_path
            try:
                rules = open(pension_scheme_path, "r")
            except:
                print("Unable to open pension scheme file.")
            selected_date_str = request.form.get("selected_date")
            if selected_date_str:
                try:
                    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
                    vars['selected_date']=selected_date.strftime("%Y-%m-%d") if selected_date else None
                except ValueError:
                    error_message = "Invalid date format. Please use MM-DD-YYYY."
            raw_data = request.form.get('user_data_input')
            modified_data = request.form.get('modified_data')
            vars['modified_data'] = modified_data
            
            calc = calculate_pension(modified_data, selected_date)
            current_pension, reevaluated_pension, explanation = calc
            
            explanation = """The provided information indicates the individual is a "Pensioner" with a "Current Pension Amount" of 50000. Since the date is 1987, we can assume the pension is already in payment.  Given the lack of information about the pension\'s origin (GMP, pre/post 1997, etc.),  we must default to the most common scenario for pensions in payment in 1987.\n\nThe most common pension type in 1987 would be "Pre 6/4/1988 GMP, in payment". This is because Guaranteed Minimum Pensions (GMPs) were introduced in 1988, and before that, pensions were typically calculated based on a standard formula. \n\nTherefore, the appropriate pension readjustment is:\n\n* *Criteria:* "Pre 6/4/1988 GMP, in payment"\n* *Description:* "Fixed 7.5% increase"\n* *Adjustment about:*  The pension should be increased by 7.5%.\n* *Amount:* 0.075 \n\nThis means the individual\'s pension would be increased by 7.5% of their current pension amount (50000) in the following year. \n"""
            vars['explanation'] = explanation
            
            print("output", calc)
            print('pension_scheme_path', vars.get('pension_scheme_path'))
            print('selected_date', vars.get('selected_date'))
            print('raw_data', vars.get('raw_data'))
            print('modified_data', vars.get('modified_data'))
            print('current_pension', vars.get('current_pension'))
            print('reevaluated_pension', vars.get('reevaluated_pension'))
            print('explanation', vars.get('explanation'))

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

    return render_template("index.html", raw_data=vars.get('raw_data'), modified_data=vars.get('modified_data'), 
                            selected_date=vars.get('selected_date'),
                            current_pension=current_pension, reevaluated_pension=reevaluated_pension,
                            explanation=explanation, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=False)

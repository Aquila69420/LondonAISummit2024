# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ai.pipelines.user_data_extraction_pipeline import UserDataExtractionPipeline

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    pipe = UserDataExtractionPipeline("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU")
    i = "Tom not married, current pension 50000, tom is not a dad and has retired normally."
    a = pipe.process(i)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

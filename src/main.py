# This is a sample Python script.
from custome_io import read_docx
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from ai.pipelines.user_data_extraction_pipeline import UserDataExtractionPipeline
from ai.pipelines.understand_prt_pipeline import UnderstandPrtPipeline
from ai.pipelines.recommend_revaluation_pipeline import RecommendRevaluationPipeline
import agents

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass

    #pipe = UserDataExtractionPipeline("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU")
    #i = "Tom not married, current pension 50000, tom is a dad had a son Bob and daughter Elsa and has retired normally."
    #a = pipe.process(i)
    #print(a)

    #pipe = UnderstandPrtPipeline("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU")
    #i = read_docx("input/IBP_Problemstatement.docx")
    #b = pipe.process(i)
    #print(b)

    #pipe = RecommendRevaluationPipeline("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU")
    #c = pipe.process(a, b)
    #print(c)

    #print(f"Before: {float(a['Current Pension Amount'])}")
    #print(f"Adjustment: {float(c['Amount'])}")
    #print(f"After: {float(a['Current Pension Amount']) * (1 + float(c['Amount']))}")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

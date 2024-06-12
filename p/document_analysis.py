from gemini_model import GeminiModel
from custome_io import read_docx

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = read_docx("input/IBP_Problemstatement.docx")
    gemini_model = GeminiModel("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU", "gemini-1.5-flash")
    with open("input/prompt.txt", "r") as f:
        prompt = f.read()
    gemini_model.start_chat()
    response = gemini_model.send_message(a + prompt)

    for i in range(5):
        print("--------------------")

    with open("input/input.txt", "r") as f:
        iiii = f.read()
    prompt = ("recommend suitable PRT schemes or pricing options, this will be used as a guidences "
              "for a human to make the final decision.")
    response = gemini_model.send_message(iiii + prompt)
    print(response)


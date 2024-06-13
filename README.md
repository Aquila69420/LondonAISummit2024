# AI Summit London 2024 Hackathon
## Setup & Dependencies
To set up all the dependencies for this project simple crate a new python virtual environment and install the following packages:

    pip install uagents
    pip install google-generativeai
    pip install python-docx
    pip install flask
    pip install pandas
    pip install Flask-Bootstrap

## Repository Contents
### Main Packages
This repository contains 3 main packages:
* **Agents** -  ```agents```  packages harness the power of uagetns likening capabilities to combine small single purpose agents into powerful AI power pipelines
* **AI** - ```ai```  package contains our customer AI framework that we have designed specify for exploiting the NPL power of LLM, it provides hight level of abstraction and plenty of predefined component read to be used to build a small single purposes LLM pipeline.
* **ERF**  - ```erf``` pacage contain utilities related to is our own new file format .erf (embedded referring format) used to store and manage templates (prompts, primers etc) for the use with the AI package. This package contains a complier used to read and compile this file types.
### Template
In the ```templates```  folder you can see our .erf file type in action (no explaninig needed, you will know how it works once you see inside one of the file) and the overall approuch we took to maning and thinking about scalining with repect to preompt templaye which are the core of LLM systems.

## More About AI Package
The AI package contains our modulare framework for LLM based interactions and 3 predifned pipelines
* **UserDataExtractionPipeline**  - This pipeline is responsible for extracting useful data about the person to a structed format, we can handle when the most un-structed input such as transcript of conversation where the person talks about themselves.   See for more detail ```ai/pipelines/user_data_extraction_pipeline.py```.
* **UnderstandPrtPipeline** - This pipeline is responsible for reading and understating the pensions scheme document in various formats (.docx, .pdf, .txt, ect if we can read it, we can use it) and extracting relevant sections/rules to a structed JSON from. See for more detail ```ai/pipelines/understand_prt_pipeline.py```
* **RecommendRevaluationPipeline** - This pipeline take in structured user data and structured relevant scheme data (from data points come from the pipelines introduced above), based on these inputs we make recommendations what pension readjustment to apply providing reasoning for the matches in human language and structured parameter data about the section that will be used to automatically apply the readjustment if it contains sufficient data, if not only a suggestion of what section should be applied will be used. See for more detail ```ai/pipelines/user_data_extraction_pipeline.py``` 

## Presentation
Presentation slides are available at the root of the repo. 

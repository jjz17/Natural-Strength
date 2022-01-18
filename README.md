# 🔨Build Your Natural Strength🔨
_**A tool to improve powerlifting through goal setting, estimates for  PRs, and to stay up to date on the world's best natural lifters**_

## Resources
https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030
https://codeshack.io/login-system-python-flask-mysql/#packages

## Introduction 
https://barbend.com/social-media-training-impact/

Discuss

## To Run
cd into pythonlogin -> flask run


[comment]: <> (## Tool Description )

[comment]: <> (Data Storyteller is an AI based tool that can take a data set, identify patterns in the data, can interpret the result, )

[comment]: <> (and can then produce an output story that is understandable to a business user based on the context. It is able to)

[comment]: <> (pro-actively analyse data on behalf of users and generate smart feeds using natural language generation techniques )

[comment]: <> (which can then be consumed easily by business users with very less efforts. The application has been built keeping in )

[comment]: <> (mind a rather elementary user and is hence, easily usable and understandable. This also uses a )

[comment]: <> (**multipage implementation** of Streamlit Library using Class based pages. )

[comment]: <> (## Features )

[comment]: <> (Given data/analytics output, the tool can:-)

[comment]: <> (- turn the data into interactive data stories based on the given data )

[comment]: <> (- generate deep insights, infer pattern and help in business decisions.)

[comment]: <> (- provide personalization profiles; these could be represented as meta data describing what would be of interest to a given user.)

[comment]: <> (- generate reports understandable to a business user with interactive and intuitive interface.)

[comment]: <> (## 📝 Module-Wise Description)

[comment]: <> (The application also uses Streamlit for a multiclass page implementation which can be viewed in the `multipage.py` file. The UI of the application can be seen here. The application is divided into multiple modules, each of which have been described below.)

[comment]: <> (![UI of the application]&#40;https://i.stack.imgur.com/MOVpz.png&#41;)


[comment]: <> (_📌 **Data Upload**_ <br/>)

[comment]: <> (This module deals with the data upload. It can take csv and excel files. As soon as the data is uploaded, it creates a copy of the data to ensure that we don't have to read the data multiple times. It also saves the columns and their data types along with displaying them for the user. This is used to upload and save the data and it's column types which will be further needed at a later stage. )

[comment]: <> (_📌 **Change Metadata**_ <br/>)

[comment]: <> (Once the column types are saved in the metadata, we need to give the user the option to change the type. This is to ensure that the automatic column tagging can be overridden if the user wishes. For example a binary column with 0 and 1s can be tagged as numerical and the user might have to correct it. The three data types available are:)

[comment]: <> (* Numerical )

[comment]: <> (* Categorical )

[comment]: <> (* Object)

[comment]: <> (The correction happens immediately and is saved at that moment. )

[comment]: <> (_📌 **Machine Learning**_ <br/>)

[comment]: <> (This section automates the process of machine learning by giving the user the option to select X and y variables and letting us do everything else. The user can specify which columns they need for machine learning and then select the type of process - regression and classficiation. The application selects multiple models and saves the best one as a binary `.sav` file to be used in the future for inferencing. The accuracy or R2 score is shown right then and there with the model running in the background.  )

[comment]: <> (_📌 **Data Visualization**_ <br/>)

[comment]: <> (_📌 **Y-Parameter Optimization**_ <br/>)

[comment]: <> (## Technology Stack )

[comment]: <> (1. Python )

[comment]: <> (2. Streamlit )

[comment]: <> (3. Pandas)

[comment]: <> (4. Scikit-Learn)

[comment]: <> (5. Seaborn)

[comment]: <> (# How to Run )

[comment]: <> (- Clone the repository)

[comment]: <> (- Setup Virtual environment)

[comment]: <> (```)

[comment]: <> ($ python3 -m venv env)

[comment]: <> (```)

[comment]: <> (- Activate the virtual environment)

[comment]: <> (```)

[comment]: <> ($ source env/bin/activate)

[comment]: <> (```)

[comment]: <> (- Install dependencies using)

[comment]: <> (```)

[comment]: <> ($ pip install -r requirements.txt)

[comment]: <> (```)

[comment]: <> (- Run Streamlit)

[comment]: <> (```)

[comment]: <> ($ streamlit run app.py)

[comment]: <> (```)

[comment]: <> (## Other Content)

[comment]: <> (**[Video Walkthrough]&#40;https://drive.google.com/file/d/1C-WMgJ6tLfVMAz4mS-OQF9-9-0GhgSWJ/view?usp=sharing&#41;**)

[comment]: <> (**[Presentation]&#40;https://drive.google.com/file/d/1vlmXN_wNQdf6Y_hpVKV2QD1ub80izIiK/view?usp=sharing&#41;**)

[comment]: <> (## 🤝 How to Contribute? [3])

[comment]: <> (- Take a look at the Existing Issues or create your own Issues!)

[comment]: <> (- Wait for the Issue to be assigned to you after which you can start working on it.)

[comment]: <> (- Fork the Repo and create a Branch for any Issue that you are working upon.)

[comment]: <> (- Create a Pull Request which will be promptly reviewed and suggestions would be added to improve it.)

[comment]: <> (- Add Screenshots to help us know what this Script is all about.)


[comment]: <> (# 👨‍💻 Contributors ✨)

[comment]: <> (<table>)

[comment]: <> (  <tr>)

[comment]: <> (    <td align="center"><a href="https://github.com/prakharrathi25"><img src="https://avatars.githubusercontent.com/u/38958532?v=4" width="100px;" alt=""/><br /><sub><b>Prakhar Rathi</b></sub></a><br /></td>)

[comment]: <> (    <td align="center"><a href="https://github.com/mpLogics"><img src="https://avatars.githubusercontent.com/u/48443496?v=4" width="100px;" alt=""/><br /><sub><b>Manav Prabhakar</b></sub></a><br /></td>)

[comment]: <> (    <td align="center"><a href="https://github.com/salilsaxena"><img src="https://avatars.githubusercontent.com/u/54006908?v=4" width="100px;" alt=""/><br /><sub><b>Salil Sxena</b></sub></a><br /></td> )

[comment]: <> (  </tr>)

[comment]: <> (</table>)

[comment]: <> (## References )

[comment]: <> ([1] SAP Hackathon: https://sap-code.hackerearth.com/challenges/hackathon/sap-code/custom-tab/data-4-storytelling/#Data%204%20Storytelling &#40;used for the `README.md` introduction&#41;)

[comment]: <> ([2] Gartner: https://www.gartner.com/en/documents/3982132)

[comment]: <> ([3] Soumyajit Behera: https://github.com/soumyajit4419/MedHub_360)


[comment]: <> (## Contact)

[comment]: <> (For any feedback or queries, please reach out to [prakharrathi25@gmail.com]&#40;prakharrathi25@gmail.com&#41;.)

[comment]: <> (Note: The project is only for education purposes, no plagiarism is intended.)
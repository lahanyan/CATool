# CATool
Conjoint Analysis
This tool has been developed by a group of students from the American University of Armenia for the Marketing Analytics course.
The tool enables the users to build surveys to perform one of the most used marketing analytics methods: Choice-Based Conjoint Analysis.

Requirements: Streamlit, Numpy, Pandas, SKLearn


Input: csv file of attributes and level ranges with design (orthogonal, full- or half- factorial). Your data can be turned into the needed format by running the Createdf.ipynb file in the Data folder. As an additional source, R packages can be used to obtain the design, as well.

User settings:  user chooses pivotal columns, show or hide the screening
Survey taker flow: For each alternative the respondent chooses if it's "possible" for them to obtain the product or "impossible". 
                 The Bayesian approach makes this tool one-in-the-market as it gives the survey taker the unique opportunity to eliminate the Unacceptable options of                          attributes.
                 
Results: The return is a downloadable choice tournament, where the best-fit choices are shown based on the coefficients. 

Replication: Clone this Github repository. The front - and back-end codes with the ML models are inside the one notebook for the ease of use. Run it in your machine's terminal. PLEASE, MAKE SURE YOU SET THE CURRENT WORKING DIRECTORY TO THE PATH WHICH INDICATES TO THE DIRECTORY WHERE THE CODE FILES ARE not to get the path errors. 

P.S. the logistic regression model theoretically serves as a "filter". The results are the top-matches for a single survey taker regressed and matched with the Unacceptable factors. It would have been just adding one line of code, but there is no single point of adding an accuracy score on a tool like this. 

Enjoy the demo!

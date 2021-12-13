# CATool
Conjoint Analysis
This tool has been developed by a group of students from the American University of Armenia for the Marketing Analytics course.
The tool enables the users to build surveys to perform one of the most used marketing analytics methods: Choice-Based Conjoint Analysis.

Requirements: Streamlit, Numpy, Pandas, SKLearn


Input: csv file of attributes and level ranges with design (orthogonal, full- or half- factorial)
User settings: user chooses pivotal columns, show or hide the screening
Survey taker flow: For each alternative the respondent chooses if it's "possible" for them to obtain the product or "impossible". 
                 The Bayesian approach makes this tool one-in-the-market as it gives the survey taker the unique opportunity to eliminate the Unacceptable options of                          attributes.
                 
Results: The return is a downloadable choice tournament, where the best-fit choices are shown based on the coefficients.



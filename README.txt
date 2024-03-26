Jessica Beno
3/26/24

# Description
The file main.py carries out the primary tasks of interest. First, a SQLite database (local .db file) is created with tables of the specified format. The title of this db is client_data.db. Next, each of the input files (located in 0_infiles) are read into a pandas dataframe. Each row of this dataframe is then stored as a list within a storage list (i.e., a nested list object, or list of lists). These storage lists are then used to populate the data tables of the SQLite database. The appropriate primary and foreign keys are set during table generation. This satisfies the first endpoint (i.e., consume and parse the data files, and load them into a database).

Finally, the requested query is performed. This query lists the top X number of clients that have accumulated the most loyalty points since Y date. The values of X and Y are dynamic, and are specified by the user as inputs in the command line (input prompts are provided for each). Banned clients are excluded. This satisfies the second endpoint request.

For compatibility with a RESTful API Response, the results of the query are converted to JSON format (see the object "json_results"). This JSON result is suitable for a RESTful API response and can be used in a web application like the one described in the assignment directions.

Basic instructions have been provided below. After, a few points for improvement have been provided in the subsequent "Future Directions" section.


# Instructions
1. Run main.py
2. Enter "Top X number" as input into terminal
3. Enter "Date" as input into terminal (formatting: 2018-01-01, exception handling was not implemented for this assignment).


# Future Directions
This code can be improved upon in several ways if more time were permitted. First, the "nice to have" items could be added as simple SQL operations. These operations are much more simple than the primary query request, but I did not have time to add them during the work week. 

Second, functions could be added to carry out basic queries of a well defined format. These functions would make the code more functional / useful overall.

Third, a basic web application could be developed, perhaps using flask or Django frameworks, to test the output of this script in the intended context (i.e., pass the JSON result to the web application).

Lastly, I note that the "user input" command line features are a bit clunky. I only implemented this in this way for example purposes. It might be more relevant to receive user inputs from a form displayed on a web app, but I did not have time to develop a test app for this assignment.

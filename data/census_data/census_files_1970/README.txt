File: explanation_of_files.txt
Purpose: guide old data directories

Each year has a few types of files:

1. CSV files: these are the raw data files. The first bit (e.g., nhgis009) says which pull it is. The rest identifies the file and table. Each file has a matching codebook. 

2. Codebook.txt files: these files match with each CSV file to provide guidance. 

3. Ipynb notebook: each notebook will create the csv file for use in the db with just the variables that we care about! 

4. Other csv files: the final csv file for export to the database

To recreate the files we used, all you need to do is run the Jupyter notebook per folder. The output file will be generated as specified in the variable definition cell.  
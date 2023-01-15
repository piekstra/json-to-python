from json_to_python import JsonToPython

# The name of a json file in the local directory - do not include the extension
file_name = 'transaction_summary'

# A python file will be output with the same nae as the input file
JsonToPython.transform_file(file_name)

import pickle


# saves a Python object to a pickled file using a relative path from the ../data/ directory.
def pickle_file(data_path, python_obj):
    with open('../pickled_data/' + data_path, 'wb') as pickle_file:
        pickle.dump(python_obj, pickle_file, protocol=pickle.DEFAULT_PROTOCOL)

def load_file(data_path):
    with open('../pickled_data/' + data_path, "rb") as input_file:
        return pickle.load(input_file)

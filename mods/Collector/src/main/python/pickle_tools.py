import os
import pickle

def save_to_pickle(data, filename):
    """Saves data to a pickle file."""
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_from_pickle(filename, default):
    """Loads data from a pickle file. Returns None if the file does not exist or cannot be loaded."""
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error loading pickle file: {e}")
            return default
    else:
        return default

def pickle_file_exists(filename):
    """Checks if a pickle file exists."""
    return os.path.exists(filename)

def delete_pickle_file(filename):
    """Deletes a pickle file if it exists."""
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except Exception as e:
            print(f"Error deleting pickle file: {e}")

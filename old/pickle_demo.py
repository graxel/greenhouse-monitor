import pickle
import sys

my_variable = {'example_key': 'example_value'}

pickled_data = pickle.dumps(my_variable)

print(sys.getsizeof(my_variable), sys.getsizeof(pickled_data))

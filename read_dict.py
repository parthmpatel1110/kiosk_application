import pickle

# Read dictionary pkl file
with open('feedback_data.pkl', 'rb') as fp:
    person = pickle.load(fp)
    print(person)
import numpy as np
from sklearn import preprocessing

input_labels = ['red','black','red','green','black','yellow','white']

encoder = preprocessing.LabelEncoder()
encoder.fit(input_labels)

print("Label mapping")
for i in enumerate(encoder.clasees_):
    print(item ,"-->", i)

test_labels = ['green','yellow','black']
encoded_values = encoder.transform(test_labels)
print("Labels = ", test_labels)
print("Encoded values = ", list(encoded_values))

encoded_values = [3,0,4,1]
decoded_list = encoder.inverse_transform(encoded_values)
print("Encoded values = ", encoded_values)
print("Decoded list = ", list(Decoded_list))
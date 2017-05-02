import numpy as np
import pandas as pd
from collections import defaultdict
import math
from sklearn.model_selection import train_test_split
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import zero_one_loss
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
import itertools
import pickle


# if more than ATTACK_THRESHOLD percent of packets are predicted as attack, return true.
# else, return false.
def is_attack(switch_pred):
    ATTACK_THRESHOLD = .15 
    num_rows = switch_pred.shape[0]
    num_attack = sum(switch_pred)
    return (float(num_attack / num_rows) > ATTACK_THRESHOLD)

def check_for_anomalies():

	# load best ML model and make predictions on x
	best_model = pickle.load(open('data/model.pkl', 'rb'))

	switch_data = pd.read_csv('data/switch.csv')
	camera_data = pd.read_csv('data/camera.csv')
	phone_data = pd.read_csv('data/phone.csv')

	switch_x=switch_data.copy(deep=True)
	switch_y=switch_x['Label']
	del switch_x['Label']

	camera_x=camera_data.copy(deep=True)
	camera_y=camera_x['Label']
	del camera_x['Label']

	phone_x=phone_data.copy(deep=True)
	phone_y=phone_x['Label']
	del phone_x['Label']

	switch_pred = best_model.predict(switch_x)
	camera_pred = best_model.predict(camera_x)
	phone_pred = best_model.predict(phone_x)

	ans = dict()
	ans['172.24.1.81'] = is_attack(switch_pred)
	ans['172.24.1.107'] = is_attack(camera_pred)
	ans['172.24.1.63'] = is_attack(phone_pred)

	return ans
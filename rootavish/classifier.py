#! /usr/bin/env python
from sklearn import svm

#key:
# 1 = Male
# 0 = Female

class Classifier:

	# The SVM
	claf = svm.SVC()

	# Here pitch and gender are numpy matrices.
	# We Create only one Instance of this type, and pass lists
	def __init__(self, pitch, gender, sample):
		self.pitch = pitch
		self.gender = gender
		self.sample = sample

		# Train the classifer using our sample data
		self.claf.fit(self.pitch, self.gender)
		print "Classifier trained successfully"

	# Call to the classifier during testing, return the prediction of the SVM.
	def classify(self, testcase):
		if self.claf.predict(testcase)[0] == 0:
			print "The speaker is Female"
		else:
			print "The speaker is Male"

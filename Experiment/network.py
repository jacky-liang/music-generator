import lasagne
import theano
import theano.tensor as T
import numpy as np
from sound_data_object import SoundDataObject
from sound_syns import SoundSyns

class Network:
	def __init__(self, learning_rate=0.1, train="keys_Training.sdo",
			cv="keys_CV.sdo", test="keys_Test.sdo"):
		print "Loading data sets"
		self.train_data = Network.parseSdo(SoundDataObject.loadSdo(train))
		self.cv_data = Network.parseSdo(SoundDataObject.loadSdo(cv))
		self.test_data = Network.parseSdo(SoundDataObject.loadSdo(test))
		print "Done loading"
		self.build_mlp(learning_rate, len(self.train_data["Y"][0]))

	@staticmethod
	def parseSdo(sdo):
		X = []
		Y = []
		for sample in sdo.data:
			sampleX = []
			for bucket in sample.data:
				sampleX.append(bucket.muAmp)
			X.append(sampleX)

			sampleY = []
			keys = SoundSyns.key_mappings.keys()
			for key in keys:
				sampleY.append(1 if key in sample.labels else 0)
			Y.append(sampleY)
		return {"X": X, "Y": Y}

	def build_mlp(self, learning_rate=0.1, outputs=120):
		# Each row is a different example
		# For the input, each column is a different feature
		input_var = T.matrix('inputs')
		# 
		target_var = T.imatrix('targets')
	
		# Input layer
		# Unspecified batch size, each example has 120 elements
		network = lasagne.layers.InputLayer((None, 120), input_var=input_var)
	
		# Hidden layer
		# Fully connected, 100 units
		network = lasagne.layers.DenseLayer(network, num_units=100,
				nonlinearity=lasagne.nonlinearities.sigmoid)
	
		# Output layer
		# outputs possible labels, but multiple labels may apply to an input (e.g. a chord)
		network = lasagne.layers.DenseLayer(network, num_units=outputs,
				nonlinearity=lasagne.nonlinearities.sigmoid)
	
		# Expression for output
		prediction = lasagne.layers.get_output(network)
		# Expression for cost function
		cost = lasagne.objectives.binary_crossentropy(prediction, target_var)
		# Right now cost is a vector of costs for each example, so take the average
		cost = cost.mean()
	
		params = lasagne.layers.get_all_params(network, trainable=True)
		# Expressions for updating parameters, using stochastic gradient descent
		updates = lasagne.updates.sgd(cost, params, learning_rate=learning_rate)
	
		self.train = theano.function([input_var, target_var], cost, updates=updates)
		self.predict = theano.function([input_var], prediction)

network = Network()
print 'Use network.train(network.train_data["X"], network.train_data["Y"]) to train (it returns the current cost)'
print 'Use network.predict(network.train_data["X"]) to predict'

import numpy
import pandas
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense 
from keras.layers import LSTM
from keras.layers import Dropout
from keras.preprocessing.sequence import pad_sequences

dataset = (pandas.read_csv('example_dataset.csv')).values

wElo = []
bElo = []
moves = []
movesSet = set()

for i in dataset:
	wElo.append(i[0])
	bElo.append(i[1])
	gameMoves = []
	
	for move in i[2].split():
		gameMoves.append(move)
		movesSet.add(move)
	
	moves.append(gameMoves)

#Encoding moves as ints then hot encoding.	
movesIntCodes = LabelEncoder().fit_transform(list(movesSet))
movesIntCodes = movesIntCodes.reshape(len(movesIntCodes), 1)
movesHotCodes = OneHotEncoder(sparse=False).fit_transform(movesIntCodes)

movesToHotCodes = {}
movesSet = list(movesSet)

for moveNum in range(len(movesSet)):
	movesToHotCodes[movesSet[moveNum]] = movesHotCodes[moveNum].tolist()		


moveSequenceCount = 0
for moveSequence in moves:		
	moveCount = 0
	for move in moveSequence:		
		if move in movesToHotCodes:
			moves[moveSequenceCount][moveCount] = movesToHotCodes[move]
		moveCount += 1
	moveSequenceCount += 1

moves = numpy.array(moves)
wElo = numpy.array(wElo)
bElo = numpy.array(bElo)

elo = numpy.vstack((wElo, bElo)).T

movesPad = pad_sequences(moves, 10, dtype='int', padding='pre')

numberOfFolds = 10
inputFolds = numpy.split(movesPad, numberOfFolds)
outputFolds = numpy.split(elo, numberOfFolds)

accuracies = []

for foldNum in range(0,numberOfFolds):
	inputTrain = []
	
	for inputFoldNum in range(0,numberOfFolds):
		if inputFoldNum != foldNum:
			if inputTrain == []:
				inputTrain = inputFolds[inputFoldNum]
			else:
				inputTrain = numpy.concatenate((inputTrain, inputFolds[inputFoldNum]))
    
	outputTrain = []
	
	for outputFoldNum in range(0,numberOfFolds):
		if outputFoldNum != foldNum:
			if outputTrain == []:
				outputTrain = outputFolds[outputFoldNum]
			else:
				outputTrain = numpy.concatenate((outputTrain, outputFolds[outputFoldNum])) 
	
	inputTest = inputFolds[foldNum]
	outputTest = outputFolds[foldNum]
	
	model = Sequential()
	
	model.add(LSTM(units=389, return_sequences=True, input_shape=(
			movesPad.shape[1], movesPad.shape[2])))
	model.add(Dropout(0.2))
	
	model.add(LSTM(units=389))
	model.add(Dropout(0.2))	
	
	model.add(Dense(units=2))
	
	model.compile(optimizer='RMSprop', loss='mean_squared_error', metrics=['accuracy'])
	
	model.fit(inputTrain, outputTrain, epochs = 1)
	
	eloPred = model.evaluate(inputTest, outputTest)
	accuracies.append(eloPred[1])
	
	break #Include break to only run one kfold iteration.	

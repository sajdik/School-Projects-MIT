import numpy as np
from glob import glob
import librosa
from sklearn import mixture
import sys
import os

CLASS_N = 31
TRAIN_DIR = '../train'
VAL_DIR = '../dev'
EVAL_DIR = '../eval'
RESULT_FILE = 'voice_predictions'

def wav16khz2mfcc(dir_name):
    """
    Loads all *.wav files from directory dir_name (must be 16kHz), converts them into MFCC 
    features (40 coefficients) and stores them into a list.
    """
    features = []
    for f in glob(dir_name + '/*.wav'):
        X, sample_rate = librosa.load(f, sr=16000)
        mfcc = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
        features.append(mfcc)
        
    return features

def create_model():
    """
        Creates model from train samples. Returns list of learned gmms
    """
    gmms = []
    for i in range(1, CLASS_N+1):
        data = wav16khz2mfcc(TRAIN_DIR + '/'+ str(i))
        gm = mixture.GaussianMixture(n_components=1)
        data = np.hstack(data).T
        gm.fit(data) 
        gmms.append(gm)
    return gmms

def test_model(model):
    """
        Evaluate model and print results on stdout 
    """
    hit = 0
    total = 0 
    for i in range(CLASS_N):
        data = wav16khz2mfcc(VAL_DIR +'/'+ str(i+1))
        for f in data:
            scores = []
            for g in model:
                scores.append(g.score(f.T))
            if(np.argmax(scores) == i):
                hit += 1
            total += 1

    print("Hits: ", hit, "/", total)
    print("Accuracy:", hit/total)

def eval_model(model):
    """
        Classify files eval files and print results into result file
    """
    data = wav16khz2mfcc(EVAL_DIR)
    f = open(RESULT_FILE, "w")
    stdout = sys.stdout
    sys.stdout = f

    files = glob(EVAL_DIR + '/*.wav')
    i = 0
    for d in data:
        scores = []
        file = os.path.split(files[i])[1]
        i+=1
        file = file.split('.')[0]
        print(file, end=" ")
        for g in model:
            scores.append(g.score(d.T))
        print(np.argmax(scores)+1, end=" ")
        print("NaN")

    sys.stdout = stdout



if __name__ == "__main__":
    model = create_model()
    test_model(model)
    eval_model(model)

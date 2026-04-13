from src.data_loader import load_and_split
from src.preprocess import preprocess_train_test

"""Testing the proprocessing pipeline"""

def test_preprocessing():
    #load and split data - with 80/20 ratio
    X_train, X_test, Y_train, Y_test = load_and_split()

    #processing now
    preprocessor = None
    X_train_proc, X_test_proc, preprocessor = preprocess_train_test(X_train, X_test, preprocessor)

    print(f"Original training set shape: {X_train.shape}")
    print(f"Processed training set shape: {X_train_proc.shape}")

    print(f"Original testing set shape: {X_test.shape}")
    print(f"Processed testing set shape: {X_test_proc.shape}")

if __name__ == "__main__":
    test_preprocessing()




#!./.venv/bin/python
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Define your 7 genres in order
GENRES = ['Action', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Horror', 'Romance']

def train():
    X_list = []
    y_list = []
    
    for i, genre in enumerate(GENRES):
        print(f"Loading {genre} embeddings...")
        embeddings = np.load(f"./data/embeddings/{genre}.npy")
        X_list.append(embeddings)
        y_list.append(np.full(len(embeddings), i)) # Label indices 0-6

    # Combine everything
    print("Concatenating data...")
    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    
    # Optional: Split for validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Logistic Regression (this may take a few minutes)...")
    # Using 'saga' or 'lbfgs' solver for large datasets
    clf = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs', verbose=1)
    clf.fit(X_train, y_train)
    
    # Accuracy check
    score = clf.score(X_test, y_test)
    print(f"Validation Accuracy: {score:.4f}")
    
    # Save the classifier and the genre list
    joblib.dump({'model': clf, 'genres': GENRES}, "./data/genre_classifier.joblib")
    print("Model saved to genre_classifier.joblib")

if __name__ == "__main__":
    train()
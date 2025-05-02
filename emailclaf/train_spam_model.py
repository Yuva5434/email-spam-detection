import pandas as pd
from model import train_model
from utils import mask_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os
import joblib

def load_data(filepath):
    try:
        data = pd.read_csv(filepath, encoding='latin-1')
        # The dataset has columns: Category, Message
        # Remove any unnamed columns if present
        data = data.loc[:, ['Category', 'Message']]
        return data['Message'], data['Category']
    except FileNotFoundError:
        print("File not found. Please check the filepath.")
        return None, None
    except pd.errors.EmptyDataError:
        print("File is empty. Please check the file contents.")
        return None, None

def preprocess_messages(messages):
    return messages.apply(mask_text)

if __name__ == "__main__":
    # Load dataset
    X, y = load_data('data set/email.csv')

    if X is not None and y is not None:
        # Preprocess messages by masking sensitive info
        X_masked = preprocess_messages(X)

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X_masked, y, test_size=0.2, random_state=42)

        # Train model
        clf, vectorizer = train_model(X_train, y_train)

        print("Training completed.")

        # Evaluate on test set
        X_test_vec = vectorizer.transform(X_test)
        y_pred = clf.predict(X_test_vec)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, pos_label='spam')
        recall = recall_score(y_test, y_pred, pos_label='spam')
        f1 = f1_score(y_test, y_pred, pos_label='spam')

        print(f"Evaluation on test set:")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-score: {f1:.4f}")

        # Save model and vectorizer to models folder
        os.makedirs('models', exist_ok=True)
        joblib.dump(clf, os.path.join('models', 'spam_model.pkl'))
        joblib.dump(vectorizer, os.path.join('models', 'vectorizer.pkl'))

        # Test the model on some sample messages
        test_messages = [
            "Congratulations! You've won a free ticket to Bahamas. Call now!",
            "Hey, are we still meeting for dinner tonight?",
            "Please send your bank details to claim your prize.",
            "Can you call me when you get this message?"
        ]

        # Mask test messages
        test_masked = [mask_text(msg) for msg in test_messages]

        # Vectorize test messages
        test_vec = vectorizer.transform(test_masked)

        # Predict
        predictions = clf.predict(test_vec)

        for msg, pred in zip(test_messages, predictions):
            print(f"Message: {msg}\nPredicted label: {pred}\n")

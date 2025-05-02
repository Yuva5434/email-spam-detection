import joblib
from utils import mask_text

# Load the trained model and vectorizer
model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Debug prints to check feature sizes
print(f"Vectorizer vocabulary size: {len(vectorizer.vocabulary_)}")
print(f"Model expected number of features: {model.n_features_in_}")

def check_spam_or_ham(message):
    # Mask sensitive information in the message
    masked_message = mask_text(message)

    # Transform the masked message using the vectorizer
    message_vector = vectorizer.transform([masked_message])

    # Predict the label using the model
    prediction = model.predict(message_vector)[0]

    return prediction

if __name__ == "__main__":
    message = input("Enter the message to classify: ")
    result = check_spam_or_ham(message)
    print(f"The message is classified as: {result}")

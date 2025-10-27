# Install required libraries (run only once)
# pip install transformers torch

from transformers import pipeline

# Load the pre-trained sentiment analysis model
sentiment_classifier = pipeline("sentiment-analysis")

# Take input from the user
text = input("Enter a sentence to analyze sentiment: ")

# Get prediction
result = sentiment_classifier(text)[0]

# Display the result
print(f"\nText: {text}")
print(f"Sentiment: {result['label']}")
print(f"Confidence: {result['score']:.2f}")

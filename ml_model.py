# IntervuAI - Improved ML Model

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training examples
answers = [
    # Good answers
    "Python is a programming language",
    "Machine learning learns from data",
    "AI means artificial intelligence",
    "Python is used for software development",
    "Machine learning uses algorithms to learn",
    "AI helps machines perform intelligent tasks",

    # Average answers
    "Python is useful",
    "Machine learning is about computers",
    "AI is a technology",
    "Python is easy to learn",
    "Machines learn things",
    "AI is used in many fields",

    # Weak answers
    "I don't know",
    "Nothing",
    "I have no idea",
    "I cannot answer",
    "I forgot",
    "Not sure"
]

# Labels
labels = [
    "Good", "Good", "Good", "Good", "Good", "Good",
    "Average", "Average", "Average", "Average", "Average", "Average",
    "Needs Improvement", "Needs Improvement",
    "Needs Improvement", "Needs Improvement",
    "Needs Improvement", "Needs Improvement"
]

# Convert text into numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(answers)

# Train ML model
model = MultinomialNB()
model.fit(X, labels)


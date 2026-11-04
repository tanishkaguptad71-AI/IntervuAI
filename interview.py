from ml_model import model, vectorizer
print("========================================")
print("              INTERVUAI")
print("        AI MOCK INTERVIEW SYSTEM")
print("========================================")

# Step 1: Candidate details

name = input("Enter your name: ")

role = input("Enter your desired job role: ")

print("\nWelcome", name)
print("Your selected role is:", role)

print("\nYour interview is starting!")

# Step 2: Role-based interview questions

if role == "AI/ML Engineer":

    print("\nQuestion 1: What is Artificial Intelligence?")
    answer1 = input("Your answer: ")

    print("\nQuestion 2: What is Machine Learning?")
    answer2 = input("Your answer: ")

    print("\nQuestion 3: What is Python?")
    answer3 = input("Your answer: ")

elif role == "Python Developer":

    print("\nQuestion 1: What is Python?")
    answer1 = input("Your answer: ")

    print("\nQuestion 2: What is a variable?")
    answer2 = input("Your answer: ")

    print("\nQuestion 3: What is a function?")
    answer3 = input("Your answer: ")

else:

    print("\nQuestion 1: Tell me about yourself.")
    answer1 = input("Your answer: ")

    print("\nQuestion 2: What are your strengths?")
    answer2 = input("Your answer: ")

    print("\nQuestion 3: Why should we hire you?")
    answer3 = input("Your answer: ")

# Step 3: Interview completion

print("\n========================================")
print("          INTERVIEW COMPLETED")
print("========================================")

print("Candidate Name:", name)
print("Job Role:", role)

print("Thank you for using IntervuAI!")



# Step 4: Keyword-based answer evaluation

answers = [answer1, answer2, answer3]

keywords = [
    ["human", "intelligence", "machine"],
    ["data", "algorithm", "learn"],
    ["programming", "language", "software"]
]

print("\n===== AI ANSWER REVIEW =====")

for i, answer in enumerate(answers):
    score = 0

    for word in keywords[i]:
        if word in answer.lower():
            score += 1

    print("\nQuestion", i + 1)

    if answer.strip() == "":
        print("No answer provided")

    elif score >= 2:
        print("Good answer!")
        print("Keyword score:", score, "/ 3")

    elif score == 1:
        print("Partially correct. Add more relevant points.")
        print("Keyword score:", score, "/ 3")

    else:
        print("Needs improvement.")
        print("Keyword score:", score, "/ 3")


        # Step 5: Feedback generation

print("\n===== PERSONALIZED FEEDBACK =====")

for i, answer in enumerate(answers):
    if answer.strip() == "":
        print("Question", i + 1, ": Please attempt this question.")

    elif len(answer.strip()) < 20:
        print("Question", i + 1, ": Explain your answer in more detail.")

    else:
        print("Question", i + 1, ": Good effort! Keep improving your technical knowledge.")


        # Step 6: Machine Learning Evaluation

print("\n===== MACHINE LEARNING RESULTS =====")

for i, answer in enumerate(answers, start=1):

    test_data = vectorizer.transform([answer])
    prediction = model.predict(test_data)

    print("Question", i, ":", prediction[0])
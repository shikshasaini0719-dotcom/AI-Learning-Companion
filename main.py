import random
from questions import python_questions , ai_questions, ml_questions

# Show Previous Results
print("===== PREVIOUS RESULTS =====")

try:
    with open("results.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("No previous results found.")

print("\n=============================\n")

# Login
name = input("Enter your name: ")

with open("students.txt", "a") as file:
    file.write(name + "\n")

print(f"\nWelcome {name}!")
print("Let's test your Python knowledge.\n")
 
#Subject selection
print("\nChoose Subject")
print("1. Python")
print("2. AI Basics")
print("3. Machine Learning")

choice = input("Enter your choice (1-3): ")

if choice == "1":
    questions = python_questions
elif choice == "2":
    questions = ai_questions
elif choice == "3":
    questions = ml_questions
else:
    print("Invalid choice")
    exit()


# Select 5 Random Questions
selected_questions = random.sample(questions, 5)

score = 0
weak_topics = []
wrong_questions = []

# Quiz Starts
for q in selected_questions:

    print("\n" + q["question"])
    user_answer = input("Your Answer: ")

    if user_answer.strip().lower() == q["answer"].lower():
        print("✅ Correct!")
        score += 1
    else:
        print(f"❌ Wrong! Correct answer is {q['answer']}")
        wrong_questions.append(q["question"])
        weak_topics.append(q["topic"])

# Result
percentage = (score / 5) * 100

print("\n===== RESULT =====")
print("Student:", name)
print("Score:", score, "/5")
print("Percentage:", percentage, "%")

# opted subject
subject_name = ""

if choice == "1":
    subject_name = "Python"
elif choice == "2":
    subject_name = "AI Basics"
elif choice == "3":
    subject_name = "Machine Learning"

#performance report
print("\n===== PERFORMANCE REPORT =====")
try:
    with open("results.txt", "r") as file:
        lines = file.readlines()

    attempts = 0

    for line in lines:
        if name in line:
            attempts += 1

    print("Previous Attempts:", attempts)

except FileNotFoundError:
    print("Previous Attempts: 0")
print("Student:", name)
print("Subject:", subject_name)
print("Score:", score, "/5")
print("Percentage:", percentage, "%")

print("\n===== TOPICS TO REVIEW =====")

if wrong_questions:
    for question in wrong_questions:
        print("•", question)
else:
    print("Excellent! No mistakes made.")


# Recommendation System
print("\n===== RECOMMENDATIONS =====")

if choice == "1":  # Python
    if percentage < 40:
        print("📚 Revise Python Basics, Functions and Loops.")
    elif percentage < 70:
        print("📝 Practice more Python coding questions.")
    else:
        print("🚀 Start learning OOP, File Handling and Modules.")

elif choice == "2":  # AI
    if percentage < 40:
        print("🤖 Revise AI fundamentals and key concepts.")
    elif percentage < 70:
        print("📝 Practice AI applications and terminology.")
    else:
        print("🚀 Start exploring NLP, Computer Vision and Chatbots.")

elif choice == "3":  # ML
    if percentage < 40:
        print("📊 Revise Machine Learning basics.")
    elif percentage < 70:
        print("📝 Learn more about supervised and unsupervised learning.")
    else:
        print("🚀 Start learning Scikit-Learn, Pandas and Model Building.")

# Save Result
with open("results.txt", "a") as file:
    file.write(
        f"{name} | {subject_name} | Score: {score}/5 | Percentage: {percentage}%\n"
    )

print("\n✅ Result saved successfully.")
with open("leaderboard.txt", "a") as file:
    file.write(
        f"{name}|{subject_name}|{percentage}\n"
    )

print("\n===== LEADERBOARD =====")

try:
    with open("leaderboard.txt", "r") as file:
        records = []

        for line in file:
            data = line.strip().split("|")

            if len(data) == 3:
                records.append(data)

        records.sort(key=lambda x: float(x[2]), reverse=True)

        for i, record in enumerate(records[:5], start=1):
            print(
                f"{i}. {record[0]} ({record[1]}) - {record[2]}%"
            )

except FileNotFoundError:
    print("No leaderboard data available.")
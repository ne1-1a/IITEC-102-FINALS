import sqlite3
import random
import math

DB_NAME = "quiz.db"
NUM_QUESTIONS = 10


# ---------- DATABASE ----------
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS scores ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT, "
        "score INTEGER)"
    )
    conn.commit()
    conn.close()


def save_score(name, score):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()


def show_scores():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT name, score FROM scores ORDER BY score DESC LIMIT 5"
    ).fetchall()
    conn.close()

    print("\n--- Top 5 Scores ---")
    for name, score in rows:
        print(f"{name}: {score}/{NUM_QUESTIONS}")


# ---------- QUESTIONS ----------
def make_question():
    """Pick a random easy question. Returns (question_text, answer)."""
    kind = random.choice(["add", "subtract", "multiply", "sqrt"])

    if kind == "add":
        a, b = random.randint(1, 20), random.randint(1, 20)
        return f"{a} + {b} = ?", a + b

    if kind == "subtract":
        a = random.randint(10, 30)
        b = random.randint(1, a)
        return f"{a} - {b} = ?", a - b

    if kind == "multiply":
        a, b = random.randint(2, 10), random.randint(2, 10)
        return f"{a} x {b} = ?", a * b

    root = random.randint(2, 12)
    return f"What is the square root of {root ** 2}?", int(math.sqrt(root ** 2))


# ---------- QUIZ ----------
def run_quiz():
    score = 0

    for i in range(1, NUM_QUESTIONS + 1):
        question, answer = make_question()
        print(f"\nQuestion {i}: {question}")

        try:
            guess = int(input("Your answer: "))
        except ValueError:
            guess = None

        if guess == answer:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. The answer is {answer}.")

    return score


# ---------- MAIN ----------
def main():
    setup_database()

    name = input("Enter your name: ")
    score = run_quiz()

    print(f"\nFinal score: {score}/{NUM_QUESTIONS}")
    save_score(name, score)
    show_scores()


if __name__ == "__main__":
    main()

# Math Quiz: Code Notes

These notes cover `math_quiz.py` only. There are three parts: a reference of every function the program uses, a walkthrough of the code from top to bottom, and an explanation of how `sqlite3`, `random`, and `math` fit together.

## 1. Function Reference

### Functions defined in the program

| Function | Parameters | Returns | Called by | What it does |
|---|---|---|---|---|
| `setup_database()` | none | nothing | `main()` | Creates `quiz.db` and the `scores` table if they don't exist |
| `save_score(name, score)` | player name (str), score (int) | nothing | `main()` | Inserts one row into `scores` |
| `show_scores()` | none | nothing | `main()` | Prints the top 5 scores |
| `make_question()` | none | tuple: `(question_text, answer)` | `run_quiz()` | Builds one random easy question and its answer |
| `run_quiz()` | none | the score (int) | `main()` | Asks 10 questions, checks answers, counts correct ones |
| `main()` | none | nothing | the `if __name__` line | Runs the whole program in order |

### Functions from `sqlite3`

| Function | Used in | What it does here |
|---|---|---|
| `sqlite3.connect(DB_NAME)` | `setup_database`, `save_score`, `show_scores` | Opens `quiz.db`, or creates it on the first run |
| `conn.execute(sql)` | all three database functions | Runs `CREATE TABLE`, `INSERT`, or `SELECT` |
| `conn.commit()` | `setup_database`, `save_score` | Saves the table or the new score to the file |
| `cursor.fetchall()` | `show_scores` | Turns the SELECT result into a list of `(name, score)` tuples |
| `conn.close()` | all three database functions | Closes the connection |

### Functions from `random`

| Function | Used in | What it does here |
|---|---|---|
| `random.choice(list)` | `make_question` | Picks the question type from `["add", "subtract", "multiply", "sqrt"]` |
| `random.randint(a, b)` | `make_question` | Picks the numbers inside each question. Both ends are included |

### Function from `math`

| Function | Used in | What it does here |
|---|---|---|
| `math.sqrt(x)` | `make_question` | Gets the square root for the square root questions. Returns a float like `9.0` |

### Built-in functions

| Function | Used in | What it does here |
|---|---|---|
| `input(prompt)` | `run_quiz`, `main` | Reads what the player types. Always returns a string |
| `int(value)` | `run_quiz`, `make_question` | Converts the typed answer to a number. Also turns `9.0` into `9` after `math.sqrt` |
| `print(...)` | `run_quiz`, `main`, `show_scores` | Shows text on screen |
| `range(start, stop)` | `run_quiz` | Gives the numbers 1 to 10 for the question loop |

## 2. The Code, Step by Step

### Step 1: Imports and constants

```python
import sqlite3
import random
import math

DB_NAME = "quiz.db"
NUM_QUESTIONS = 10
```

The three imports load the modules. `DB_NAME` and `NUM_QUESTIONS` are constants (written in capitals by convention). They sit at the top so a setting can be changed in one place. Change `NUM_QUESTIONS` to 5 and the quiz, the loop, and the "score out of" display all follow.

### Step 2: `setup_database()`

```python
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
```

1. `connect` opens `quiz.db`. On the very first run the file doesn't exist, so SQLite makes it.
2. `execute` runs the `CREATE TABLE` command. `IF NOT EXISTS` means it only builds the table once. On later runs the command does nothing, so old scores are safe.
3. The table has three columns: `id` (a number that goes up by one for every row), `name`, and `score`.
4. `commit` saves the change.
5. `close` ends the connection.

### Step 3: `save_score(name, score)`

```python
def save_score(name, score):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()
```

The two question marks are placeholders. SQLite fills them from the tuple `(name, score)`, in order. This is safer than putting the name straight into the SQL string, because a player who types something strange as a name can't change the command. Without `commit`, the new row would be thrown away when the program ends.

### Step 4: `show_scores()`

```python
def show_scores():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT name, score FROM scores ORDER BY score DESC LIMIT 5"
    ).fetchall()
    conn.close()

    print("\n--- Top 5 Scores ---")
    for name, score in rows:
        print(f"{name}: {score}/{NUM_QUESTIONS}")
```

1. `SELECT name, score` asks for those two columns.
2. `ORDER BY score DESC` sorts from highest to lowest.
3. `LIMIT 5` keeps only the first five rows.
4. `fetchall()` returns them as a list, for example `[("Ana", 9), ("Ben", 7)]`.
5. The connection closes before printing, because the data is already in the `rows` variable.
6. The `for name, score in rows` loop unpacks each tuple into two variables and prints a line.

If two players tie, SQLite doesn't promise which one is listed first. The program doesn't handle ties.

### Step 5: `make_question()`

```python
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
```

1. `random.choice` picks one of the four type names and stores it in `kind`.
2. The `if` blocks check `kind`. Each block creates its numbers, then **returns** a tuple of question text and answer. A `return` ends the function right away, so only one block ever runs.
3. **Add:** two numbers from 1 to 20.
4. **Subtract:** the first number is 10 to 30, and the second is picked from 1 up to the first. That way the answer is never negative.
5. **Multiply:** two numbers from 2 to 10.
6. **Square root:** none of the three `if` checks matched, so the code falls through to the last lines. `randint(2, 12)` picks the root. The question shows the root squared, and the answer is calculated with `math.sqrt`, then converted with `int()`.

Take a root of 8. The question reads "What is the square root of 64?". `math.sqrt(64)` gives `8.0`, and `int()` makes it `8`.

### Step 6: `run_quiz()`

```python
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
```

1. `score` starts at 0.
2. `range(1, NUM_QUESTIONS + 1)` produces 1 through 10. The stop value is left out, which is why the `+ 1` is there.
3. Each pass calls `make_question()` and unpacks the returned tuple into `question` and `answer`.
4. `input` reads the player's text, and `int` tries to turn it into a number.
5. If the player types something like `abc`, `int` raises a `ValueError`. The `except` block catches it and sets `guess` to `None`, so the program keeps going. `None` never equals a number, so it counts as wrong.
6. If `guess == answer`, the score goes up by one. Otherwise the correct answer is shown.
7. After the loop, `return score` hands the total back to `main()`.

### Step 7: `main()` and the entry point

```python
def main():
    setup_database()

    name = input("Enter your name: ")
    score = run_quiz()

    print(f"\nFinal score: {score}/{NUM_QUESTIONS}")
    save_score(name, score)
    show_scores()


if __name__ == "__main__":
    main()
```

`main()` is the order of events: set up the database, get the name, run the quiz, print the result, save it, show the leaderboard. The last two lines mean `main()` only starts when you run the file directly. If another file imports `math_quiz.py`, nothing runs until that file calls `main()` itself.

## 3. How the Three Modules Work Together

The modules never call each other. They are linked by the **values** the program passes around. Each one handles one stage of the data's trip:

```
random                 math                    sqlite3
  |                      |                       |
  | picks type           |                       |
  | picks numbers        |                       |
  v                      v                       |
make_question() ----> answer calculated          |
  |                    (sqrt questions only)     |
  v                                              |
run_quiz() compares guess with answer            |
  |                                              |
  v                                              v
score (int) ---------------------------> save_score() ---> quiz.db
                                                              |
                                                              v
                                         show_scores() <--- top 5 rows
```

| Stage | Module | What happens |
|---|---|---|
| Creating the question | `random` | Picks the type and the numbers, so every quiz is different |
| Solving the question | `math` | Calculates the answer when the type is a square root |
| Remembering the result | `sqlite3` | Stores the final score and reads the top 5 back |

Here is `random` and `math` meeting inside one line of code:

```python
root = random.randint(2, 12)                      # random makes the number
return f"...{root ** 2}?", int(math.sqrt(root ** 2))   # math solves it
```

`random` supplies the root, and `math.sqrt` works backwards from its square to check it. Then the result moves on to `run_quiz()` and, at the end, to `sqlite3`.

### One full run, traced

Say the player is Ana, and the quiz produces these questions (shortened to four for the example):

| Question | Made by | Answer | Ana's guess | Result |
|---|---|---|---|---|
| 14 + 6 = ? | `random` | 20 | 20 | Correct |
| 9 x 7 = ? | `random` | 63 | 56 | Wrong |
| Square root of 49 | `random` picks 7, `math.sqrt` solves | 7 | 7 | Correct |
| 25 - 11 = ? | `random` | 14 | abc | Wrong (`ValueError` caught) |

After all 10 questions, suppose her score is 8. Then:

1. `save_score("Ana", 8)` writes a row to `quiz.db`: `(1, "Ana", 8)`.
2. `show_scores()` reads the five best rows back and prints `Ana: 8/10`.
3. The next time the program runs, that row is still in the file, so Ana's score shows up on the leaderboard next to the new player's.

That last point is the reason `sqlite3` is in the project. `random` and `math` only matter while the program is running. `sqlite3` is the only module whose work is still there afterward.

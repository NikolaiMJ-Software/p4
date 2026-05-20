# RogueLiteScript
This domain-specific natural language programming language aimed at lowering the barrier to entry for aspiring indie game developers, specifically within the Roguelite genre. Traditional programming languages often present steep learning curves that hinder new developers from making games. To address this, the proposed language utilizes a human-readable, Subject-Verb-Object syntax to minimize ambiguity while maximizing accessibility. Genre-specific mechanics, such as procedural randomness and permachoice persistence, are built-in features. Implemented as a strongly and dynamically typed interpreted language using the parser Lark, the system employs type inference to simplify development.

## Features

### Indentation-based syntax

Code blocks are defined through indentation. Each statement must be written on its own line.

```text
create Health is 10

if Health greater than 0 do:
    output "Still alive"
```

### Save States:
Persistent game state is handled through a reserved `Game` struct.
Only values stored inside `Game` are saved between program runs.

The `Play` function acts as the program entry point.
```text
create Game with:
    Health is 100
    Gold is 0

define Play:
    output "Welcome back!"
    output "Gold:", Gold from Game

    Gold from Game is Gold from Game + 10
```

### Syntax:
#### Variables:

Variables are created using `create` and assigned using `is`.
```text
create Name
Name is "Hero"

create Health is 100
Health is Health - 10
```

#### Arithmetic expressions:

The language supports common arithmetic operators.

```text
create Damage is 10 + 5
create Health is 100 - Damage
create Total is Damage * 2
create Half is Health / 2
create Power is 2 ^ 3
```

Supported Arithmetic operators:

```text
+   (numeric addition or string concatenation)
-   (numeric subtraction)
*   (numeric multiplication)
/   (numeric division)
^   (power/exponentiation)
```

#### Boolean logic:

Boolean expressions can be combined using `and`, `or`, `not`, and `either` ... `or` ....

```text
create Alive is true
create HasPotion is false

if Alive and not HasPotion do:
    output "Still alive, but no potion"

if either Alive or HasPotion do:
    output "At least one condition is true"
```

#### Lists:

Lists are created using `listing:` and accessed using `index`

```text
create Inventory is listing: "Sword", "Potion", "Key"

output index 0 of Inventory
index 1 of Inventory is "Health Potion"
```

Nested indexes can be used to access lists inside lists.

```text
create Rooms is listing: "Key", "Coin", listing: "Sword", "Shield"

index 1 of Rooms is "Key 1", "Key 2"

output index 1 of index 2 of Rooms
```

#### Structs and inheritance:

Structs group related values together using `with:`.

Struct fields can be created with or without an initial value.

A struct can inherit fields from another struct using `from`.

```text
create Character with:
    Health is 100
    Damage is 10
    Name

create Player from Character with:
    Name is "Hero"

output Health from Player
output Name from Player

Health from Player is 80
```


#### Conditions:

Conditions use readable comparison keywords.

```text
if Health from Player greater than 0 do:
    output "Alive"
else do:
    output "Dead"
```
Supported comparisons:

```text
equal                     (same as ==)
not equal                 (same as !=)
greater than              (same as >)
greater than or equal to  (same as >=)
less than                 (same as <)
less than or equal to     (same as <=)
```

#### Loops:

The language supports while, do-while, range-based loops, and list-based loops.

```text
while Health from Player greater than 0 do:
    Health from Player is Health from Player - 10

do:
    output "This runs at least once"
while Health from Player greater than 0

for each X from 1 to 5 do:
    output X

for each Item in Inventory do:
    output Item
```

Loops can be exited early using `stop`.

```text
for each Item in Inventory do:
    if Item equal "Potion" do:
        output "Potion found"
        stop
```

#### Functions:

Functions are defined using `define` and executed using `call`.

```text
define Attack with Damage:
    output "You dealt", Damage, "damage"

call Attack with 10
```

Functions can optionally take parameters using `with`.

```text
define Attack with Damage:
    output "You dealt", Damage, "damage"

call Attack with 10
```

Functions can return values using `return`.

```text
define Add with A, B:
    return A + B

create Result is call Add with 5, 10
output Result
```

#### Input and Output:

The language supports basic `input` and `output`.

```text
create Answer

output "What is your name?"
input in Answer

output "Hello", Answer
```

#### Roguelike features:

The language includes built-in randomness features for roguelike-style mechanics.

`between` generates a random numeric value within a range.

`chance` evaluates to either `true` or `false` based on probability. It can be written either as a percentage or as an `x in y` chance.

```text
create Damage is between 5 and 15

create CriticalHit is chance 25%
create RareDrop is chance 1 in 100

if CriticalHit do:
    output "Critical hit!"
```

#### Comments:

Comments can be written as either single-line or multi-line comments.

Single-line comments use `#`.

Multi-line comments use `#/` and `/#`.

```text
# output statement
output "hello"

#/
This is a
multi-line comment
/#

output "goodbye"
```

## Technologies Used
- LARK (parser)
- Pytest (tests)

## Project Structure
```plaintext
P4/
├── src/
│   ├── ast/            # AST builder and nodes
│   ├── runtime/        # File I/O functionality
│   ├── visitors/       # Visitors for the AST (interpreter, and type checker)
│   ├── errors.py       # Error system for the language
│   └── parser.py       # Lark parser
├── test/               # Different tests
├── app.py              # The main program
└── main.rls            # File to write code
```

## Getting Started
### Prerequisites
- Python 3

### Setup the project
1.	Clone the repository:
```bash
git clone https://github.com/NikolaiMJ-Software/p4.git
```
2. Navigate to the project directory:
```bash
cd p4
```
3. Create virtual environment:
```bash
python -m venv .venv
```

4. Activate venv folder:
```bash
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the app for the first time
1. Write some code in `main.rls`

2. Start the program:
```bash
python app.py
```

### Running tests
Run all tests:
```bash
python -m pytest
```

Run a specific test file:
```bash
python -m pytest test/{test_dir_and_name}
```

# Contributing
Contributions are welcome! Follow these steps:
1. Make sure you are on `staging` and it is up to date.
```bash
git switch staging
git pull
```

2. Create a branch for your feature or bugfix:
```bash
git switch -c feat/feature-name
# or
git switch -c bugfix/bug-name
```

3. Commit your changes:
```bash
# If dependencies changed
pip freeze > requirements.txt

git commit
# Write commit message in opened editor, save and exit editor
```

4. Push local branch to remote:
```bash
git push origin feature-name
```
5. Open a pull request to `staging` and test it, and then create a new pull request for main.
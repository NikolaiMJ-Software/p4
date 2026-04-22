# p4
Some sort of program language

## Features


## Technologies Used
- LARK (parser)

## Project Structure
```plaintext

```

## Getting Started
### Prerequisites


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
1. Write some code in `main.rouge`

2. Start the program:
```bash
python app.py main.rouge
```

### Running tests
Run all tests:
```bash
python -m pytest
```

Run a specific test file:
```bash
python -m pytest src/Testing/{test_dir_and_name}
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
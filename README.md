# Student Course Allocation System

## Project Description

The Student Course Allocation System is designed to efficiently allocate students to courses based on their preferences
and priorities. It supports both a basic allocation algorithm and a more complex genetic algorithm to optimize the
distribution of students across available courses.

## Demo

*Screenshots or a video link demonstrating the system in action.*

## Project Installation / Deployment

1. Ensure Python 3.12 or higher is installed.
2. Clone the repository to your local machine.
3. Navigate to the project directory.
4. Install required dependencies with

```shell
pip install -r requirements.txt
```

## How to Use

To use the system, follow these steps:

1. Student and course information should be provided in Excel files.
   Student information should be named `Student table.xlsx` and have columns like the example.
   Course information should be named `Courses table.xlsx` and have columns like the example.
   Results will be written to a file named `path/to/students.json` (make sure to change `path/to/students.json` to your
   actual path and prefered name of file).
2. The system supports converting Excel files to JSON format and then distributing students to courses based on
   preferences and priorities.
   To convert Excel files to JSON and run the distribution algorithm, execute the following command in your terminal:

```shell
python algorithm_cli.py --convert --courses Courses.xlsx --students Students1.xlsx --students2 Students2.xlsx --output path/to/students.json
```

This command will convert the specified Excel files for courses and students into JSON format, merge the student
information.

To run algorithm with converted JSON files, execute the following command in your terminal:

```shell
python algorithm_cli.py --courses path\to\courses.json --students path\to\students.json --output path\to\distribution.json
```

Available flags for converting:

- `--convert`: Convert Excel files to JSON.
- `--courses`: Path to the courses Excel file.
- `--students1`: Path to the first students Excel file.
- `--students2`: Path to the second students Excel file.
- `--output`: Path to the output JSON file.

Available flags for running the algorithm:

- `--courses`: Path to the courses JSON file.
- `--students1`: Path to the students JSON file.
- `--output`: Path to the output JSON file.

## Features

- Converts student and course information from Excel to JSON.
- Supports a basic algorithm for student course allocation.
- Reads student and course information from Excel files.
- Writes allocation results to a JSON file.
- Configurable through command line flags.

## Frameworks or Technology

- **Language:** `Python`
- **Package Manager:** `pip`
- **External Libraries:** `xlwt` for writing Excel files, `openpyxl` for reading Excel files, `pytest` for testing.



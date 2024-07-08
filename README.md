# Student Course Allocation System

## Project Description

The Student Course Allocation System is designed to efficiently allocate students to courses based on their preferences
and priorities. It supports both a basic allocation algorithm and a more complex genetic algorithm to optimize the
distribution of students across available courses.

## Demo

*Screenshots or a video link demonstrating the system in action.*

## How to Use

To use the system, follow these steps:

1. Student and course information should be provided in Excel files.
   Student information should be named `Student table.xlsx` and have columns like the example.
   Course information should be named `Courses table.xlsx` and have columns like the example.
   Results will be written to a file named `Results.xlsx`.
2. System supports basic algorithm and genetic algorithm (**work in progress**) for student allocation to courses.
   To run the system with basic algorithm, execute the following command in your terminal:

```shell
python algorithm_cli.py --read-courses --read-students --distribute --write-results --algorithm basic
```

To run the system with genetic algorithm, execute the following command in your terminal:

```shell
python algorithm_cli.py --read-courses --read-students --distribute --write-results --algorithm gen
```

These commands will read course and student information, distribute students to courses using specified algorithm, and
write the results to an Excel file.

Available flags:

- `--read-courses`: Read courses information from the specified Excel file.
- `--read-students`: Read students information from the specified Excel file.
- `--distribute`: Distribute students to courses based on preferences and priorities.
- `--write-results`: Write the final allocation results to an Excel file.
- `--algorithm`: Specify the algorithm to use for student allocation. Options: `basic`, `gen`.

## Features

- Supports two algorithms for student course allocation: Basic and Genetic Algorithm.
- Reads student and course information from Excel files.
- Writes allocation results to an Excel file.
- Configurable through command line flags.

## Project Installation / Deployment

1. Ensure Python 3.9 or higher is installed.
2. Clone the repository to your local machine.
3. Navigate to the project directory.
4. Install required dependencies with 
```shell
pip install -r requirements.txt
```

## Frameworks or Technology

- **Language:** `Python`
- **Package Manager:** `pip`
- **External Libraries:** `xlwt` for writing Excel files, `openpyxl` for reading Excel files, `pytest` for testing.



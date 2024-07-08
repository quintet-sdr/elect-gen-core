# Student Course Allocation System

## Installation

1. Ensure Python 3.9 or higher is installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory and install required dependencies:
   ```shell
   pip install -r requirements.txt
    ```

## Usage
Student and course information should be provided in Excel files.
Student information should be named `Student table.xlsx` and have columns like the example.
Course information should be named `Courses table.xlsx` and have columns like the example.
Results will be written to a file named `Results.xlsx`.

System supports basic algorithm and genetic algorithm (**work in progress**) for student allocation to courses.

To run the system with basic algorithm, execute the following command in your terminal:
```shell
python algorithm_cli.py --read-courses --read-students --distribute --write-results --algorithm basic
```


To run the system with genetic algorithm, execute the following command in your terminal:
```shell
python algorithm_cli.py --read-courses --read-students --distribute --write-results --algorithm gen
```
These commands will read course and student information, distribute students to courses using specified algorithm, and write the results to an Excel file.

Available flags:
- `--read-courses`: Read courses information from the specified Excel file.
- `--read-students`: Read students information from the specified Excel file.
- `--distribute`: Distribute students to courses based on preferences and priorities.
- `--write-results`: Write the final allocation results to an Excel file.
- `--algorithm`: Specify the algorithm to use for student allocation. Options: `basic`, `gen`.



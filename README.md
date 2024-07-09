# Elect.Gen Core

This repository is a service of the
[Elect.Gen](https://gitlab.pg.innopolis.university/sdr-sum24/elect-gen) project.
Navigate there to learn more.

## 🧰 Tooling

- 🐍 Programming language: [Python](https://github.com/python/cpython)
- 📦 Package manager: [Pip](https://github.com/pypa/pip)
- 📚 External Libraries: `xlwt` for writing Excel files, `openpyxl` for reading Excel files, `pytest` for testing.

## 🖥️ Launch locally

<details open>
<summary open>
<b>Clone the entire project (recommended):</b>
</summary>

### Clone the main repository

For example, you can do it via HTTPS:

```console
git clone --recurse-submodules https://gitlab.pg.innopolis.university/sdr-sum24/elect-gen.git
```

### Open the core directory

```shell
cd elect-gen/services/core/
```

</details>

<details>
<summary>
<b>Clone the core only:</b>
</summary>

> We recommend you not follow this option.

### Clone the core repository

For example, you can do it via HTTPS:

```console
git clone https://gitlab.pg.innopolis.university/sdr-sum24/elect-gen-core.git
```
### Open the cloned directory

```shell
cd elect-gen-backend/
```

</details>

### How to use

Make sure you have the follows:

1. Ensure Python 3.9 or higher is installed.
2. Clone the repository to your local machine.
3. Navigate to the project directory.
4. Install required dependencies with 
```shell
pip install -r requirements.txt
```
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

**BROKEN:** To run the system with genetic algorithm, execute the following command in your terminal:

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

## ✨ Features

- Supports two algorithms for student course allocation: Basic and Genetic Algorithm.
- Reads student and course information from Excel files.
- Writes allocation results to an Excel file.
- Configurable through command line flags.

## 📄 License

The project is licensed under the [MIT License](/LICENSE).

(c) [SDR](https://gitlab.pg.innopolis.university/sdr-sum24/) /
[Innopolis University](https://innopolis.university/en/). All rights reserved.





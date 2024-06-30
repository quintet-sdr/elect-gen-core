# Instructions to start the algorihtm

1. Create new empty folder on your device.
2. Create Excel File for the Students and Excel File for the Courses (you can see and\or download examples of Course table: https://gitlab.pg.innopolis.university/sdr-sum24/elect-gen-core/-/blob/main/Course%20table.xlsx?ref_type=heads and Student table: https://gitlab.pg.innopolis.university/sdr-sum24/elect-gen-core/-/blob/main/Students%20table.xlsx?ref_type=heads.
3. Start Docker app.
4. Start terminal in this folder.
5. Pull Docker image ```docker pull lanebo1/elect-gen-core```.
6. Run Docker image ```docker run -p 5801:5801 -v .:/app/data --rm -it lanebo1/elect-gen-core```.
7. Open browser at http://localhost:5801/ and click `Connect` to connect to the virtual desktop.
8. Select Keywords file (.txt): `/app/pystsup/test/acm.txt`.
9. Select Students File and Course File.
10. Select path and name of Result File.
11. Click `Start Genetic Algorithm` (Running logs will appear in the terminal).
12. After running of the algorithm Result Ecxel File will appear in the selected directory.

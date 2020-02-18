### Checksum checker
The program verifies checksums (located in a text file) for a set of files by recalculating the values using a predefined algorithm.

Checksum is an alphanumeric sequence that is calculated for a file and can be used to verify its identity. Ideally, a checksum should be unique for a file, but there may be a checksum collision, i.e. two files have the same checksum. This topic is beyond the scope of this description.
 

The program should be started as `thirs_task.py <path to file with files' information> <path to directory with files to check checksum value on>`.

1 CLI argument: The text file with files' information consisting of a number of 'file name - checksum algorithm - checksum value' sets (each three on its line).

2 CLI argument: The directory with files for each of which a calculated checksum will be compared to a value from a text file (1 CLI argument). 

Algorithm:
1. Check if all CLI arguments are passed.
2. Create 2 variables: the first one to store text file's path, the second one to store file's directory path.
3. For each line in the text file:

   3.1. Split the line and create `file_name`, `algorithm`, `checksum` variables for each line (set) member if the line's format is valid. If not, skip the line.
   
   3.2. Calculate the checksum for the `file_name` if the file is in the directory and define if the calculated value equals the one in file.

Supported checksum algorithms are sha1, sha245, md5.

#### Usage example:
`python3 third_task.py /home/linux/IdeaProjects/task/input.txt /home/linuxlite/IdeaProjects/task/files`

Input.txt:
```text
1.txt md5 838ece1033bf7c7468e873e79ba2a3ec
2.txt md5 2d940b11e5a900a6d7930be8ad9b60c7
3.txt sha1 37c965a8d6d7bec292c7b11ff315d9ea
4.txt md5 3c25155ecee7b86584736915de7b68f
5.txt md5 3c215155ecee7b86584736915de7b68f
doc2.txt md5 3c215155ecee7b86584736915de7b68f
```

Files in /home/linuxlite/IdeaProjects/task/files:
* '1.txt'
* '2.txt'
* '3.txt'
* '4.txt'
* 'text_file.txt'

Output:
```text
2020-02-18 11:36:48,214 - INFO - 1.txt OK
2020-02-18 11:36:48,214 - INFO - 2.txt OK
2020-02-18 11:36:48,214 - INFO - 3.txt FAIL
2020-02-18 11:36:48,214 - INFO - 4.txt FAIL
2020-02-18 11:36:48,214 - INFO - 5.txt NOT FOUND
2020-02-18 11:36:48,215 - INFO - doc2.txt NOT FOUND
```

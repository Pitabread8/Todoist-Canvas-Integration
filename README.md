# Canvas to Todoist Integration
This script adds all (new) Canvas assignments due in the next five days to Todoist.

# Setup

1. For the APIs to work, replace the `{TOKEN}` placeholders in [main.py](main.py). You'll need two personal tokens, one from [Canvas](https://canvas.instructure.com/doc/api/file.oauth.html) and one from [Todoist](https://developer.todoist.com/rest/v2/#authorization).

2. My Todoist is set up so that courses are grouped up into different projects and each one has its own section. In [data.json](data.json), for each course, fill out the Canvas course name (as it was set by the instructor) and the respective project and section IDs.

3. You'll need to use the cron command-line utility for adding tasks automatically. The following code will run the script every hour (as long as the computer is on). Make sure to replace the `{DIRECTORY}` placeholder with your computer's directory.
    ```bash
    0 * * * * cd {DIRECTORY} && /usr/local/bin/python3 main.py >>{DIRECTORY}/output.txt
    ```

    In order to avoid duplicating tasks, the tasks are listed in the currently empty list in [tasks.json](tasks.json). It'll automatically update.
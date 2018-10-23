# ReCell : Django Application

## Getting set up

1. Download this repository using git clone:

    ```
    git clone https://github.com/naitemach/ReCell.git
    ```

2. Set up a virtual environment which uses Python 3.  You may need to
[install virtualenv](sudo apt install python3-venv) and/or
[install Python 3](https://www.python.org/downloads/release/python-364/).
Once you've got everything installed, you can create a virtualenv with the
following command (Run it in ReCell Directory) :

    ```
    python3 -m venv virtualenv
    ```

   Then, you can run the virtual environment with the command:

    ```
    source virtualenv/bin/activate
    ```

3. Next, install the project requirements:

    ```
    pip install -r requirements.txt
    ```

4. Run the project and check that everything’s working.  Navigate to the
ReCell directory and run:

    ```
    python manage.py runserver
    ```

   Then, you can open up the project in your browser.  You should see a message
   telling you that you've finished setting up.
   
## Git Cheat 
1. Make your branch
    ```
    git branch branchname
    ```
2. Checking out / Using your branch
    ```
    git checkout branchname
3. Add your changes and commit.
   Push your code to your branch and make a pull request
   ```
   git push origin branchname
   ```

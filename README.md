
## Install Poetry

### MacOS and Linux

- Open `Terminal` and run following command

`curl -sSL https://install.python-poetry.org | python3 -`


### Windows

- Open Powershell and run following command

`(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`


## Clone/Download Project from

- `https://github.com/pywaker/flask_ims.git`
- Extract Project if you have downloaded as zip file


## Run Project

- `cd flask_ims`
- `poetry install`
- `poetry run flask --debug --app main run`


### Running chapters

- `poetry run flask --debug --app chapter1.main run`
- `poetry run flask --debug --app chapter2.main run`
- `poetry run flask --debug --app chapter3.main run`
- `poetry install`
- `poetry run flask --debug --app chapter4.main run`


## Chapters

- [x] chapter 1: flask basics
- [x] chapter 2: flask routes and templates
- [x] chapter 3: simple login with flask session
- [x] chapter 4: flask login
- [ ] chapter 5: add user and add item
- [ ] chapter 6: activate and deactivate user
- [ ] chapter 7: borrow and return item
- [ ] chapter 8: use persistent database
- [ ] chapter 9: use cli command

## Data
Admin
    Add User
        User: (user-id, email, password, role, fullname, is_active, datetime)
        Borrowed Items: (item-id, status, datetime) status: Pending, Received, Returning, Returned
    Add Item
        Item: (item-id, name, count)
    Deactivate User
    Reactivate User
    Accept Borrow request
    Acknowledge return request
    List all items
    List all users
    List all items borrowed by a user

User
    Borrow Item (pending)
    Return Item (pending)
    List my items


Cli command to create super user
Dashboard based on user role ( Admin -> User )
# ssr_whiteboard

Graphical web front-end to manage your crossfit workouts results written in Python/Flask.

## Built With

* SQlite3
* Flask
* Flask-Bcrypt
* W3.CSS

## Getting Started

### Installation

1. Clone the repository
```sh
git clone https://github.com/tmaegel/ssr_whiteboard
```

2. Create virtual environment and install requirements
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Generate SECRET_KEY with python console
```
import secrets
secrets.token_urlsafe(32)
```

4. Put config.py to instance/ and change SECRET_KEY
```
DEBUG = False
SECRET_KEY = 'CHANGEME'
DATABASE = 'instance/whiteboard.sqlite'
TIMEZONE = 'Europe/Berlin'
```

5. Initialize databases and create a first user to log in

```
make init_db
sqlite3 instance/whiteboard.sqlite 'INSERT INTO table_users(name, password) VALUES ("admin", "$2b$12$ypVgiQ4MU2F5AP8BUSxUmu4w9tyLZkjCShZMxp4XwoNWyfbVA/Jly");'
sqlite3 instance/whiteboard.sqlite 'INSERT INTO table_users(name, password) VALUES ("user", "$2b$12$ypVgiQ4MU2F5AP8BUSxUmu4w9tyLZkjCShZMxp4XwoNWyfbVA/Jly");'
```

This add two user (admin, user) with the default password 'secret'. The password can be change in the application.

6. Build and run
```sh
cd ssr_whiteboard/
make run
```

7. Access on http://localhost:8080

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

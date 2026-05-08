# AirBnB Clone — v3 (REST API)

Third stage of the Holberton School **AirBnB clone** project. Builds on top of [v2](https://github.com/TeoVH/holbertonschool-AirBnB_clone_v2) by exposing all the existing models through a versioned **JSON REST API** powered by Flask.

The previous capabilities are preserved: command interpreter (`console.py`), pluggable storage (`FileStorage` / `DBStorage`), Flask web layer (`web_flask/`) and Fabric deployment scripts.

## What's new in v3

- **`api/v1/`** — versioned REST API with one Flask Blueprint per resource.
- **Endpoints** for `State`, `City`, `Amenity`, `User`, `Place`, `Review` and `Place ↔ Amenity` relationships.
- **Status & stats endpoints**: `GET /api/v1/status` and `GET /api/v1/stats`.
- **JSON 404 handler** so error responses stay consistent with the API contract.
- **`storage.get(cls, id)`** and **`storage.count(cls)`** helpers on the storage engines.
- **API host/port via env vars**: `HBNB_API_HOST` and `HBNB_API_PORT`.

## API Endpoints

Base URL: `http://0.0.0.0:5000/api/v1`

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/status` | Service health check |
| `GET`  | `/stats`  | Counts of each object type |
| `GET`  | `/states` | List all states |
| `GET`  | `/states/<state_id>` | Retrieve a single state |
| `POST` | `/states` | Create a state |
| `PUT`  | `/states/<state_id>` | Update a state |
| `DELETE` | `/states/<state_id>` | Delete a state |
| `GET`  | `/states/<state_id>/cities` | List cities of a state |
| `POST` | `/states/<state_id>/cities` | Create a city in a state |
| `GET`/`POST`/`PUT`/`DELETE` | `/cities/<city_id>` | CRUD on a city |
| `GET`/`POST`/`PUT`/`DELETE` | `/users[/<user_id>]` | CRUD on users |
| `GET`/`POST`/`PUT`/`DELETE` | `/amenities[/<amenity_id>]` | CRUD on amenities |
| `GET`/`POST`/`PUT`/`DELETE` | `/cities/<city_id>/places[/<place_id>]` | CRUD on places of a city |
| `GET`/`POST`/`PUT`/`DELETE` | `/places/<place_id>/reviews[/<review_id>]` | CRUD on reviews of a place |
| `GET`/`POST`/`DELETE` | `/places/<place_id>/amenities[/<amenity_id>]` | Manage place amenities |

## Project Structure

| Path | Description |
|------|-------------|
| [`api/v1/app.py`](./api/v1/app.py) | Flask app factory — registers the `app_views` Blueprint, JSON 404 handler, teardown hook |
| [`api/v1/views/`](./api/v1/views) | One module per resource (`states`, `cities`, `amenities`, `users`, `places`, `places_reviews`, `places_amenities`) |
| [`models/`](./models) | Domain classes (`BaseModel`, `User`, `State`, `City`, `Place`, `Amenity`, `Review`) |
| [`models/engine/`](./models/engine) | `FileStorage` (JSON) and `DBStorage` (SQLAlchemy + MySQL) |
| [`console.py`](./console.py) | Command interpreter (carried over from v1/v2) |
| [`web_flask/`](./web_flask) | Server-rendered Flask views (carried over from v2) |
| [`web_static/`](./web_static) | Static front-end prototype |
| [`tests/`](./tests) | `unittest` suite |
| [`setup_mysql_dev.sql`](./setup_mysql_dev.sql) / [`setup_mysql_test.sql`](./setup_mysql_test.sql) | DB bootstrap scripts |
| `0-3-*.{sh,py}`, `100-*.py` | Fabric/Bash deployment scripts |

## Setup & Run

### 1. Clone

```bash
git clone https://github.com/TeoVH/holbertonschool-AirBnB_clone_v3.git
cd holbertonschool-AirBnB_clone_v3
```

### 2. (Optional) Bootstrap MySQL

```bash
cat setup_mysql_dev.sql  | mysql -uroot -p
cat setup_mysql_test.sql | mysql -uroot -p
```

### 3. Run the API

```bash
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db \
HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 \
python3 -m api.v1.app
```

Quick smoke test:

```bash
curl http://0.0.0.0:5000/api/v1/status
# {"status":"OK"}
```

### 4. Run the console

```bash
./console.py
```

### 5. Run the tests

```bash
python3 -m unittest discover tests
```

## Tech Stack

- **Python 3** — `Flask`, `SQLAlchemy`, `cmd`, `unittest`, `Fabric`
- **MySQL** (production) / **JSON file storage** (development)
- **Nginx** on the deployment targets

## Authors

This repository builds on the [original AirBnB_clone v3](https://github.com/justinmajetich/AirBnB_clone) line; the original `AUTHORS` file is preserved. Contributions to this fork:

- [Mateo Villada](https://github.com/TeoVH)
- [Zapata9664](https://github.com/Zapata9664)

## Acknowledgments

Project completed as part of the [Holberton School](https://www.holbertonschool.com/) curriculum.

# BantuKurir-TSP

## Algorithm Used for TSP

Branch and Bound algorithm is used to approximate TSP.

- Cost of every state represents the lower bound to reach our goal from the state
- Cost of every state is calculated using reduced cost matrix.
  A matrix is "reduced cost" if every column and row contains at least one 0, and other elements are not negative.
- Let R, the i-th location be current state and S, the j-th location be next state.
- The cost of S is sum of cost of R, "distance" between R and S, and all subtractor.

## Backend

[Flask](https://flask.palletsprojects.com/en/2.0.x/) is also used for the backend, together with [MySQL](https://www.mysql.com/) as the database platform.
One big reason of using these two are the "direct" connection of python and MySQL. Using only library and query strings to be able to connect.

## Frontend

Pure [Flask](https://flask.palletsprojects.com/en/2.0.x/) is used for the frontend as the same framework is also used for backend

## Setting up for the first time

- fill blanks in `.env.example` with your MySQL database authorization. DB_NAME and TABLE_NAME are optional.
- run `./setup`

## Setting up manually

- fill blanks in `.env.example` with your MySQL database authorization. DB_NAME and TABLE_NAME are optional.
- run `pip install -r requirements.txt`
- rename `.env.example` to `.env`. \
  If you cannot rename manually, run `mv .env.example .env` instead
- run `python app.py` and open [http://localhost:5000](http://localhost:5000)

## Running the app

run `python app.py`

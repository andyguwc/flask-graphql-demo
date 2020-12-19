# Flask GraphQL Demo App

## Overview
This app implements a simple HackerNews clone using Flask, React, and GraphQL.

### Stack
Backend
- Flask server with any SQL dadatabase (supported by SQLAlchemy)
- GraphQL endpoint for fetching and manipulating data

Frontend
- React frontend generated from `create-react-app`
- Apollo Client to consume from the graphQL endpoint

### Features
Account mangement
- Basic login, logout
- Only logged in users can submit posts and votes

Post and votes
- Submit posts and votes

Search posts based on text pattern

<br>

## Getting Started

### Docker Based

To start the application as a docker container with postgreSQL db
```
cp .env.dist .env
make bootstrap
```
View on `localhost:5000`

With graphiQL endpoint `localhost:5000/graphql`


### Local Install

To develop locally without docker
```
# Start a virtualenv
python3 -m venv venv
source venv/bin/activate

# Set the env variables, etc.
# Without SQLALCHEMY_DATABASE_URI from .env the app generates a sqlite app.db 
export $(grep -v '^#' .env | xargs)

# Install dependencies
pip install -r requirements.txt

# Boot up and run flask at :5000
flask db upgrade
flask run

# Enable frontend, which start react server and proxies traffic from `localhost:3000` to `localhost:5000`
cd client
npm install
npm run start
```

View on `localhost:3000`

With graphiQL endpoint `localhost:5000/graphql`

<br>

## Credits

The backend on Flask and Graphene is based on this [blog](https://medium.com/@n.raj.suthar/building-a-mini-blogger-with-graphene-and-react-hooks-api-1deb06cf2d47)

Then frontend with Apollo Client is based on this [tutorial](https://www.howtographql.com/react-apollo/0-introduction/)
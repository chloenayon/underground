# Underground
------
Cultivate your favorite places around the city!

[Live Site](http://undergroundapp.herokuapp.com)
##
https://www.youtube.com/watch?v=DHAs6_p2wEw

## Pages
- `/` Home Page
- `/login` Login Page
- `/signup` Sign up Page
- `/users/<username>` User Profile Page
- `/users/<username>/edit` Edit User Page
- `/users/<username>/favorites` User Favorites Page
- `/places/create` Create Place Page
- `/places/place_id` View Place Page
- `/places/place_id/edit` Edit Place Page
- `/search` Search Page

## Models

### User
- first_name: `String`
- last_name: `String`
- username: `String`
- email: `Email`
- password: `String`
- favorites: [`Places`]

### Place
- name: `String`
- description: `String`
- location: `GeoPoint`
- address: `String`
- user: `User` (author)

### Comment
- user: `User` (author)
- place: `Place`
- text: `String`
- date: `DateTime`


## Installation
`$ pip install flask mongoengine`

## Run
`$ python app.py`

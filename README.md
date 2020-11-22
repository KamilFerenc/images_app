# Images app

## Information
- For local development and testing fixtures have been created:
  - For all created users: username `admin, test_basic, test_premium, test_enterprise` password is the same -  `images_app`
  - 3 tests `AccountTier` model instance have been created 
  - 2 tests `Thumbnail settings` model instance have been created (height 200, 400 px)

## Setup
*Requirements*
 - It is required to have Docker installed

1) Clone repository `git clone https://github.com/KamilFerenc/images_app.git`
2) Go to project directory `cd images_app`
3) Run command `docker build .`
4) Run command `docker-compose up`
5) Open new terminal tab and run command `docker-compose exec backend bash`
6) Run command `python manage.py loaddata fixtures/*.yaml` and exit container `ctrl+d`
5) Open browser eg. `http://127.0.0.1:8000/admin/`
7) Login `username: admin, password: images_app`
6) Check already created test models instances `Users, Account tiers, Thumbnail settings`

## Endpoints
Base url `http://127.0.0.1:8000/`
1) `GET api/login/` - login view 
2) `POST api/logout/` - logout view
3) `POST api/user/` - basic information about user (if logged) (here you can find user id (pk))
4) `POST api/users/<id>/` - user detail - returns list of all user images with thumbnails
5) `POST api/images/add/` - add image
6) `POST api/images/generate-link/` - generate temporary link for image
7) `GET api/images/<link_suffix>/` - temporary link which expires after certain time period, in response returns link to original image 

## Create Account Tier plan - admin panel
1) Create required Thumbnail settings (max height, thumbnail_prefix, display name)
2) Create Account Tier - select checkbox for the original image and generate temporary link if required and add thumbails 

## Tests
1) Login into container `docker-compose run backend bash`
2) Run command `python manage.py test`

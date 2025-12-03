## Setup:
    - pip install -r requirements.txt
    - python3 manage.py migrate
    - python3 manage.py seeder
    - python3 manage.py runserver

### To seed the DB, you will need an api key from [Pexels image library](https://www.pexels.com/api/)
### After getting the key, run `cp .env.example .env` in `/main` and add your api key
### To view the `/admin` page, login as the admin user: `AdminMaster:DjangoUser` 
### default poweruser  login: `jani:ASDFjkle!` (this usergroup can start / close auctions)
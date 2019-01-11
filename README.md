![](https://travis-ci.com/stoltzmaniac/foco_ds_portal.svg?branch=master)

# FoCo DS Portal

## Quick Start

Quick note: this uses Docker and Docker Compose and we will keep the Python environment at 3.6 for now.

### Getting Started

Clone the repository
```sh
$ git clone https://github.com/stoltzmaniac/foco_ds_portal.git
```

Update the environment variables in *docker-compose.yml* by:
  - Rename `.env.example` to `.env`
  - Fill in the variables (a few are prepopulated for debug mode)
  - Fill in the `TWTR` variables with your own data
  - This will be ignored via `.gitignore`

Build images and spin up containers!

```sh
$ sh initial_deploy.sh
```

Access the application at the address [http://localhost](http://localhost)

### Testing

Test without coverage:

```sh
$ docker-compose run web python manage.py test
```

Test with coverage:

```sh
$ docker-compose run web python manage.py cov
```

Lint:

```sh
$ docker-compose run web flake8 project
```


### How to Contribute  

Do you have the desire to add something to this project? If so, please follow the steps outlined below.  

  1. After cloning, create a branch and name it with your GitHub username
  2. Pop into the `project/server` directory and create a directory with your GitHub username
     * You can follow the example of `new_user_addition_example`
     * Basically copy the directory and find / replace `new_user_addition_example` with your username
     * I left a bunch of imports in there to help you understand what's going on in `projects/server/stoltzmaniac`
  3. Pop into the `project/client/template` directory and create a directory with your GitHub username
     * You can follow the example of `new_user_addition_example`
     * Basically copy the directory and find / replace `new_user_addition_example` with your username
  4. Register your the Blueprint you just made (`project/new_user_addition_example/views`)
     * This is done in  `project/server/__init__.py`
     * Add it directly underneath the other `register_blueprint` sections (same with your import)
     * Keeping with our `new_user_addition_example` you would add two lines:
       * `from project.server.new_user_addition_example.views import new_user_addition_example_blueprint`
       * `app.register_blueprint(new_user_addition_example_blueprint`
  5. Make something awesome!
     * Any requirements must go at the bottom of the `requirements.txt` file.
     * If you need environment variables, please just add a blank line with the name in `.env.example` 
     * Don't forget to add tests in the `project/server/tests` directory - call your file `test_<your_username>`
     * Use the `test_user` as an example if you're just getting started with testing
  6. Clean your code by using black `black project`
      * If you don't already have black `pip install black`
  7. Commit everything and make a pull request
  
If you are going to add a data source, try to follow what's going on in the `project/twitter` directory. 
If your data sources require environment variables please let me know how to make my own accounts for those 
services so we can allow everyone to access that data!
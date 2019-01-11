![](https://travis-ci.com/stoltzmaniac/foco_ds_portal.svg?branch=master)

# FoCo DS Portal

## Quick Start

# Docker Setup

Use this guide if you want to use Docker in your project.

> Built with Docker v18.03.1-ce.

## Getting Started

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

Access the application at the address [http://localhost:5002/](http://localhost:5002/)

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

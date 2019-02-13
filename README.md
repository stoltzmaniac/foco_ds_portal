![Build Status](https://travis-ci.com/stoltzmaniac/foco_ds_portal.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/stoltzmaniac/foco_ds_portal/badge.svg)](https://coveralls.io/github/stoltzmaniac/foco_ds_portal)
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
  - Copy the project/nginx/default.conf.example (remove .example) replace your server/domain
  - This will be ignored via `.gitignore`

Build images and spin up containers!

```sh
$ sh initial_deploy.sh
```

Access the application at the address [http://localhost:5002](http://localhost:5002)

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

### Adding SSL / TLS

The Nginx container has a [Let's Encrypt](https://letsencrypt.org/) client installed called `certbot`. If you are running on a server that a valid domain name points to, you can obtain certificates and instruct Nginx to use them for SSL / TLS. You must first execute `certbot` and provide information specific to your server / domain.

1. Before you begin, change the `server_name` parameter in your `projects/nginx/nginx.conf` file from `localhost` to your domain name (e.g. `example.com`).
2. You need to rebuild your Nginx container for the changes to take effect. Alternatively, you can manually copy the new file into the container but you will have to restart the container or enter the shell and reload Nginx.
3. Open a shell in the running Nginx container.
  - `docker-compose exec web-nginx sh`
4. Once at the Nginx containers shell prompt, run the `certbot` client.
  - `certbot --authenticator webroot --installer nginx --webroot-path /var/letsencrypt --staging`
  - You will be prompted for information and decisions. Specifically:
    - The domain name you are obtaining a certificate for. This can be provided on the command line with the `--domain` option.
    - An email address to receive information from Let's Encrypt like certificate expiration notices. This can be provided on the command line with the `--email` option.
    - You will have to agree to the terms of service. This can be skipped on the command line with `--agree-tos`.
    - Do you want to configure Nginx to redirect all insecure requests (port 80) to the secure port, 443? This can be specified on the command line with `--redirect` or `--no-redirect`.
5. The above command uses the `--staging` option which will test your configuration but not obtain valid certificates. This is useful so that you do not hit any request limits with Let's Encrypt while you are testing. 
  - At this point you should be able to connect to your site using HTTPS but the certificate will not be valid and the browser will likely complain.
6. Once you are satisfied that the request is successful, re-run the above command without `--staging`.
7. Exit the Nginx shell with `exit`.

You should now be able to establish a secure connection to your server.

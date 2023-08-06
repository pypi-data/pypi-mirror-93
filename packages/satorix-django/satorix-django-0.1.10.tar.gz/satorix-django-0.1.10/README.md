# satorix-django

By [Internet Exposure](https://www.iexposure.com/)


[Satorix](https://www.satorix.com): Get your app from local to live

The `satorix-django` package provides a streamlined mechanism for a 12-factor capable Django application to interact with the Satorix ecosystem.

## Preparing your application

Add Satorix to your Django application by including it in your `requirements.txt` with:

```text
satorix-django
```

Run `pip install satorix-django` to install it.

Next, run the generator from a terminal at the root of your application:

```console
$ satorix-django-config
```

This creates a set of files that utilize environment variables created by default with Satorix. These include the [Phusion Passenger Rails app server](https://www.phusionpassenger.com/) and the Passenger built in Nginx web server.

# Configuring your application

You can configure your application on a per-environment basis using environment variables.
The `satorix-django-config` command attempts to add the import for `satorix_django` that sets up the database connection for your application.

### Default environment Variables

The following default environment variables are used by the `satorix-django` generated files and can be managed through the Satorix Dashboard:

##### SATORIX_CANONICAL_URI_HOST

*Optional*, a domain to rewrite all requests to by default. Setting this will make it so all requests to your site will go to the supplied domain.

Common setting:

* `www.domain.dom`

##### SATORIX_CANONICAL_URI_PROTOCOL

*Optional*, the `HTTP` protocol to rewrite requests to.

Valid settings:

* `http`
* `https`

##### SATORIX_PROXY_IPS

*Optional*, used to define proxy IP addresses, for services like CloudFlare. This will allow you to get the actual client IP address accessing your site in the logs and accessible to your application.

Valid settings:

* Space separated list of IPs or network ranges (`103.21.244.0/22 103.22.200.0/22 103.31.4.0/22 104.16.0.0/12 108.162.192.0/18 131.0.72.0/22 141.101.64.0/18 162.158.0.0/15 172.64.0.0/13 173.245.48.0/20 188.114.96.0/20 190.93.240.0/20 197.234.240.0/22 198.41.128.0/17 199.27.128.0/21`)

##### SATORIX_AUTHENTICATION_HTPASSWDS

*Optional*, used to control access to your site with HTTP Basic authentication. Needs to be generated in the format created by the Apache tool `htpasswd -nb username password` or using an [online generator](http://www.htaccesstools.com/htpasswd-generator/).

Valid settings:

* Newline separated list of username and hashed password (`username:$apr1$vAxBKb8N$m0en1zabtHktHeFyT3j9y`)

##### SATORIX_AUTHENTICATION_ALLOWED_IPS

*Optional*, used to control access to your site by bypassing the above HTTP Basic authentication. If set to `all` no authentication will be required. Any IP addresses or networks added here will not need to supply the username and password to access the site.

Valid settings:

* All (`all`)
* Single IP (`192.168.1.2`)
* Network range (`192.168.1.0/24`)
* Space separated list of multiple IPs or network ranges (`192.168.1.3 192.168.2.0/24`)

## Contributing

Please coordinate contributions using the [official issue tracker](http://github.com/satorix/satorix-django/issues).

## Testing

This package is tested using [unittest](https://docs.python.org/3.5/library/unittest.html).

You can run the same tests that run during CI with:

 ```
python setup.py test
 ```
 
## CI/CD

Satorix is used to provide continuous integration and continuous deployment for this application.

CI is run against every push.

CD is used to build and publish the package for the master branch.

## License

The Satorix package is released under the terms described in the [LICENSE file](LICENSE).

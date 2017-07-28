Package format proposal
=======================

Requirements
------------

Package format should

 * precisely describe a single 'app package' - how to install, run,
   restart, and maintain working application
   * be able to describe very custom apps with very custom requirements
 * allow to generate user-friendly interface for installing apps
   * provide information about how to configure an app
   * provide information how to verify if configuration entered by user
     is valid
   * provide information about needed dependencies
   * provide default values (good enough to run an app)
 * allow to manualy configure app (with no checks and full
   responsibility on the user)

An idea
-------

Application package requires some dependencies and provides some
dependencies for other packages. Single provided or required element is
called 'a resource'.

Resource can be for example:

 * string, int, bool or other simple datatype
 * REST API available at given URL
 * access to SQL DB (a tuple: URL, username, password)
 * list of resources
 * dictionary of resources (map string -> resource)

Resources are typed. This provides additional verification if setup (set
of installed apps) is valid.

When installing an app user interface will generate a form based on
description which resources are needed. For example `string` resource
will be displayed as text field and `REST API` will be displayed as
dropdown list containing matching resources provided by other apps.
After gathering configuration data it will be injected into commandline
parameters or into configuration files of the application.

Apart from provided and required resources a package contains other
info, for example name, description, name of Docker Image, start
command, reload command.

Format
------

Package consits of:

 * parametrization file (`parameters.json`),
 * configuration file templates to be mounted inside container after
   rendering them.

Example packages are included in local directory. (for now
`parameters.json` files are not exactly json)

### Structure of `parameters.json`

`parameters.json` constains JSON object with following fields:

 * `name` - Human-readable name of the application.
 * [optional] `description` - Human-readable short description of
   application.
 * `image` - Name of Docker Image that contains application code.
 * [optional] `cmd` - Command that starts application. Ommited `cmd`
   field indicates that `CMD` command from Docker Image should be used.
 * [optional] `reload_cmd` - Command to reload running app. Ommited
   `reload_cmd` indicates that in order to reload app it should be
   restarted.
 * `files` - List of templates to be rendered and mounted inside
   container.
 * `requires` - Object that describes which resources are needed to
   start this app. Each value has stucture named
   `requirement description`. Keys are used to access created resources.
 * `provides` - Array of `provision description` objects.

#### Required resources

`requirement description` is an object that describes type of resource.
It has following fields:

 * `type` - type of resource, string, one of available types (e.g.
   `string`, `int`, `list`)
 * `description` - human-readable description of what this resource
   will be used for
 * [optional] `default` - default value for resources created. Depending
   on `type` it has different forms.
 * other fields, specific for given `type`

Types of `requirement description` objects:

 * `string`, `int`, `bool` - string, integer and boolean values
 * `list` - list of requirements, all of given type

   Additional fields in `requirement description`:

    * `of` - `requirement description` for nested resources

 * `dict` - dictionary of requirements, each of given type

   Additional fields in `requirement description`:

    * `content` - object with values of type `requirement description`
      describing nested resources

 * `http_service` - HTTP location (host, port, path)

   Additional fields in `requirement description`:

    * [optional] `api` - string that specifies requires interface. For
      HTTP endpoints that serve GUI this field should be set to some
      arbitrary value like `gui`. Ommited `api` field indictes that any
      interface is acceptable.

   This type doesn't support `default` field. (Field should be not set.)

 * `postgresql_db` - user and database in a PostgreSQL server

   `default` field contains object with keys:

    * `username`
    * `database`

#### Provided resources

`provision description` is an object with keys:

 * `type` - String, type of provided resource.
 * `description` - String, human-readable description of provided
   resource.
 * Other fields, specific for given `type`.

Types of `provision rescription` objects:

 * `http_service` - HTTP location served by the app.

   Additional fields in `provision description`:

    * `api` - String specyfying interface. Same as in
      `requirement description` of type `http_service`.
    * `port` - Int. Port number on which HTTP is served.

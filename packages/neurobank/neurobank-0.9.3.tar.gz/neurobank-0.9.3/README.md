# neurobank

**neurobank** is a simple data management system. It's designed for neural and behavioral data, but could be used for other kinds of experiments. The software helps you generate unique identifiers for your data resources, including stimuli, protocols, and recording units. No more guessing what version of a stimulus you presented in an experiment, where you stored an important recording, and whether you've backed it up or archived it.

The data management strategy behind **neurobank** is simple: every resource gets a unique identifier. What are resources? Resources include *sources*, which are used to control an experiment, and *data*, which result from running the experiment. Resources do not include things that evolve, like code, figures, or manuscripts. These should be managed in a version control system.

There are two components to the **neurobank** system. One part is the **registry**, a service that stores identifiers, ensures they're unique, and resolves identifiers to the location where the resource is stored.  [django-neurobank](https://github.com/melizalab/django-neurobank) is an implementation of this service that uses a postgres backend and the django REST framework.

The second component is an **archive**: a storage and retrieval mechanism. That's this package, which provides a basic filesystem-based archive for your resources. You can also use an external cloud-based service or a distributed filesystem like [IPFS](https://ipfs.io/), but for i/o-intensive pipelines you'll want to have your data on a local disk. This package also provides a simple python and commandline interface for querying the registry.

## Installation

Install the **neurobank** Python package and its dependencies:

```bash
pip install neurobank
```

## Archive setup

First, initialize an archive:

```bash
nbank [-a username:password] [-r registry-url] init [-n name] my-archive-path
```

`my-archive-path` must be a directory on a locallly-accessible filesystem (which could be an NFS or SSHFS mount).

`registry-url` specifies the registry to use, which can be any service that implements the API defined in [django-neurobank](https://github.com/melizalab/django-neurobank) can be used. If not supplied, the script will try to use the value of the environment variable `NBANK_REGISTRY`. The registry URL also determines the base URL for the resource identifiers. For example, if the registry is at `http://melizalab.org/neurobank/resources/` and you deposit a resource with the identifier `st32_1_2_1`, the full identifier is `http://melizalab.org/neurobank/resources/st32_1_2_1/`. `st32_1_2_1` is guaranteed to be unique within this domain.

If your registry requires authentication, this must be supplied with the `-a` flag, or in your [netrc](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html) file.

The script will attempt to contact the registry service through the supplied URL and add the archive. By default, the archive is named after the basename of the archive path. For example, `/home/data/intracellular` would have the name `intracellular`. You can can override this behavior with the `-n` flag; however, the registry may only allow you to have one archive name for each path to avoid confusion. Then the script will create and initialize the archive under `my-archive-path`. You'll get an error if the target directory already exists, or if the registry already has an archive with the same name.

### Set archive policies

Edit the `README.md` and `nbank.json` files created in the archive directory to describe your project. The `nbank.json` file is also where you'll need to set some key variables and policies. These are the settings you may want to modify:

- `auto_identifiers`: If set to false (the default), when files are deposited, their names are used as identifiers unless the user asks for an automatically generated id. If set to true, every resource is given an automatic id.

- `auto_id_type`: If set to `null` (or not set at all), automatic ids are assigned by the registry. This is usually a short, random base-36 string. If set to `"uuid"`, the `nbank` script will generate 128-bit UUIDs as identifiers.

- `require_hash`: If set to true (the default), every resource will have a hash value calculated and stored in the registry. The registry will then be able to prevent duplicate files from being deposited under multiple identifiers.

  - `keep_extensions`: If set to true (the default), files keep their extensions when deposited. Only one file with a given base identifier can be deposited, so you can't have a `st32_1_2_1.wav`, the identifier is `st32_1_2_1`, and therefore you can't also have an `st32_1_2_1.json` file. If set to false, the extension is stripped, so `st32_1_2_1.wav` would be deposited as `st32_1_2_1`. Usually you want this to be true, unless your archive only contains one kind of file.

  - `allow_directories`: If set to true, directories and their contents can be deposited as resources. The identifier is given to the directory, and the user is responsible for knowing how to interpret the contents. If set to false (the default), only regular files can be deposited.

  - `access`: Specify the `user` and `group` who will own deposited files, and the `umask` to modify access mode. If these are not set, files will be owned by the user who deposited them.

## Registering and storing resources

Before you start an experiment, register all the resources you plan to use. For example, let's say you're presenting a set of acoustic stimuli to an animal while recording neural responses. To register the stimuli:

```bash
nbank [-a user:pass] deposit [options] my-archive-path stimfile-1 stimfile-2 ...
```

Each stimulus will be given an identifier and moved to the archive. The command will output a JSON-encoded list of the resources that were deposited, including a mapping from the identifiers to the old filenames, if automatic identifiers were used.

The `deposit` command takes several options:

 - `-d, --dtype`: specify the datatype for the deposited resources. Your registry may require this.
 - `-k`: specify a metadata key-value pair. You can use this flag multiple times to set multiple fields.
 - `-H, --hash`: if set, `nbank` will calculate a SHA1 hash of each file and store it in the registry. Use this if you expect the contents of the file to be unique.
 - `-A, --auto-id`: if set, `nbank` will ask the registry to assign each file an automatically generated identifier, overriding the `auto_identifiers` policy if it is set to false.
 - `-j, --json-out`: if set, the script will output info about each deposited file as line-deliminated JSON

Now run your experiment, making sure to record the identifiers of the stimuli. The short identifier suffices in most cases, but make sure you record the registry URL somewhere, too.

After the experiment, deposit the data files into the archive using the same command. If you deposit containers or directories, you're responsible for organizing the contents and assigning any internal identifiers.

### Resource datatypes

Depending on your registry implementation, you may be required to specify a datatype for each deposited resource. This feature allows a single registry to store information about different kinds of resources. Each datatype has a name and a MIME content-type. Content-types can be from the  [official list](https://www.iana.org/assignments/media-types/media-types.xhtml), or they can be user-defined, like the content-type for [pprox](https://meliza.org/spec:2/pprox/). You can get a list of the known datatypes with

``` bash
nbank [-r registry-url] dtype list
```

You may be able to add datatypes to the registry with:

``` bash
nbank [-a user:pass] [-r registry-url] dtype add dtype-name content-type
```

## Retrieving resources

The `deposit` command moves resource files to the archive under the `resources` directory, so you can always manually locate your files based on the identifier. Resources are sorted into subdirectories using the first two characters of the identifier to avoid having too many files in one directory. For example, if the identifier is `edd0ccae-c34c-48cb-b515-a5e6f9ed91bc`, you'll find the file under `resources/ed`.

`nbank` also acts as a command-line interface to the registry. You can perform the following operations:

 - `nbank locate [options] id-1 [id-2 [id-3] ...]`: look up the location(s) of the resources associated with each identifier. You can supply full URL-based identifiers, or short ids. If short ids are used, the default registry (specified with `-r` argument or `NBANK_REGISTRY` environment variable) is used to resolve the full URL.

 - `nbank properties [options] id`: queries the registry for all the properties associated with `id`

 - `nbank info id`: returns the registry information on the resource in json format.

 - `nbank search [options] query`: searches the database for resources that match `query`. The default is to search by identifier, but you can also search by hash, dtype, archive, or any metadata fields. The default is to return only the identifiers of the resources, but you can use the `-j` flag to output json instead, which is useful if you want to distribute the metadata with the archive.

 - `nbank verify [options] files`: computes a SHA1 hash for each file and searches the registry for a match. Running this is a good idea before starting an experiment, as you'll be able to tell if any of your stimulus files have changed. It's also useful if the same identifier is used in more than one domain or if you have a data file that was inadvertently renamed.

 - `nbank modify [-k key=value] id`: update the metadata for `id`. Multiple `-k` flags can be used.

## Python interface

To be written

## Best Practices

See [docs/examples](docs/examples.md) for some additional notes on how the Meliza Lab uses neurobank.

###  Controlling access

One of the primary uses for neurobank is to allow multiple users to share a common set of data, thereby reducing the need for temporary copies and ensuring that a canonical, centralized backup of critical data can be maintained. In this case, the following practices are suggested for POSIX operating systems:

1. For each project, create a separate group and make the archive owned by the group. To give a user access to the data, add them to the group.
2. To restrict access to users not in the project group, set your umask to 027 before creating the archive.
3. Set the setgid (or setuid) bit on the subdirectories of the archive, so that files added to the archive become owned by the group. (`chmod 2770 resources metadata`). You may also consider setting the sticky bit so that files and directories can't be accidentally deleted.
4. If your filesystem supports it, set the default ACL on subdirectories so that added files are accessible only to the group. (`setfacl -d -m u::rwx,g::rwx,o::- resources metadata`).

## Unit testing

Unit tests are included, but you'll need a running registry. Set the `NBANK_REGISTRY` environment variable to the registry's URL, and if needed make an entry in `.netrc` with the required credentials.

## License

**neurobank** is licensed under the GNU Public License, version 2. That means you are free to use the code for anything you want, including a commerical work, but you have to provide the source code, including any modifications you make. You still own your data files and any associated metadata. See COPYING for more details.

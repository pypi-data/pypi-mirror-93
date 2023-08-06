#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


"""Utility functions that are useful to all sub-commands"""

import collections
import difflib
import fnmatch
import glob
import logging
import os
from enum import Enum
from enum import unique

import simplejson
import six
import termcolor

from beat.core import algorithm
from beat.core import database
from beat.core import dataformat
from beat.core import experiment
from beat.core import library
from beat.core import plotter
from beat.core import plotterparameter
from beat.core import protocoltemplate
from beat.core import toolchain

logger = logging.getLogger(__name__)

TYPE_GLOB = {
    "dataformat": os.path.join("*", "*", "*.json"),
    "database": os.path.join("*", "*.json"),
    "library": os.path.join("*", "*", "*.json"),
    "algorithm": os.path.join("*", "*", "*.json"),
    "plotter": os.path.join("*", "*", "*.json"),
    "plotterparameter": os.path.join("*", "*", "*.json"),
    "protocoltemplate": os.path.join("*", "*.json"),
    "toolchain": os.path.join("*", "*", "*.json"),
    "experiment": os.path.join("*", "*", "*", "*", "*.json"),
}


TYPE_FNMATCH = {
    "dataformat": os.path.splitext(TYPE_GLOB["dataformat"])[0],
    "database": os.path.splitext(TYPE_GLOB["database"])[0],
    "library": os.path.splitext(TYPE_GLOB["library"])[0],
    "algorithm": os.path.splitext(TYPE_GLOB["algorithm"])[0],
    "plotter": os.path.splitext(TYPE_GLOB["plotter"])[0],
    "plotterparameter": os.path.splitext(TYPE_GLOB["plotterparameter"])[0],
    "protocoltemplate": os.path.splitext(TYPE_GLOB["protocoltemplate"])[0],
    "toolchain": os.path.splitext(TYPE_GLOB["toolchain"])[0],
    "experiment": os.path.splitext(TYPE_GLOB["experiment"])[0],
}


TYPE_VALIDATOR = {
    "dataformat": dataformat.DataFormat,
    "database": database.Database,
    "library": library.Library,
    "algorithm": algorithm.Algorithm,
    "plotter": plotter.Plotter,
    "plotterparameter": plotterparameter.Plotterparameter,
    "protocoltemplate": protocoltemplate.ProtocolTemplate,
    "toolchain": toolchain.Toolchain,
    "experiment": experiment.Experiment,
}

TYPE_STORAGE = {
    "dataformat": dataformat.Storage,
    "database": database.Storage,
    "library": library.Storage,
    "algorithm": algorithm.Storage,
    "plotter": plotter.Storage,
    "plotterparameter": plotterparameter.Storage,
    "protocoltemplate": protocoltemplate.Storage,
    "toolchain": toolchain.Storage,
    "experiment": experiment.Storage,
}

TYPE_PLURAL = {
    "dataformat": "dataformats",
    "database": "databases",
    "library": "libraries",
    "algorithm": "algorithms",
    "plotter": "plotters",
    "plotterparameter": "plotters/plotterparameters",
    "defaultplotter": "plotters/defaultplotters",
    "toolchain": "toolchains",
    "experiment": "experiments",
    "protocoltemplate": "protocoltemplates",
}


@unique
class ModificationStatus(Enum):
    """This enum describes the state of possible changes between a local asset
    and it's remote counter part"""

    NO_CHANGES = ""
    REMOTE_ONLY_AVAILABLE = "r"
    LOCAL_ONLY_AVAILABLE = "l"
    DOC_CHANGED = "d"
    CONTENT_CHANGED = "+"
    BOTH_CHANGED = "*"


def recursive_rmdir_if_empty(path, stop_at):
    """Recursively removes empty directories until a certain top directory"""

    if not os.path.exists(path):
        recursive_rmdir_if_empty(os.path.dirname(path), stop_at)
        return
    if os.path.samefile(path, stop_at):
        return  # stop
    if not os.listdir(path):  # empty
        logger.info("removing empty directory `%s'...", path)
        os.rmdir(path)
        recursive_rmdir_if_empty(os.path.dirname(path), stop_at)
    return


class Selector(object):
    """Keeps track of versions and fork status"""

    def __init__(self, prefix):

        self.prefix = prefix  # the root of the directory
        self.path = os.path.join(self.prefix, ".beat", "selected.json")

        self.__version = {}
        self.__fork = {}
        self.__versionables = [
            "algorithm",
            "dataformat",
            "database",
            "library",
            "toolchain",
            "plotter",
            "plotterparameter",
            "protocoltemplate",
        ]

        self.__forkables = [
            "algorithm",
            "dataformat",
            "experiment",
            "library",
            "toolchain",
            "plotter",
            "plotterparameter",
        ]

        if os.path.exists(self.path):
            self.load()
        else:
            self.__ensure_entries()

    def __enter__(self):
        """Implements our context manager"""
        return self

    def __exit__(self, *exc):
        """Implements our context manager"""
        self.save()

    def __ensure_entries(self):
        """Ensure all types have an entry"""

        for asset_type in self.__versionables:
            if asset_type not in self.__version:
                self.__version[asset_type] = dict()

        for asset_type in self.__forkables:
            if asset_type not in self.__fork:
                self.__fork[asset_type] = dict()

    def can_fork(self, asset_type):
        """Returns whether the given asset type can be forked"""

        return asset_type in self.__forkables

    def has_versions(self, asset_type):
        """Returns whether the given asset type can have versions"""

        return asset_type in self.__versionables

    def fork(self, asset_type, src, dst):
        """Registers that object ``dst`` is a fork of object ``src``"""

        if not self.can_fork(asset_type):
            raise RuntimeError("Can't create new version of {}".format(asset_type))

        logger.info(
            "`%s/%s' is forked from `%s/%s'",
            TYPE_PLURAL[asset_type],
            dst,
            TYPE_PLURAL[asset_type],
            src,
        )
        self.__fork[asset_type][dst] = src

    def forked_from(self, asset_type, name):
        """Returns the name of the originating source object or ``None``"""
        if not self.can_fork(asset_type):
            return None

        return self.__fork[asset_type].get(name)

    def version(self, asset_type, src, dst):
        """Registers that object ``dst`` is a new version of object ``src``"""

        if asset_type not in self.__versionables:
            raise RuntimeError("Can't create new version of {}".format(asset_type))

        logger.info(
            "`%s/%s' is a new version of `%s/%s'",
            TYPE_PLURAL[asset_type],
            dst,
            TYPE_PLURAL[asset_type],
            src,
        )
        self.__version[asset_type][dst] = src

    def version_of(self, asset_type, name):
        """Returns the name of the originating version object or ``None``"""

        if asset_type not in self.__version:
            return None

        return self.__version[asset_type].get(name)

    def delete(self, asset_type, name):
        """Forgets about an object that was being tracked"""

        if asset_type in self.__fork and name in self.__fork[asset_type]:
            del self.__fork[asset_type][name]
        if asset_type in self.__version and name in self.__version[asset_type]:
            del self.__version[asset_type][name]

    def load(self):
        """Loads contents from file"""

        try:
            with open(self.path, "rt") as f:
                data = simplejson.load(f, object_pairs_hook=collections.OrderedDict)
        except simplejson.JSONDecodeError:
            logger.warning(
                "invalid state file at `%s' - removing and re-starting...", self.path
            )
            from beat.core.utils import safe_rmfile

            safe_rmfile(self.path)
            return False

        self.__fork = data["fork"]
        self.__version = data["version"]
        self.__ensure_entries()

        return True

    def save(self):
        """Saves contents to file"""

        dirname = os.path.dirname(self.path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        data = {"fork": self.__fork, "version": self.__version}
        with open(self.path, "wt") as f:
            simplejson.dump(data, f, indent=2)


def retrieve_remote_list(webapi, asset_type, fields):
    """Utility function used by commands to retrieve a remote list of objects


  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    fields (:py:class:`list`): A list of fields to retrieve from the remote
      server


  Returns:

    :py:class:`list`: A list of dictionaries containing the ``name``,
    ``short_description`` and ``hash`` of available remote objects.

  """

    logger.debug("retrieving remote %s list...", TYPE_PLURAL[asset_type])

    fields = "" if not fields else "?fields=%s" % ",".join(fields)

    url = "/api/v1/%s/%s" % (TYPE_PLURAL[asset_type], fields)

    return webapi.get(url)


def make_up_remote_list(webapi, asset_type, requirements):
    """Creates a list of downloadable objects from user requirements.

  This function can create a list of downloadable objects from user
  requirements. User requirements may point to valid object names (in which
  case these are returned unchanged) or partial object names, which are used to
  filter available remote resources. A list of fully resolved remote names
  respecting user restrictions is returned.


  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    requirements (:py:class:`list`): A list of requirements that are used to
      filter (additively) the available (remote) objects.


  Returns:

    :py:class:`list`: A list of valid object names matching user requirements
      and its order.

  """

    candidates = retrieve_remote_list(webapi, asset_type, ["name"])

    if not requirements:  # special case, return all possible values
        if candidates is None:
            return None
        return [c["name"] for c in candidates]

    # othewise, we need to separate filters from full-names
    full_requirements = fnmatch.filter(requirements, TYPE_FNMATCH[asset_type])
    short_requirements = [k for k in requirements if k not in full_requirements]

    retval = []

    if short_requirements:
        if candidates is None:
            return None
        retval = set()
        for name in short_requirements:
            retval |= set([k["name"] for k in candidates if k["name"].find(name) != -1])
        retval = list(retval)
        logger.info("search strings matched %d remote object(s)", len(retval))

    # note: if you specify a full-length requirement, we don't really care if it
    # is there or not. The final command will decide if it is an error.
    return retval + full_requirements


def display_remote_list(webapi, asset_type):
    """Implements a generic "list --remote" command

  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest, on behalf of a pre-configured user.

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    remote_list = retrieve_remote_list(
        webapi, asset_type, ["name", "short_description"]
    )
    if remote_list is None:
        return 1

    for item in remote_list:
        logger.info("%s", item["name"])
        if item["short_description"]:
            logger.extra(2 * " " + item["short_description"])

    if len(remote_list) != 1:
        logger.extra("%d %s found", len(remote_list), TYPE_PLURAL[asset_type])
    else:
        logger.extra("1 %s found" % asset_type)

    return 0


def make_up_local_list(prefix, asset_type, requirements):
    """Creates a list of uploadable objects from user requirements.

  This function can create a list of uploadable objects from user requirements.
  User requirements may point to valid object names (in which case these are
  returned unchanged) or partial object names, which are used to filter
  available local resources. A list of fully resolved local names respecting
  user restrictions is returned.


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    requirements (:py:class:`list`): A list of requirements that are used to
      filter (additively) the available (remote) objects.


  Returns:

    :py:class:`list`: A list of strings, each with the relative name of an
      object belonging to a certain category and in the order prescribed by the
      user.

  """

    root = os.path.join(prefix, TYPE_PLURAL[asset_type])
    asset_path_list = glob.glob(os.path.join(root, TYPE_GLOB[asset_type]))
    candidates = [
        os.path.splitext(os.path.relpath(path, root))[0] for path in asset_path_list
    ]

    # adds hashed path structures
    hashed_path_list = glob.glob(os.path.join(root, "*", "*", TYPE_GLOB[asset_type]))
    hashed_path_list = [
        os.path.splitext(os.path.relpath(path, root))[0] for path in hashed_path_list
    ]
    candidates += [os.path.join(*path.split(os.sep)[2:]) for path in hashed_path_list]

    if not requirements:
        return candidates

    use_requirements = []
    for k in requirements:  # remove leading plural-name
        if k.startswith(TYPE_PLURAL[asset_type] + os.sep):
            use_requirements.append(k.replace(TYPE_PLURAL[asset_type] + os.sep, ""))
        else:
            use_requirements.append(k)
    requirements = use_requirements

    full_requirements = fnmatch.filter(requirements, TYPE_FNMATCH[asset_type])
    short_requirements = [k for k in requirements if k not in full_requirements]

    retval = set()
    for name in short_requirements:
        retval |= set([k for k in candidates if k.startswith(name)])

    # note: if you specify a full-length requirement, we don't really care if it
    # is there or not. The final command will decide if it is an error.
    return list(retval) + full_requirements


def display_local_list(prefix, asset_type):
    """Implements the local "list" command


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    names = make_up_local_list(prefix, asset_type, [])

    for name in names:
        logger.info("%s", name)
        try:
            storage = TYPE_STORAGE[asset_type](prefix, name)
            contents = simplejson.loads(
                storage.json.load(), object_pairs_hook=collections.OrderedDict
            )
            if "description" in contents:
                logger.extra(2 * " " + contents["description"])
        except simplejson.JSONDecodeError:
            logger.warning(2 * " " + "(!) invalid JSON file")

    if len(names) != 1:
        logger.extra("%d %s found", len(names), TYPE_PLURAL[asset_type])
    else:
        logger.extra("1 %s found" % asset_type)

    return 0


def display_local_path(prefix, asset_type, names):
    """Implements the local "path" command


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    selected_type = None

    try:
        selected_type = TYPE_PLURAL[asset_type]
    except IndexError:
        logger.error("Selected type is not valid: %s", asset_type)
        return 1

    for name in names:
        root = os.path.join(prefix, selected_type)
        object_path = os.path.join(root, name.rsplit("/", 1)[0])
        object_files = [
            filename
            for filename in os.listdir(object_path)
            if filename.startswith(name.rsplit("/", 1)[1])
        ]
        if len(object_files) > 0:
            logger.info(
                "Available local file(s) for type '%s' and name '%s':",
                selected_type,
                name,
            )
            for filename in object_files:
                full_name = os.path.join(object_path, filename)
                logger.info(full_name)
        else:
            logger.info(
                "No local file(s) found for type '%s' and name '%s':",
                selected_type,
                name,
            )

    return 0


def edit_local_file(prefix, editor, asset_type, name):
    """Implements the local "path" command


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    selected_type = None

    try:
        selected_type = TYPE_PLURAL[asset_type]
    except IndexError:
        logger.error("Selected type is not valid: %s", asset_type)
        return 1

    python_objects = ["database", "library", "algorithm", "plotter"]
    json_objects = [
        "dataformat",
        "toolchain",
        "experiment",
        "plotterparameter",
        "protocoltemplate",
    ]

    ext = None
    if asset_type in python_objects:
        ext = ".py"
    elif asset_type in json_objects:
        ext = ".json"
    else:
        logger.error("Selected type is not valid: %s", asset_type)

    root = os.path.join(prefix, selected_type)
    object_path = os.path.join(root, name + ext)
    if os.path.isfile(object_path):
        # check if editor set
        if editor is None:
            if "VISUAL" in os.environ and len(os.environ["VISUAL"]) > 0:
                editor = os.environ["VISUAL"]
            elif "EDITOR" in os.environ and len(os.environ["EDITOR"]) > 0:
                editor = os.environ["EDITOR"]
            else:
                logger.error("No default editor set in your environment variable")
                return 1
        logger.info("Editing object of type '%s' and name '%s'", selected_type, name)
        cmd = "%s %s" % (editor, object_path)
        os.system(cmd)  # nosec
    else:
        logger.error("Not a valid file: %s", object_path)
        return 1

    return 0


def make_webapi(config):
    """Instantiates an usable web-api proxy using the command-line configuration

  Parameters:

    config (object): The command-line configuration object, from which this function
      will extract the ``platform``, ``user`` and ``token`` parameters.


  Returns

    WebAPI: A valid web-api proxy instance

  """

    from .webapi import WebAPI

    return WebAPI(config.platform, config.user, config.token)


def check_one(prefix, asset_type, name):
    """Implements object validation for a single, well-defined object


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    name (str): The name of the object, representing the unique relative path
      of the objects to check (e.g. ``user/integer/1``)

    klass (type): A python class that validates the object. It must accept the
      object

  """

    o = TYPE_VALIDATOR[asset_type](prefix, name)

    if not o.valid:
        logger.info("%s/%s [invalid]", TYPE_PLURAL[asset_type], name)
        for e in o.errors:
            logger.warning("  * %s", e)
        return 1

    else:
        logger.info("%s/%s [ok]", TYPE_PLURAL[asset_type], name)
        return 0


def check(prefix, asset_type, names):
    """Implements object validation


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to check. If the list is empty, then we
      check all available objects of a given type.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    names = make_up_local_list(prefix, asset_type, names)
    return sum([check_one(prefix, asset_type, name) for name in names])


def fetch_object(webapi, asset_type, name, fields):
    """Retrieves a single well-known object from the server

  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    name (str): A string defining the name of the object to retrieve

    fields (:py:class:`list`): A list of fields to retrieve from the remote
      server


  Returns:

    dict: A dictionary containing the object contents

  """

    fields = "?object_format=string&fields=%s" % ",".join(fields)
    if name is not None:
        url = "/api/v1/%s/%s/%s" % (TYPE_PLURAL[asset_type], name, fields)
    else:
        url = "/api/v1/%s/%s" % (TYPE_PLURAL[asset_type], fields)

    return webapi.get(url)


def pull(webapi, prefix, asset_type, names, fields, force, indentation):
    """Copies objects from the server to the local prefix


  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to retrieve or a list of usernames from
      which to retrieve objects. If the list is empty, then we pull all
      available objects of a given type. If no user is set, then pull all
      public objects of a given type.

    fields (:py:class:`list`): A list of strings, each defining one field that
      **must** be downloaded from the web-server for a given object of the
      current type and passed, unchanged to the storage ``save()`` method. For
      example, for toolchains, this value shall be ``['declaration']``. For
      algorithms, it shall be ``['declaration', 'code']``.

    force (bool): If set to ``True``, then overwrites local changes with the
      remotely retrieved copies.

    indentation (int): The indentation level, useful if this function is called
      recursively while downloading different object types. This is normally
      set to ``0`` (zero).


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

    :py:class:`list`: A list of strings containing the names of objects
      successfuly downloaded or which were already present on the current
      installation (if the user has chosen not to ``--force`` the override), in
      the order of their download.

  """

    names = make_up_remote_list(webapi, asset_type, names)
    if not names:
        return 1, []
    indent = indentation * " "
    available = set()

    status = 0

    for name in names:
        storage = TYPE_STORAGE[asset_type](prefix, name)
        if storage.exists() and not force:  # exists locally, force not set
            logger.extra(
                "%sskipping download of `%s/%s' (exists locally)",
                indent,
                TYPE_PLURAL[asset_type],
                name,
            )
            available.add(name)
            continue
        else:
            logger.info(
                "%sretrieving `%s/%s'...", indent, TYPE_PLURAL[asset_type], name
            )

            data = fetch_object(webapi, asset_type, name, fields)
            if data is None:
                status += 1  # error
                continue

            if asset_type == "plotterparameter":
                declaration = {
                    "description": data["short_description"],
                    "plotter": data["plotter"],
                    "data": data["data"],
                }
                storage.save(declaration)
            else:
                if asset_type == "algorithm" and storage.language == "cxx":
                    try:
                        file_data = webapi.download(
                            "/api/v1/%s/%s/file/"
                            % (TYPE_PLURAL[asset_type], storage.fullname,)
                        )
                        data["code"] = file_data
                    except Exception as e:
                        logger.error(e)
                        status += 1
                        continue

                storage.save(**data)

            available.add(name)

    return status, list(available)


def diff(webapi, prefix, asset_type, name, fields):
    """Shows the differences between two objects, for each of the fields


  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    name (str): A string defining the name of the object to calculate
      differences from.

    fields (:py:class:`list`): A list of strings, each defining one field that
      **must** be downloaded from the web-server for a given object of the
      current type.  For example, for toolchains, this value shall be
      ``['declaration']``. For algorithms, it shall be ``['declaration',
      'code']``.

  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    extension = {"code": ".py", "declaration": ".json", "description": ".rst"}

    def _eval_diff(remote, local, ext):
        """Calculates differences between two string buffers"""

        if not isinstance(local, six.string_types):
            if isinstance(local, dict):
                local = simplejson.dumps(local)
            else:
                local = local.decode("utf-8")
        if not isinstance(remote, six.string_types):
            if isinstance(remote, dict):
                remote = simplejson.dumps(remote)
            else:
                remote = remote.decode("utf-8")

        return difflib.unified_diff(
            remote.split("\n"),
            local.split("\n"),
            os.path.join("remote", asset_type, name + ext),
            os.path.join("local", asset_type, name + ext),
        )

    def _show_diff(diffs):
        """Displays difference display between two string buffers"""

        for line in diffs:
            if line.startswith("+"):
                termcolor.cprint(line, "green")
            elif line.startswith("-"):
                termcolor.cprint(line, "red")
            else:
                print(line)

    storage = TYPE_STORAGE[asset_type](prefix, name)
    local = storage.load()  # may also return a tuple, depending on the type
    remote = fetch_object(webapi, asset_type, name, fields)
    if remote is None:
        return 1
    if "declaration" in remote and not isinstance(
        remote["declaration"], six.string_types
    ):
        remote["declaration"] = simplejson.dumps(remote["declaration"], indent=4)

    local = dict(zip(fields, local))  # ``local`` should have the same size

    # replaces None entries with an empty string so these are comparable
    for key in local:
        local[key] = local[key] if local[key] is not None else ""

    for field in fields:
        diffs = _eval_diff(remote[field], local[field], extension.get(field, ""))
        if diffs:
            logger.info(
                "differences for `%s' of `%s/%s':", field, TYPE_PLURAL[asset_type], name
            )
            _show_diff(diffs)
        else:
            logger.info(
                "no differences for `%s' of `%s/%s'",
                field,
                TYPE_PLURAL[asset_type],
                name,
            )

    return 0


def create(prefix, asset_type, names):
    """Creates an empty object of a certain type under the given name


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    names (str): A string defining the names of the objects to create.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    status = 0

    for name in names:

        storage = TYPE_STORAGE[asset_type](prefix, name)

        if storage.exists():
            logger.error(
                "`%s/%s' already exists - will *not* overwrite",
                TYPE_PLURAL[asset_type],
                name,
            )
            status += 1

        obj = TYPE_VALIDATOR[asset_type](prefix, data=None)  # the default object
        storage = TYPE_STORAGE[asset_type](prefix, name)
        obj.write(storage)

    return status


def copy(prefix, asset_type, src, dst):
    """Creates a new object by copying another object of the same type.

  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    src (str): A string defining the name of the object to fork a new version
      from.

    dst (str): A string defining the name of the object to fork to.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    src_storage = TYPE_STORAGE[asset_type](prefix, src)
    if not src_storage.exists():
        logger.error("source `%s/%s' does not exist", TYPE_PLURAL[asset_type], src)
        return 1

    dst_storage = TYPE_STORAGE[asset_type](prefix, dst)
    if dst_storage.exists():
        logger.error("destination `%s/%s' already exists", TYPE_PLURAL[asset_type], dst)
        return 1

    dst_storage.save(*src_storage.load())

    return 0


def new_version(prefix, asset_type, src):
    """Creates a new object by copying another object of the same type.

  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    src (str): A string defining the name of the object to fork a new version
      from.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    with Selector(prefix) as selector:
        src_storage = TYPE_STORAGE[asset_type](prefix, src)
        dst = os.sep.join(src.split(os.sep)[:-1] + [""])
        dst += str(int(src_storage.version) + 1)
        dst_storage = TYPE_STORAGE[asset_type](prefix, dst)

        if dst_storage.exists():
            logger.info(
                "A representation for %s `%s' already exists - not " "overwriting",
                asset_type,
                dst,
            )
        else:
            status = copy(prefix, asset_type, src, dst)
            if status != 0:
                return status  # error

        selector.version(asset_type, src, dst)
        return 0


def fork(prefix, asset_type, src, dst):
    """Creates a new object by forking another object of the same type.


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    src (str): A string defining the name of the object to fork from.

    dst (str): A string defining the name of the object to fork to.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    with Selector(prefix) as selector:
        dst_storage = TYPE_STORAGE[asset_type](prefix, dst)

        if dst_storage.exists():
            logger.info(
                "A representation for %s `%s' already exists - not " "overwriting",
                asset_type,
                dst,
            )
        else:
            status = copy(prefix, asset_type, src, dst)
            if status != 0:
                return status  # error

        selector.fork(asset_type, src, dst)  # mark forking status
        return 0


def delete_local(prefix, asset_type, names):
    """Deletes a local object of a given type

  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to retrieve or a list of usernames from
      which to delete.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    status = 0

    for name in names:

        storage = TYPE_STORAGE[asset_type](prefix, name)
        if not storage.exists():
            logger.error("`%s/%s' does not exist", TYPE_PLURAL[asset_type], name)
            status += 1

        with Selector(prefix) as selector:
            selector.delete(asset_type, name)  # unset forking status and others

        storage.remove()

    return status


def delete_remote(webapi, asset_type, names):
    """Deletes a remote object of a given type

  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to retrieve or a list of usernames from
      which to delete.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    status = 0

    for name in names:

        logger.debug("deleting %s/%s...", TYPE_PLURAL[asset_type], name)

        url = "/api/v1/%s/%s/" % (TYPE_PLURAL[asset_type], name)
        try:
            webapi.delete(url)
        except RuntimeError as e:
            logger.error(e)
            status += 1

    return status


def status(webapi, prefix, asset_type):
    """Flags objects which have changed


  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

    :py:class:`list`: A list of objects that have local modifications and
      should be pushed remotely, eventually.

  """

    remote = retrieve_remote_list(
        webapi, asset_type, ["name", "hash", "description", "creation_date"]
    )
    if remote is None:
        return 1, []
    remote = collections.OrderedDict([(k["name"], k) for k in remote])

    local = make_up_local_list(prefix, asset_type, [])
    retval = collections.OrderedDict()

    logger.extra(
        "legend: [+] definition; [d] docs; [*] both; [l] only local; [r] only remote"
    )

    for key in remote:
        if key in local:

            storage = TYPE_STORAGE[asset_type](prefix, key)
            contents = storage.hash() != remote[key]["hash"]
            local_doc = storage.doc.load() if storage.doc.exists() else ""
            doc = local_doc != remote[key]["description"]

            if contents:
                if doc:
                    symbol = (
                        ModificationStatus.BOTH_CHANGED
                    )  # both contents and doc changed
                else:
                    symbol = ModificationStatus.CONTENT_CHANGED  # only contents changed
            else:
                if doc:
                    symbol = ModificationStatus.DOC_CHANGED  # only docs changed
                else:
                    symbol = ModificationStatus.NO_CHANGES  # no changes

            if symbol != ModificationStatus.NO_CHANGES:
                logger.info(
                    "[%s] %s/%s (@%s)",
                    symbol,
                    TYPE_PLURAL[asset_type],
                    key,
                    remote[key]["creation_date"],
                )
            else:
                logger.extra("    %s/%s", TYPE_PLURAL[asset_type], key)

            retval[key] = symbol

    # whatever is not listed remotely
    for key in set(local) - set(remote.keys()):
        logger.info("[l] %s/%s", TYPE_PLURAL[asset_type], key)
        retval[key] = ModificationStatus.LOCAL_ONLY_AVAILABLE

    # whatever is not listed locally
    for key in set(remote.keys()) - set(local):
        logger.extra(
            "[r] %s/%s (@%s)",
            TYPE_PLURAL[asset_type],
            key,
            remote[key]["creation_date"],
        )
        retval[key] = ModificationStatus.REMOTE_ONLY_AVAILABLE

    return 0, retval


def push(
    webapi, prefix, asset_type, names, fields, mappings, force, dry_run, indentation
):
    """Copies objects to the server from the local prefix


  Parameters:

    webapi (object): An instance of our WebAPI class, prepared to access the
      BEAT server of interest

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to push or a filtering criteria for local
      objects. If the list is empty, then we push all available objects of a
      given type, which have changes. If no user is set, then an error is
      raised.

    fields (:py:class:`list`): A list of strings, each defining one field that
      **must** be uploaded to the web-server for a given object of the current
      type. For example, for toolchains, this value shall be ``['declaration',
      'description']``. For algorithms, it shall be ``['declaration', 'code',
      'description']``.

    mappings (dict): A dictionary containing mappings from the stock field
      names to equivalents which are expected by our web interface. This field
      is required by experiments only.

    force (bool): If set to ``True``, then push local changes even if no change
      is detected on the local copy.

    dry_run (bool): If set to ``True``, then only prints what it would do
      instead of doing it.

    indentation (int): The indentation level, useful if this function is called
      recursively while downloading different object types. This is normally
      set to ``0`` (zero).


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

    :py:class:`list`: A list of strings containing the names of objects
      successfuly uploaded or which were already present on the remote server
      (if the user has chosen not to ``--force`` the override), in the order of
      their upload.

  """

    if webapi.is_anonymous():
        logger.error("cannot anonymously push objects, set your access token")
        return 1

    if webapi.user is None:
        logger.error("Invalid user, stopping.")
        return 1

    retval, candidates = status(webapi, prefix, asset_type)
    if retval:
        return retval

    if names:  # apply filtering conditions
        full_requirements = fnmatch.filter(names, TYPE_FNMATCH[asset_type])
        short_requirements = [k for k in names if k not in full_requirements]

        # check full-length requirements
        filtered = collections.OrderedDict()
        for k in full_requirements:
            if k not in candidates:
                logger.error(
                    "%s/%s is not available locally", TYPE_PLURAL[asset_type], k
                )
                return 1
            filtered[k] = candidates[k]

        # check short requirements
        for k in short_requirements:
            for c in candidates:
                if c.startswith(k):
                    filtered[c] = candidates[c]

        candidates = filtered

    if not force:  # filter again, if no local changes
        candidates = collections.OrderedDict(
            [
                (asset_name, modification_status)
                for asset_name, modification_status in candidates.items()
                if modification_status != ModificationStatus.NO_CHANGES
            ]
        )

    if not candidates:
        logger.warning("No new candidates for upload were found")
        return 0

    # flush all final candidates
    for asset_name, modification_status in candidates.items():
        if modification_status == ModificationStatus.REMOTE_ONLY_AVAILABLE:
            # don't push what is available unmodified remotely
            continue

        splits = asset_name.split("/")
        if splits[0] != webapi.user:
            logger.error(
                "Can't push asset {} not owned by user {}".format(
                    asset_name, webapi.user
                )
            )
            return 1

        logger.info(
            "pushing %s/%s [%s]",
            TYPE_PLURAL[asset_type],
            asset_name,
            modification_status,
        )
        storage = TYPE_STORAGE[asset_type](prefix, asset_name)
        data = storage.load()  # returns a named tuple
        message = {}
        for f in fields:
            if hasattr(data, f):
                message[f] = getattr(data, f)
            elif hasattr(storage, f):
                message[f] = getattr(storage, f)
        if "description" in message and not message["description"]:
            del message["description"]

        # apply message mappings
        for key, value in mappings.items():
            message[value] = message[key]
            del message[key]

        # fills-in fork status
        with Selector(prefix) as selector:
            fork = selector.forked_from(asset_type, asset_name)
            if fork:
                message["fork_of"] = fork
            version = selector.version_of(asset_type, asset_name)
            if version:
                message["previous_version"] = version

        if dry_run:
            continue  # don't send the data

        url = "/api/v1/%s/%s/" % (TYPE_PLURAL[asset_type], webapi.user)

        # C++ algorithms must be sent in two steps (see below)
        if asset_type == "algorithm" and storage.language == "cxx":
            message.pop("code")

        # sends the data
        if (
            modification_status == ModificationStatus.LOCAL_ONLY_AVAILABLE
        ):  # POST (new object)
            message["name"] = storage.name

            version = getattr(storage, "version")
            if version is not None:
                message["version"] = version

            if asset_type == "experiment":
                message["toolchain"] = "/".join(splits[1:-1])

            try:
                webapi.post(url, data=message)
            except RuntimeError as e:
                logger.error(e)
                return 1
            else:
                logger.info("Successfuly created `%s'", asset_name)

        else:  # PUT (update)

            url += "/".join(splits[1:]) + "/"
            if modification_status == ModificationStatus.DOC_CHANGED:
                data = {"description": message["description"]}
            else:
                data = message

            try:
                webapi.put(url, data=data)
            except RuntimeError as e:
                logger.error(e)
                return 1
            else:
                logger.info("Successfuly updated `%s'", asset_name)

        # C++ algorithms must be sent in two steps, we send the binary file now
        if asset_type == "algorithm" and storage.language == "cxx":
            try:
                with open(storage.code.path, "rb") as f:
                    webapi.upload(
                        "/api/v1/%s/%s/%s/%s/file/"
                        % (
                            TYPE_PLURAL[asset_type],
                            webapi.user,
                            storage.name,
                            storage.version,
                        ),
                        {"binary": ("%s.so" % storage.version, f)},
                    )
            except RuntimeError as e:
                logger.error(e)
                return 1
            else:
                logger.info("Successfuly uploaded binary blob `%s'", asset_name)

    return 0


def dot_diagram(prefix, asset_type, names, path, formats):
    """Dumps DOT (Graphviz) diagrams of the given toolchains/experiments


  Parameters:

    prefix (str): A string representing the root of the path in which the user
      objects are stored

    asset_type (str): One of ``database``, ``dataformat``, ``algorithm``,
      ``toolchain`` or ``experiment``.

    names (:py:class:`list`): A list of strings, each representing the unique
      relative path of the objects to push or a filtering criteria for local
      objects. If the list is empty, then we push all available objects of a
      given type, which have changes. If no user is set, then an error is
      raised.

    path (str): The directory to use for dumping the drawings. The filenames
      assigned correspond to the full object name. If not set, the default is
      to write on the current directory.

    formats (:py:class:`list`): A list of formats to dump. If not set or set to
      an empty value, then dump dot/graphviz and png formats.


  Returns:

    int: Indicating the exit status of the command, to be reported back to the
      calling process. This value should be zero if everything works OK,
      otherwise, different than zero (POSIX compliance).

  """

    if not formats:
        formats = ["dot", "png"]

    path = path or os.curdir
    if not os.path.exists(path):
        logger.info("creating directory `%s'...", path)
        os.makedirs(path)

    names = make_up_local_list(prefix, asset_type, names)

    for name in names:

        obj = TYPE_VALIDATOR[asset_type](prefix, name)

        if not hasattr(obj, "dot_diagram"):
            logger.error(
                "%s do not support DOT/Graphviz diagram output", TYPE_PLURAL[asset_type]
            )
            return 1

        if not obj.valid:
            logger.warning(
                "%s/%s is not valid - skipping it", TYPE_PLURAL[asset_type], name
            )
            continue

        try:
            diagram = obj.dot_diagram()
        except Exception as e:
            logger.warning(
                "%s/%s cannot be drawn: %s - skipping it",
                TYPE_PLURAL[asset_type],
                name,
                e,
            )
            continue

        destfile = os.path.join(path, "%s" % TYPE_PLURAL[asset_type], obj.name)

        for k in formats:
            if k == "dot":
                logger.info(
                    "%s/%s -> %s.%s", TYPE_PLURAL[asset_type], name, destfile, k
                )
                diagram.save(destfile + ".dot")
            else:
                logger.info(
                    "%s/%s -> %s.%s", TYPE_PLURAL[asset_type], name, destfile, k
                )
                diagram.format = k
                diagram.render(destfile, cleanup=True)

    return 0


def stringify(value):
    """Creates a string representation of a baseformat represented as a dict

  To avoid overloading the terminal that will print the result of this
  function, only the first ten elements of lists are processed with visual cues
  that will show that there's more to it.

  The input variable ``value`` is modified in-place.

  Parameters:

    value (dict): A dictionary representing the baseformat object, obtained as
      with :py:meth:`beat.backend.python.baseformat.baseformat.as_dict`, that
      represents the object one seeks to represent in string format.


  Returns

    dict: Modifies the input variable ``value`` in-place, but also returns it.

  """

    if isinstance(value, list):
        if len(value) > 10:
            if isinstance(value[0], dict) or isinstance(value[0], list):
                return (
                    map(stringify, value[0:4])
                    + ["..."]
                    + map(stringify, value[-4:])
                    + ["BEAT_LIST_SIZE(%d elements)BEAT_LIST_SIZE" % len(value)]
                )

            reduced = "BEAT_LIST_DELIMITER["
            for v in value[0:4]:
                reduced += str(v) + ", "
            reduced += "..."
            for v in value[-4:]:
                reduced += ", " + str(v)
            reduced += " (%d elements)]BEAT_LIST_DELIMITER" % len(value)
            return reduced
        elif (len(value) > 0) and (
            isinstance(value[0], list) or isinstance(value[0], dict)
        ):
            return list(map(stringify, value))

    elif isinstance(value, dict):
        for name, value2 in value.items():
            value[name] = stringify(value2)

    return value

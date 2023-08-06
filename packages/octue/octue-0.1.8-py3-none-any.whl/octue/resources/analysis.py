import json
import logging

from octue.definitions import OUTPUT_STRANDS
from octue.mixins import Hashable, Identifiable, Loggable, Serialisable, Taggable
from octue.resources.manifest import Manifest
from octue.utils.encoders import OctueJSONEncoder
from octue.utils.folders import get_file_name_from_strand
from twined import ALL_STRANDS, Twine


module_logger = logging.getLogger(__name__)


_HASH_FUNCTIONS = {
    "configuration_values": Hashable.hash_non_class_object,
    "configuration_manifest": lambda manifest: manifest.hash_value,
    "input_values": Hashable.hash_non_class_object,
    "input_manifest": lambda manifest: manifest.hash_value,
}

# Map strand names to class which we expect Twined to instantiate for us
CLASS_MAP = {"configuration_manifest": Manifest, "input_manifest": Manifest, "output_manifest": Manifest}


class Analysis(Identifiable, Loggable, Serialisable, Taggable):
    """ Analysis class, holding references to all input and output data

    ## The Analysis Instance

    An Analysis instance is unique to a specific computation analysis task, however large or small, run at a specific
    time. It will be created by the task runner (which will have validated incoming data already - Analysis() doesn't
    do any validation).

    It holds references to all config, input and output data, logs, connections to child twins, credentials, etc, so
    should be referred to from your code to get those items.

    It's basically the "Internal API" for your data service - a single point of contact where you can get or update
    anything you need.

    Analyses are instantiated at the top level of your app/service/twin code and you can import the instantiated
    object from there (see the templates for examples)

    :parameter twine: Twine instance or json source
    :parameter configuration_values: see Runner.run() for definition
    :parameter configuration_manifest: see Runner.run() for definition
    :parameter input_values: see Runner.run() for definition
    :parameter input_manifest: see Runner.run() for definition
    :parameter credentials: see Runner.run() for definition
    :parameter monitors: see Runner.run() for definition
    :parameter output_values: see Runner.run() for definition
    :parameter output_manifest: see Runner.run() for definition
    :parameter id: Optional UUID for the analysis
    :parameter logger: Optional logging.Logger instance attached to the analysis
    """

    def __init__(self, twine, skip_checks=False, **kwargs):
        """ Constructor of Analysis instance
        """

        # Instantiate the twine (if not already) and attach it to self
        if not isinstance(twine, Twine):
            twine = Twine(source=twine)

        self.twine = twine
        self._skip_checks = skip_checks

        # Pop any possible strand data sources before init superclasses (and tie them to protected attributes)
        strand_kwargs = [(name, kwargs.pop(name, None)) for name in ALL_STRANDS]
        for strand_name, strand_data in strand_kwargs:
            setattr(self, f"{strand_name}", strand_data)

        for strand_name, strand_data in strand_kwargs:
            if strand_name in _HASH_FUNCTIONS:
                strand_hash_name = f"{strand_name}_hash"

                if strand_data is not None:
                    setattr(self, strand_hash_name, _HASH_FUNCTIONS[strand_name](strand_data))
                else:
                    setattr(self, strand_hash_name, None)

        # Init superclasses
        super().__init__(**kwargs)

    def finalise(self, output_dir=None):
        """ Validates and serialises output_values and output_manifest, optionally writing them to files

        If output_dir is given, then the serialised outputs are also written to files in the output directory

        :parameter output_dir: path-like pointing to directory where the outputs should be saved to file (if None, files
         are not written)
        :type output_dir:  path-like

        :return: dictionary of serialised strings for values and manifest data.
        :rtype: dict
        """

        # Using twined's validate_strand method gives us sugar to check for both extra outputs
        # (e.g. output_values where there shouldn't be any) and missing outputs (e.g. output_values is None when it
        # should be a dict of data)
        serialised = dict()
        for k in OUTPUT_STRANDS:
            self.logger.debug(f"Serialising {k}")
            att = getattr(self, k)
            if att is not None:
                att = json.dumps(att, cls=OctueJSONEncoder)

            serialised[k] = att

        self.logger.debug("Validating serialised output json against twine")
        self.twine.validate(**serialised)

        # Optionally write the serialised strand to disk
        for k in OUTPUT_STRANDS:
            if output_dir and serialised[k] is not None:
                file_name = get_file_name_from_strand(k, output_dir)
                self.logger.debug(f"Writing {k} to file {file_name}")
                with open(file_name, "w") as fp:
                    fp.write(serialised[k])

        return serialised

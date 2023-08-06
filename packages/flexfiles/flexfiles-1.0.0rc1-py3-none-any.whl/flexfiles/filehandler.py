from flexlog import cleanlogger
import csv
import os
import json
import hashlib

def __get_hash_and_dump(data):
    dump = json.dumps(data)
    checksum = hashlib.md5(dump.encode())
    return checksum.hexdigest(), dump

def get_hash(data):
    checksum, _ = __get_hash_and_dump(data)
    return checksum

DELIMITER = ","

class AssetsIO:
    """
    Provides functionality to read and write CSV and JSON files. It also maintains checksums and caches, such that you do not reload the files all the time.
    """

    def __init__(self, logger = cleanlogger.CleanLogger("AssetsIO")):
        self._log = logger
        self._checksums = {}
        self._cache = {}

    def read_csv(self, directory, filename, line_translator=lambda line: line, force=False, delimiter=DELIMITER):
        """
        Reads the given CSV file from the given directory. If there are any reading or access problems, errors are logged and nothing is returned.
        It also tries to give you cached data if the file has been loaded before.
        It returns a tuple containing the data and the header of the CSV file.
        
        `data, header = read_csv(...)`
        """
        checksum = self.__read_checksum(directory, filename)

        if not force \
            and (directory, filename) in self._checksums.keys() \
            and self._checksums[directory, filename] == checksum:
            if not (directory, filename) in self._cache.keys():
                self._log.warning("Tried to load cached data for ({d}, {f}) but there is nothing. I will load a fresh version now.".format(d=directory, f=filename))
            else:
                self._log.debug("Loading cached data for ({d}, {f}) ...".format(d=directory, f=filename))
                return self._cache[directory, filename]

        self._log.debug("Loading data from CSV for ({d}, {f}) ...".format(d=directory, f=filename))
        csv_file = os.path.join(directory, filename)
        if not os.path.exists(csv_file):
            self._log.error("File '{f}' not found.".format(f=csv_file))
            return [], []
        
        header = []
        data = []
        with open(csv_file, newline='', mode='r') as f:
            reader = csv.reader(f, delimiter=delimiter)
            skipfirst = True
            for line in reader:
                if skipfirst:
                    skipfirst = False
                    header = line
                    continue
                data += [ line_translator(line) ]

        self._checksums[directory, filename] = checksum
        self._cache[directory, filename] = header, data
        return header, data

    def write_csv(self, directory=".", filename="result.csv", header=["property", "value"], data=[], line_creator=lambda entry: entry, delimiter = DELIMITER):
        """
        Writes data to a CSV file of the given name to the given directory. The header must contain the column names, the data must contain one entry per data set.
        Use the line creator to define a mapping from data sets to CSV rows, if necessary. If a data set is a list of appropriate length, the default line creator is sufficient.
        If the directory does not exist, it tries to create it. 

        If something goes wrong, errors are logged and False is the result. Returns true if everything is fine.
        """
        success = True
        if not self.__check_directory(directory):
            return False

        csv_file = os.path.join(directory, filename)
        self._log.debug("Writing to file {f} ...".format(f=csv_file))

        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(header)
            for entry in data:
                try:
                    writer.writerow(line_creator(entry))
                except:
                    self._log.error("There was an error writing the following entry: {e}. I will try to continue anyway.".format(e=entry))
                    success = False
        
        checksum_file = os.path.join(directory, "{f}.md5".format(f=filename))
        self._log.debug("Writing checksum to file {f} ...".format(f=checksum_file))
        with open(checksum_file, mode='w') as f:
            checksum = changes.get_hash(data)
            f.write(checksum)

        self._cache[directory, filename] = header, data
        self._checksums[directory, filename] = checksum

        self._log.info("Finished writing to {f}.".format(f=csv_file))
        return success

    def load_json(self, directory, filename, force = False):
        """
        Loads the JSON file from the given directory. Delivers a cached version unless overridden using force.

        If anything goes wrong, errors are logged and an empty list is returned.
        """
        checksum = self.__read_checksum(directory, filename)

        if not force \
            and (directory, filename) in self._checksums.keys() \
            and self._checksums[directory, filename] == checksum:
            if not (directory, filename) in self._cache.keys():
                self._log.warning("Tried to load cached data for ({d}, {f}) but there is nothing. I will load a fresh version now.".format(d=directory, f=filename))
            else:
                self._log.debug("Loading cached data for ({d}, {f}) ...".format(d=directory, f=filename))
                return self._cache[directory, filename]

        if not self.__check_directory(directory):
            log.warning("Cannot access directory {d}, using current directory instead.".format(d=directory))
            directory = "."

        json_file = os.path.join(directory, filename)
        if not os.path.exists(json_file):
            self._log.info("File {f} does not exist, so I return empty data, which should be expected.".format(f=json_file))
            return []

        self._log.debug("Reading from file {f} ...".format(f=json_file))
        with open(json_file, mode='r') as f:
            try:
                data = json.load(f)
                self._cache[directory, filename] = data
                self._checksums[directory, filename] = checksum

                return data
            except:
                self._log.error("Reading from file {f} caused an error. Something is fishy here. I return empty data.".format(f=json_file))

        return []

    def write_json(self, directory, filename, data):
        """
        Writes the given data as JSON to the given filename in the given directory.
        Tries to create the directory if needed.

        If anything goes wrong, errors are logged and False is returned.
        """
        success = True
        if not self.__check_directory(directory):
            return False

        json_file = os.path.join(directory, filename)

        self._log.debug("Writing to file {f} ...".format(f=json_file))
        with open(json_file, mode='w') as f:
            try:
                json.dump(data, f)
            except:
                self._log.error("Writing to file {f} caused an error. Something is fishy here.".format(f=json_file))
                success = False

        checksum_file = os.path.join(directory, "{f}.md5".format(f=filename))
        self._log.debug("Writing checksum to file {f} ...".format(f=checksum_file))
        with open(checksum_file, mode='w') as f:
            checksum = changes.get_hash(data)
            f.write(checksum)

        self._cache[directory, filename] = data
        self._checksums[directory, filename] = checksum
        return success

    def get_checksum(self, directory, filename):
        """
        Gets the checksum for this file, either from cache or from the corresponding checksum file.
        """
        if (directory, filename) in self._checksums.keys():
            return self._checksums[directory, filename]

        return self.__read_checksum(directory, filename)

    def has_data(self, directory, filename):
        """
        Indicates whether there is data around corresponding to folder and file, either cached or as a file.
        """
        if (directory, filename) in self._cache.keys():
            return True

        return os.path.exists(
            os.path.join(
                directory,
                filename
            )
        )

    def __check_directory(self, dir):
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except:
                self._log.error("Cannot create directory {d}.".format(d=dir))
                return False

        return True

    def __read_checksum(self, directory, filename):
        checksum_file = os.path.join(directory, "{f}.md5".format(f=filename))
        checksum = ""
        if not os.path.exists(checksum_file):
            self._log.warning("Checksum file '{f}' not found.".format(f=checksum_file))

        else:
            with open(checksum_file, mode='r') as f:
                checksum = f.readline()

        return checksum


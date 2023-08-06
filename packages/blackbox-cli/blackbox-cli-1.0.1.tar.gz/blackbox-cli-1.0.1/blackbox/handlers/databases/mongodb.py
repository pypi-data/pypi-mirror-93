import datetime
from pathlib import Path

from blackbox.handlers.databases._base import BlackboxDatabase
from blackbox.utils import run_command
from blackbox.utils.logger import log


class MongoDB(BlackboxDatabase):
    """
    A Database handler that will do a mongodump for MongoDB, backing up all documents.

    This will use mongodump with --gzip and --archive, and must be restored using the same
    arguments, e.g. mongorestore --gzip --archive=/path/to/file.archive.
    """

    connstring_regex = r"mongodb://(?P<user>.+):(?P<password>.+)@(?P<host>.+):(?P<port>.+)"
    valid_prefixes = [
        "mongodb"
    ]

    def backup(self) -> Path:
        """Dump all the data to a file and then return the filepath."""
        date = datetime.date.today().strftime("%d_%m_%Y")
        archive_file = Path.home() / f"mongodb_blackbox_{date}.archive"

        # Run the backup, and store the outcome in this object.
        self.success, self.output = run_command(
            f"mongodump "
            f"--uri={self.connstring} "
            "--gzip "
            "--forceTableScan "
            f"--archive={archive_file}"
        )
        log.debug(self.output)

        # Return the path to the backup file
        return archive_file

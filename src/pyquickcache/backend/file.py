import os
import sys
from datetime import datetime
from typing import Optional, Union


class FileManager:
    """
    Utility class for resolving file paths and performing safe disk I/O.

    This class centralizes all filesystem-related logic used by the cache
    and metrics subsystems, including:
    - Resolving user-provided paths against project defaults
    - Creating directories as needed
    - Enforcing file extensions
    - Reading and writing text or binary data

    This class is intended for internal use only and is not designed
    for user extension or subclassing.
    """

    def __init__(self, default_dir: str, default_filename: str):
        """
        Initialize a FileManager with default storage settings.

        Args:
            default_dir (str): Default directory (relative to project root)
                where files should be stored.
            default_filename (str): Default base filename (without extension)
                to use when the user does not provide one.

        Example:
            FileManager("cache_storage", "quickcache_data")
        """
        self.default_dir = default_dir
        self.default_filename = default_filename

    def _get_project_root(self) -> str:
        """
        Determine the root directory of the running project.

        This method attempts to locate the directory of the script
        that started the Python process (i.e., `__main__`).
        If that fails, it falls back to the current working directory.

        Returns:
            str: Absolute path to the inferred project root directory.
        """
        try:
            main_module = sys.modules.get("__main__")
            if main_module and hasattr(main_module, "__file__"):
                return os.path.dirname(os.path.abspath(main_module.__file__))
        except Exception:
            pass
        return os.getcwd()

    def resolve_path(
        self, user_input: Optional[str], extension: str, use_timestamp: bool = False
    ) -> str:
        """
        Resolve the final file path based on user input and defaults.

        This method determines the correct directory and filename by
        applying the following rules:
        - If no user input is provided, defaults are used
        - If a directory path is provided, the default filename is used
        - If a filename or full path is provided, it is respected
        - The specified extension is always enforced
        - A timestamp may optionally be appended to the filename
        - Target directories are created automatically if missing

        Args:
            user_input (Optional[str]): User-provided file path, directory,
                filename, or None.
            extension (str): File extension to enforce (without dot).
            use_timestamp (bool): Whether to append a timestamp to the filename.

        Returns:
            str: Fully resolved absolute file path.
        """
        project_root = self._get_project_root()
        storage_dir = os.path.join(project_root, self.default_dir)

        # 1. Handle Filename and Directory
        if not user_input:
            # Case: Nothing given -> Use the instance defaults
            base_name = self.default_filename
            target_dir = storage_dir

        elif os.path.isdir(user_input):
            # Case: Only a directory path was given
            base_name = self.default_filename
            target_dir = user_input

        else:
            # Case: Specific filename or Path+Filename given
            target_dir = os.path.dirname(user_input) or storage_dir
            base_name = os.path.basename(user_input)
            base_name = os.path.splitext(base_name)[0]

        # 2. Add Timestamp if requested
        if use_timestamp:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"{base_name}_{ts}_srr"  # Added the suffix for consistency

        # 3. Force the correct extension
        final_filename = f"{base_name}.{extension}"

        # 4. Ensure the directory exists
        os.makedirs(target_dir, exist_ok=True)

        return os.path.join(target_dir, final_filename)

    def write(self, path: str, data: Union[str, bytes], append: bool = False):
        """
        Write data to disk at the specified path.

        The write mode (text or binary) is automatically inferred
        from the data type.

        Args:
            path (str): Full path to the target file.
            data (Union[str, bytes]): Data to write.
            append (bool): If True, append to the file instead of overwriting.

        Raises:
            OSError: If the file cannot be written.
        """
        base_mode = "a" if append else "w"

        # Determine if binary flag 'b' is needed based on data type
        mode = base_mode if isinstance(data, str) else f"{base_mode}b"

        with open(path, mode) as f:
            f.write(data)

    def read(self, path: str, binary: bool = False) -> Union[str, bytes]:
        """
        Read data from disk.

        Args:
            path (str): Full path to the file.
            binary (bool): Whether to read the file in binary mode.

        Returns:
            Union[str, bytes]: File contents.

        Raises:
            FileNotFoundError: If the file does not exist.
            OSError: If the file cannot be read.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"No such file: {path}")

        mode = "rb" if binary else "r"

        with open(path, mode) as f:
            return f.read()

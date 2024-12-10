import os
import sys
import logging
from typing import List
import importlib.metadata
import re
logger = logging.getLogger("WFM.Setup")


class SetupChecker:
    def __init__(self, requirements_file: str = "requirements.txt", spacy_model: str = "en_core_web_sm"):
        self.requirements_file = requirements_file
        self.spacy_model = spacy_model

    def is_virtual_environment(self) -> bool:
        """Check if the code is running in a virtual environment."""
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        logger.debug(f"Virtual environment status: {'Yes' if in_venv else 'No'}")
        return in_venv

    def read_requirements(self) -> List[str]:
        """Read requirements from the requirements file."""
        if not os.path.exists(self.requirements_file):
            logger.error(f"Requirements file '{self.requirements_file}' not found.")
            raise FileNotFoundError(f"Requirements file '{self.requirements_file}' not found.")

        with open(self.requirements_file, 'r') as file:
            requirements = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            logger.debug(f"Read {len(requirements)} requirements from '{self.requirements_file}'.")
            return requirements

    def check_and_install_requirements(self):
        """Check if requirements are installed, and log missing ones."""
        requirements = self.read_requirements()

        # Get a list of installed packages using importlib.metadata
        installed_packages = {dist.metadata["Name"].lower() for dist in importlib.metadata.distributions()}

        package_version_regex = re.compile(r"([a-zA-Z0-9_\-]+)([=<>!~]*.+)?")

        missing_packages = []
        for req in requirements:
            match = package_version_regex.match(req)
            if match:
                package_name = match.group(1).lower()
                if package_name not in installed_packages:
                    missing_packages.append(req)

        if missing_packages:
            logger.warning("The following packages are missing:")
            for package in missing_packages:

                logger.warning(f"  - {package}")
            logger.info("You can install missing packages using: pip install -r requirements.txt")
        else:
            logger.info("All required packages are installed.")

    def check_and_install_spacy_model(self):
        """Check if the specified spaCy model is installed and log installation commands if missing."""
        try:
            import spacy
        except ImportError:
            logger.error("spaCy is not installed. Please ensure it is listed in your requirements file.")
            return

        try:
            spacy.load(self.spacy_model)
            logger.info(f"The spaCy model '{self.spacy_model}' is installed.")
        except OSError:
            logger.warning(f"The spaCy model '{self.spacy_model}' is not installed.")
            logger.info(f"Install it using: python -m spacy download {self.spacy_model}")

    def run_checks(self):
        """Run all setup checks."""
        logger.info("Starting setup checks...\n")

        # Check virtual environment
        if not self.is_virtual_environment():
            logger.warning("You are not running in a virtual environment. It is recommended to use one.")
        else:
            logger.info("Virtual environment detected.")

        # Check requirements
        logger.info("Checking requirements...")
        self.check_and_install_requirements()

        # Check spaCy model
        logger.info("Checking spaCy model...")
        self.check_and_install_spacy_model()


# Example usage
if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    setup_checker = SetupChecker(requirements_file="../../requirements.txt", spacy_model="en_core_web_sm")
    setup_checker.run_checks()

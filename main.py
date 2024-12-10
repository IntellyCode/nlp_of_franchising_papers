from src.controller import Controller, SetupChecker
from src.config import Config
import logging

logger = logging.getLogger("WFM.Main")

logger.setLevel(logging.DEBUG)
setup_checker = SetupChecker(requirements_file="requirements.txt", spacy_model="en_core_web_sm")
setup_checker.run_checks()
c = Controller(Config())


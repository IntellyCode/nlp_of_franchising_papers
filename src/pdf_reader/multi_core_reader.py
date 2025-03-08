from src.pdf_reader import PdfReader, MultiReader
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import logging
import logging.handlers
import os

logger = logging.getLogger("WFM.MultiCoreReader")
logging.basicConfig(level=logging.INFO)


def _read_pdf(config, pdf_path: str, index: int):
    """
    Helper function to read a single PDF and return a tuple (index, text).
    """
    pdf_reader = PdfReader(config)
    pdf_reader.set_path(pdf_path)
    try:
        pdf_reader.open()
        text = pdf_reader.read()
        pdf_reader.close()
    except Exception as e:
        text = ""
    return index, text


def worker_process(directory, config, tasks_group):
    """
    Helper function to create a Worker and process a group of PDF tasks.

    Args:
        directory (str): The base directory containing the PDF files.
        config: The configuration object for PdfReader.
        tasks_group (List[Tuple[int, str]]): A list of tasks where each task is (index, relative_pdf_filename).
        log_queue: A queue to capture all logging messages from different cores

    Returns:
        dict: A dictionary mapping each PDF's index to its read text.
    """
    worker = Worker(directory, config, tasks_group)
    return worker.process()


class Worker:
    """
    Worker class to process a batch of PDF tasks concurrently using threads.

    Attributes:
        directory (str): The base directory containing the PDF files.
        config: The configuration object used for PdfReader.
        tasks (list of tuples): Each tuple is (index, pdf_file), where pdf_file is the relative file name.
    """

    def __init__(self, directory: str, config, tasks):
        """
        Initialize the Worker with a directory, configuration, and list of tasks.

        Args:
            directory (str): The base directory containing the PDF files.
            config: Configuration object for PdfReader.
            tasks (list of tuples): List of tuples (index, pdf_file) representing the PDF tasks.
        """
        self.directory = directory
        self.config = config
        self.tasks = tasks

    def process(self):
        """
        Process the assigned PDF tasks concurrently using a ThreadPoolExecutor.

        Returns:
            A dictionary mapping each PDF's index to its read text.
        """
        results = {}
        with ThreadPoolExecutor() as executor:
            futures = []
            for index, pdf_file in self.tasks:
                pdf_path = os.path.join(self.directory, pdf_file)
                futures.append(executor.submit(_read_pdf, self.config, pdf_path, index))
            for future in as_completed(futures):
                idx, text = future.result()
                results[idx] = text
        return results


class MultiCoreReader(MultiReader):
    def _get_pdf_files(self, directory: str):
        """
        Get a sorted list of PDF files from the specified directory and assign each an index.

        Returns:
            List[Tuple[int, str]]: A list of tuples where each tuple is (index, pdf_file).
        """
        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
        pdf_files.sort()
        logger.info("Got Pdf Files")
        return list(enumerate(pdf_files))

    def _read_pdf(self, pdf_path: str, index: int):
        pass

    def read_all(self):
        """
        Read all PDFs concurrently using both multiprocessing and multithreading.

        This method splits self.pdf_files (which contains the relative paths of the PDFs)
        into groups—one group per available core. Each group is processed by a separate worker
        (in its own process) that uses a ThreadPoolExecutor for concurrent PDF reading.
        The results are then aggregated into self.texts in the correct order.

        Returns:
            List[Optional[str]]: A list of PDF texts in the same alphabetical order as self.pdf_files.
        """
        logger.info("Reading Pdfs MultiCore")
        num_cores = os.cpu_count() or 1
        logger.debug("Number of CPUs: {}".format(num_cores))
        total_tasks = len(self.pdf_files)
        logger.debug(f"Total tasks: {total_tasks}")
        chunk_size = (total_tasks + num_cores - 1) // num_cores
        logger.debug("Chunk size: {}".format(chunk_size))
        groups = []
        total_length = 0
        for i in range(num_cores):
            if (i + 1) * chunk_size <= total_tasks:
                groups.append(self.pdf_files[i * chunk_size: (i + 1) * chunk_size])
            else:
                groups.append(self.pdf_files[i * chunk_size:])
            total_length += len(groups[-1])
        if total_length != total_tasks:
            raise AttributeError("Not all Pdfs were assigned to a Worker instance")

        logger.info(f"Groups: {groups}")
        logger.info(f"All Pdfs were assigned a worker instance: {total_length}")

        results = {}
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            futures = [executor.submit(worker_process, self.directory, self.config, group)
                       for group in groups]
            for future in as_completed(futures):
                group_results = future.result()
                results.update(group_results)
        logger.info("Finished MultiCore Pdf Reading")
        self.texts = [results[i] for i in sorted(results.keys())]
        return self.texts

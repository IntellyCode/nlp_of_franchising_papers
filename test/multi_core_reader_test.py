import os
import tempfile
import unittest
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import logging
import multiprocessing

from src.pdf_reader import MultiCoreReader

# Global logger (using the same logger as your production code)
logger = logging.getLogger("WFM.MultiCoreReader")
logging.basicConfig(level=logging.INFO)

# This is the worker function used by the Worker class.
# We override its behavior for testing so that it does math instead of PDF reading.
def _do_math(config, file_path: str, index: int):
    """
    Instead of reading a PDF, this function extracts a number from the filename,
    squares it, and returns (index, result).
    """
    base = os.path.basename(file_path)
    number_str, _ = os.path.splitext(base)
    number = int(number_str)
    return index, number * number

# The Worker class remains the same except that for testing we patch _read_pdf.
class Worker:
    """
    Worker class that processes a batch of tasks concurrently using threads.
    In production, it calls _read_pdf to read PDFs.
    For our test, we will patch _read_pdf to perform a math operation.
    """
    def __init__(self, directory: str, config, tasks):
        self.directory = directory
        self.config = config
        self.tasks = tasks

    def process(self):
        results = {}
        with ThreadPoolExecutor() as executor:
            futures = []
            for index, file_name in self.tasks:
                file_path = os.path.join(self.directory, file_name)
                # Instead of _read_pdf we call our math function.
                futures.append(executor.submit(_do_math, self.config, file_path, index))
            for future in as_completed(futures):
                idx, result = future.result()
                results[idx] = result
        return results

# The helper function to run a worker in a separate process.
def worker_process(directory, config, tasks_group):
    worker = Worker(directory, config, tasks_group)
    return worker.process()

# Now we subclass your MultiCoreReader for testing.
class TestMathReader(MultiCoreReader):
    def __init__(self, directory: str, config=None):
        super().__init__(directory, config)

    def _get_pdf_files(self, directory: str):
        """
        For testing, list all files ending with .pdf (our dummy math files) and sort them.
        """
        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
        pdf_files.sort()
        logger.info("Got Pdf Files: %s", pdf_files)
        return list(enumerate(pdf_files))

    def _read_pdf(self, pdf_path: str, index: int):
        pass

    def read_all(self):
        """
        Mimics the production read_all method but uses our worker_process to perform math.
        """
        logger.info("Reading files using MultiCore Math")
        num_cores = os.cpu_count() or 1
        logger.info(f"Using {num_cores} cores")
        total_tasks = len(self.pdf_files)
        chunk_size = (total_tasks + num_cores - 1) // num_cores
        logger.info("Chunk size: %s", chunk_size)
        groups = []
        total_length = 0
        for i in range(num_cores):
            if (i + 1) * chunk_size <= total_tasks:
                groups.append(self.pdf_files[i * chunk_size: (i + 1) * chunk_size])
            else:
                groups.append(self.pdf_files[i * chunk_size:])
            total_length += len(groups[-1])
        if total_length != total_tasks:
            raise AttributeError("Not all tasks were assigned to a Worker instance")

        logger.info("Task groups: %s", groups)
        results = {}
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            futures = [executor.submit(worker_process, self.directory, self.config, group)
                       for group in groups if group]  # only submit non-empty groups
            for future in as_completed(futures):
                group_results = future.result()
                results.update(group_results)
        logger.info("Finished MultiCore Math Processing")
        # Assemble the results in order of their index
        self.texts = [results[i] for i in sorted(results.keys())]
        return self.texts

# Unit test for our TestMathReader
class TestMultiCoreMath(unittest.TestCase):
    def test_math_operations(self):
        # Define the dummy file names representing our calculations.
        # These files names are numbers: 5,6,11,12,13,14,15,16,17,18.
        file_names = [f"{i}.pdf" for i in range(1, 57)]
        # Create a temporary directory and add the dummy files.
        with tempfile.TemporaryDirectory() as tmpdirname:
            for name in file_names:
                open(os.path.join(tmpdirname, name), 'a').close()

            # Instantiate our TestMathReader with the temporary directory.
            reader = TestMathReader(tmpdirname)
            results = reader.read_all()  # This will run our math calculations in a multicore setup.

            # Determine the expected order.
            # Note: _get_pdf_files sorts the filenames lexicographically.
            sorted_files = sorted(file_names)
            expected_results = []
            for f in sorted_files:
                number = int(os.path.splitext(f)[0])
                expected_results.append(number * number)

            # For debugging, print both expected and actual results.
            print("Expected results:", expected_results)
            print("Actual results:  ", results)

            self.assertEqual(results, expected_results)

if __name__ == '__main__':
    # Running the test. In production you might use a test runner instead.
    multiprocessing.freeze_support()  # For Windows support with multiprocessing
    unittest.main()

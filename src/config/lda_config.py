from src.config import Config
from typing import Optional


class LdaConfig(Config):
    def set_config(self,
                   no_below: int = 2,
                   no_above: float = 0.6,
                   num_topics: int = 20,
                   chunk_size: int = 30,
                   passes: int = 20,
                   iterations: int = 400,
                   eval_every: Optional[str | int] = None,
                   alpha: [float, int] = "auto",
                   eta: [float, int] = "auto",):
        """
        :param no_below: If word occurs less than no_below times, the word is remove from the corpus
        :param no_above: If word occurs more than no_above times, the word is remove from the corpus
        :param num_topics: Number of topics to detect in corpus
        :param chunk_size: Number of documents to read at a time (limited only by the memory)
        :param passes: Number of passes to use for LDA
        :param iterations: Number of iterations to use for LDA
        :param eval_every: Should the model be evaluated at each step
        :param alpha: Alpha parameter for LDA
        :param eta: Eta parameter for LDA
        :return:
        """

        def _to_int_or_none(value: str) -> Optional[int]:
            try:
                return int(value)
            except Exception:
                return None
        self._config = {
            "no_below": int(no_below),
            "no_above": float(no_above),
            "num_topics": int(num_topics),
            "chunksize": int(chunk_size),
            "passes": int(passes),
            "iterations": int(iterations),
            "eval_every": _to_int_or_none(eval_every),
            "alpha": alpha,
            "eta": eta
        }


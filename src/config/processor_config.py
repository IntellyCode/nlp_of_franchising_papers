from src.config import Config


class ProcessorConfig(Config):
    def set_config(self, capitalise: bool = False):
        """
        :param capitalise: Should the tokens be capitalised?
        :return:
        """
        self._config["capitalise"] = capitalise

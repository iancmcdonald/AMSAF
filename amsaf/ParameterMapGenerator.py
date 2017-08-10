class ParameterMapGenerator(object):
    def __init__(self, parameterPriors):
        super(ParameterMapGenerator, self).__init__()
        self._paramGridDict = {}
        self._applyParameterPriors(parameterPriors)

    def _applyParameterPriors(self, parameterPriors):
        # type: (dict) -> None
        pass

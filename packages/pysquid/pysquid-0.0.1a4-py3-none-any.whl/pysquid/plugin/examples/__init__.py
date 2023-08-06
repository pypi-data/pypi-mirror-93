import pysquid.plugin


class SamplePlugin1(pysquid.plugin.Plugin):
    def __init__(self):
        super().__init__('sample_plugin_1')


EXPORTS = [SamplePlugin1]

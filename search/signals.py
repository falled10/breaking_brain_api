from django_elasticsearch_dsl.signals import BaseSignalProcessor


class FakeSignalProcessor(BaseSignalProcessor):
    def setup(self):
        pass

    def teardown(self):
        pass

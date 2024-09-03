from django.db.models.signals import post_save

class DisableSignals:
    def __init__(self, *signals):
        self.signals = signals
        self.original_receivers = {}

    def __enter__(self):
        for signal in self.signals:
            self.original_receivers[signal] = signal.receivers
            signal.receivers = []

    def __exit__(self, exc_type, exc_value, traceback):
        for signal in self.signals:
            signal.receivers = self.original_receivers[signal]
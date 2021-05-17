from channels.consumer import SyncConsumer


class WebAppConsumer(SyncConsumer):

    def app1_message(self, message):
        # do something with message
        pass
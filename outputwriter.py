from datetime import datetime
from json import dumps as _

class OutputWriter():

        def get_pio_time(self):
                now = str(datetime.now())
                return now[:10] + "T" + now[11:-3] + "+0000"

        def __init__(self):
                self.output_file = open('articles.json', 'a')

        def output(self, label, text, entity_id, score):
                obj = {
                        'event': 'articles',
                        'entityType': 'political',
                        'entityId': entity_id,
                        'eventTime': self.get_pio_time(),
                        'properties': {
                                'text': text,
                                'label': label,
				'score': score
			}
		}

		self.output_file.write(_(obj) + '\n')

	def close(self):
		self.output_file.close()


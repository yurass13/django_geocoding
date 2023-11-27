from rest_framework.parsers import BaseParser
from typing import Optional, List, Dict

class CsvUploadParser(BaseParser):
    """Text csv parser.
        Read, decode and return csv from request.
    """
    media_type = 'text/csv'

    def parse(self, stream, media_type=None, parser_context=None) -> Dict:
        """Decode to utf-8, create dataset List[Dict] and return.
        :return: {'address': $dataset}
        # TODO handling errors
        """
        data = stream.read().decode('utf-8')

        dataset: List[Dict[str, str]] = []
        fields: Optional[List[str]] = None

        for row in data.split('\n'):
            if row == '':
                continue

            if fields is None:
                fields = row.split(',')
            else:
                dataset.append(dict(zip(fields, row.split(','))))

        return {'address': dataset}

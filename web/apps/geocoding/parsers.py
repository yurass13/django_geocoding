from rest_framework.parsers import BaseParser
from typing import Optional, List, Dict

import csv
import io


class CsvUploadParser(BaseParser):
    """Text csv parser.
        Read, decode and return csv from request.
    """
    media_type = 'text/csv'

    def parse(self, stream, media_type=None, parser_context=None) -> Dict:
        """Decode to utf-8, create dataset List[Dict] and return.
        :return: {'address': $dataset}
        """

        data = csv.reader(io.StringIO(stream.read().decode('utf-8'), newline='\n'),
                          delimiter=',',
                          quotechar='"')

        dataset: List[Dict[str, str]] = []
        fields: Optional[List[str]] = None

        for row in data:
            if fields is None:
                fields = row
            else:
                dataset.append(dict(zip(fields, row)))

        return {'address': dataset}

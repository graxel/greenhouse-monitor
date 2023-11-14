import sys
import fil

import time
print(sys.path, flush=True)



data_to_insert = [
    ("value1a", "value2a"),
    ("value1b", "value2b"),
    ("value1c", "value2c")
]

# fil.test_save(data_to_insert)
fil.scrape_company_page('Point72', 'https://boards.greenhouse.io/point72')
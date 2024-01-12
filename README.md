# Jugendschutzprogramm API
This is a simple API client for the [Jugendschutzprogramm API](https://www.jugendschutzprogramm.de/). It allows you to query the age rating of a website.

This might be useful if you want to check if a website is suitable for children or just want to know if your website is blocked by the [Jugendschutzprogramm](https://www.jugendschutzprogramm.de/). 

## Installation
```bash 
pip install jugendschutzprogramm
```

## Usage
```python
from jugendschutzprogramm import JugendschutzAPIClient 

client = JugendschutzAPIClient()
result = client.check("https://www.google.com")

print(result)
print(result.age)
print(result.url)
```

## License
This project is licensed under the terms of the Apache 2.0 license.

## Disclaimer
This project is not affiliated with or encouraged by the [Jugendschutzprogramm](https://www.jugendschutzprogramm.de/). However it is a helpful for journalists and researchers to check if a website is blocked by the [Jugendschutzprogramm](https://www.jugendschutzprogramm.de/).

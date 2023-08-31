# Accessibility Checker (Hack the 6ix 2023 project)

A web application built with Taipy (an open-sourced Python library) to check the accessibility of a web page given its URL.

### Winner of the Best Use of Taipy Award

### Devpost submission link: https://devpost.com/software/website-accessibility-checker

## Contributors: Amanda Guo, Miranda Guo, Prem Patel, Adnan Habib

### Setup local development environment on MacOS (following this guide: https://mlh.github.io/Getting-Started-with-Taipy/):

1. Download Python 3.8 or newer (check by running `python3 --version`)
2. Download pip (check by running `python3 -m pip --version`)
3. Run `python3 -m pip install taipy`

### Setup local development environment on Linux (following this guide: https://mlh.github.io/Getting-Started-with-Taipy/):

1. Download Python 3.8 or newer (check by running `python3 --version`)
2. Download pip (check by running `python3 -m pip --version`)
3. Run `pip install taipy`

### Running the app locally:

1. Go to https://wave.webaim.org/api/register and create an account. Note the API key that WAVE provides you (includes 100 free credits)
2. Clone this repository to your local development environment
3. Create a `.env` file and add the following to it:

```
API_KEY="<insert your API key from WAVE>"
URL="https://alphagov.github.io/accessibility-tool-audit/test-cases.html"
```

4. Open terminal and run `python3 main.py`
5. Open up 127.0.0.1:5001 in your browswer to check that the application is running

### Taipy resources:

YouTube tutorials: https://www.youtube.com/@taipy_io  
Official docs: https://www.taipy.io/ and https://docs.taipy.io/en/latest/getting_started/

### Other Technologies

Uses data collected from the WAVE API: https://wave.webaim.org/api/details

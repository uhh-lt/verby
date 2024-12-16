# Segment text using SpaCy
This project segments text sent to it into both sentences and verbal phrases.
For now **only German** is supported!
We primarily aim to provide a simple way of splitting text into verbal phrases as proposed in [Vauth et al (2021)](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2021-vauth-hatzel-chr.pdf).
In addition, we also provide a way of splitting the text into sentences.

## Building the Docker Image
In the project's top-level directory run: `docker build -t verby .`
This will build a docker image that can be run with: `docker run -p 8000:80 verby` where the `-p` option will ensure that you can access the api on port 8000 from your host.

### HTTP API
After starting the server either via docker or in a development setup you should be able to post you segmentation requests.

Using the CLI tool httpie:
```
http POST 127.0.0.1:8000/segment text="Ich gehe auf einem Wagen, oder wie manche sagen einem Auto, spazieren. Du gehst nachhause."
```

Or from Python code:
```python
import requests
response = requests.post("http://127.0.0.1:8000/segment", json={"text": "Ich gehe auf einem Wagen, oder wie manche sagen einem Auto, spazieren. Du gehst nachhause."})
print(response.json())
# Prints: {'verbal_phrases': [[[0, 30], [60, 69]], [[31, 47]], [[71, 90]]], 'sentences': [[0, 70], [71, 90]]}
```

You will get a response object with the character offsets of sentences and verbal phrases.
Note that verbal phrases may be discontinuous, as in the case above with the insertion.

## Development Server
To run a development server just execute `fastapi dev web.py`

## Library Usage
If you would prefer using _verby_ as a library rather than via HTTP, you can use this sample code as a starting point.
```python
import verby

nlp = verby.pipeline.build_pipeline("de")

doc = nlp("Sie lassen alle die krank sind nachhause gehen.")
for phrase in doc._.verbal_phrases:
    for span in phrase:
        print(span.start_char, span.end_char)
```

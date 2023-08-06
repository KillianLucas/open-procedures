# Open Procedures

**Open Procedures** is an open-source project offering tiny, structured coding tutorials that can be searched semantically. It was created to help [code-interpreting language models](http://openinterpreter.com/) complete various tasks by fetching relevant and up-to-date code snippets.

The entire collection of coding tutorials is open source and can be found on [GitHub](https://github.com/KillianLucas/open-procedures/tree/main/procedures). The community is highly encouraged to contribute by adding new tutorials or editing existing ones.

[Here's an example query](https://open-procedures.replit.app/search/?query=traceback) for learning how to handle a traceback in Python.

View the source or contribute to the project on [GitHub](https://github.com/KillianLucas/open-procedures).

## Query Open Procedures

### Using Python

```python
import requests

query = 'How to reverse a string in Python?'
response = requests.get('https://open-procedures.replit.app/search/', params={'query': query})

print(response.json())
```

### Using cURL

```bash
curl -G 'https://open-procedures.replit.app/search/' --data-urlencode 'query=How to reverse a string in Python?'
```

## Acknowledgments

Open Procedures was created by the people behind [Open Interpreter](http://openinterpreter.com/) to give large language models access to up-to-date code snippets.
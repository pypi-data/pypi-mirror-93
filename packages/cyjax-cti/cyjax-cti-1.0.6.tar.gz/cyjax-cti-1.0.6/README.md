## Introduction

```cyjax-cti``` is a Python library to use Cyjax platform API. You can access different resources (incident reports,
threat actors, indicators of compromise, etc.) from a Python script.

The library is available on [Python Package Index](http://pypi.python.org/pypi/cyjax-cti).

### Install 

You can install the ```cyjax-cti``` library with pip:

```
pip install cyjax-cti
```

### Supported resources
| Resource class         | .one()  | .list() |
| ---------------------- | ------- | ------- |
| IncidentReport         | &#9745; | &#9745; |
| IndicatorOfCompromise  | &#9746; | &#9745; |
| LeakedEmail            | &#9745; | &#9745; |
| MaliciousDomain        | &#9746; | &#9745; |
| MyReport               | &#9745; | &#9745; |
| Paste                  | &#9746; | &#9745; |
| Tweet                  | &#9746; | &#9745; |
| TorExitNode            | &#9745; | &#9746; |


### Examples

#### Set the API key

```python 
import cyjax

# set a global API key
cyjax.api_key = "346568ecf85f0b5ca98f389908e8b803"

# set a resource API key
cyjax.IndicatorOfCompromise(api_key="346568ecf85f0b5ca98f389908e8b803")
```

#### Get indicators of compromise in the last 5 minutes

```python 
import cyjax
from datetime import timedelta

cyjax.api_key = "346568ecf85f0b5ca98f389908e8b803"

indicators = cyjax.IndicatorOfCompromise().list(since=timedelta(minutes=5))
for indicator in indicators:
    print(indicator)
```

#### Get APT activity in last 6 months

```python 
import cyjax
from datetime import timedelta

cyjax.api_key = "346568ecf85f0b5ca98f389908e8b803"

reports = cyjax.IncidentReport().list(query="APT", since=timedelta(days=30*6))
for report in reports:
    print("Title: {}" % report['title'])
    print("Severity: {}" % report['severity'])
    print("Timestamp: {}" % report['last_update'])
```

#### Get leaked emails in the last 30 days

```python 
import cyjax
from datetime import timedelta

cyjax.api_key = "346568ecf85f0b5ca98f389908e8b803"

for leaked_email in cyjax.LeakedEmail().list(since=timedelta(days=30)):
    print("Email: {}" % leaked_email['email'])
    print("Source: {}" % leaked_email['source'])
    print("Timestamp: {}" % leaked_email['discovered_at'])
```

#### Get incident report by ID

```python 
import cyjax

cyjax.api_key = "346568ecf85f0b5ca98f389908e8b803"

incident_report = cyjax.IncidentReport().one(10)

print("Report title: {}" % incident_report.get('title'))
print("Report severity: {}" % incident_report.get('severity'))
print("Report content: {}" % incident_report.get('content'))
```
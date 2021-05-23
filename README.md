## Robot Framework plugin for OpenSTF

[![Unit tests](https://github.com/OpenTMI/robot-stf/actions/workflows/test.yml/badge.svg)](https://github.com/OpenTMI/robot-stf/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/OpenTMI/robot-stf/badge.svg?branch=main&t=CQV17G)](https://coveralls.io/github/OpenTMI/robot-stf?branch=main)

Library provides Robot Framework plugin to 
allocate phone from STF phone farm, create ADB connection to phone and start Appium server for testing.

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
* openstf server and access token 
* Robot Framework
* adb
* appium (`npm install appium`)
  Library expects that appium is located to PATH

### Installing

* `pip install robot-stf`
  
or for development purpose:

* `pip install -e .`

### Running the tests

`make test`

CI runs tests against following environments:

|   | ubuntu-latest | macos-latest | windows-latest |
| ------------- | ------------- | ------------- | ------------- |
| 3.7  | ✓  | ✓  | ✓  |
| 3.8  | ✓  | ✓  | ✓  |
| 3.9  | ✓  | ✓  | ✓  |

### Deployment

This pip package should be in dependency list in your tests.

### Usage

```
Library   robot-stf     host=<host>   token=<token>

Keywords:

$PHONE = Allocate Phone    <requirements>
Start adb   <phone>
Start Appium
```

See examples from [examples](examples) -folder.


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

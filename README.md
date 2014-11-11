cmdpr
=====
Command line tool for creating pull requests on GitHub
Creates GitHub pull request for current branch in current git repository.

Requirements
=====
 * python 2.7
 * requests

Installation
=====
```bash
python setup.py install
```
## Authorization
1. Create new personal access token in GitHub (Settings -> Applications -> Generate new token). Only "repo" scope required.
1. Save access token in environment variable `CMDPR_TOKEN`

Usage
=====
```
cmdpr [-h] -m SUMMARY [-b BASE_BRANCH]
```

Plans
====
 1. Add creating personal access token through basic authorization
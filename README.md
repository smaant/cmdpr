cmdpr
=====
Command line tool for creating pull requests on GitHub
Creates GitHub pull request for current branch in current git repository.

Requirements
=====
 * python 2.7
 * requests
 * PyYAML (for unit tests)

Installation
=====
```bash
python setup.py install
```
## Authorization
On first launch you'll be prompted to enter your GitHub login/password (and two-factor authorization code if enabled). Using provided credentials personal access token will be created and stored in config file (`~/.config/cmdpr`).

**Personal access token will grant access to your repositories (public and private) for anyone who has it. Therefore don't use *cmdpr* on any public or not trusted computers.**

In any case you can revoke any of your personal access tokens from your settings on GitHub. See [this blog post](https://github.com/blog/1509-personal-api-tokens) for more details.

Usage
=====
```
cmdpr [-h] [-m SUMMARY] [-b BASE_BRANCH] [--debug]
```
If you don't provide summary, *cmdpr* will open a text editor with a list of commits on current branch, so you can write one.

If base branch is omitted `master` will be implied.

Uninstall
====
The easiest way to uninstall *cmdpr* is to use `pip`:
```bash
pip uninstall cmdpr
```
**Don't forget to remove your config file if you're not going to use *cmdpr* later:**
```bash
rm ~/.config/cmdpr
```

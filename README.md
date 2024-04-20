# GitHub Codespaces ♥️ Flask

Welcome to your shiny new Codespace running Flask! We've got everything fired up and running for you to explore Flask.

You've got a blank canvas to work on from a git perspective as well. There's a single initial commit with the what you're seeing right now - where you go from here is up to you!

Everything you do here is contained within this one codespace. There is no repository on GitHub yet. If and when you’re ready you can click "Publish Branch" and we’ll create your repository and push up your project. If you were just exploring then and have no further need for this code then you can simply delete your codespace and it's gone forever.

To run this application:

```
flask --debug run
```

# Install

Create a virtualenv and activate it:

```
python3 -m venv .venv
. .venv/bin/activate
```

Or on Windows cmd:

```
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

Install SJSUBot:
```
pip install -e .
```

# Run

Initialize Database (Only once and to cleanup after SQL schema change):
```
flask --app flaskr init-db
```

Start webserver (With debug flag, changes to source file is dynamically loaded)
```
flask --app flaskr run --port 8001 --debug
```

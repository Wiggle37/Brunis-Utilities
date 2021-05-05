from flask import Flask
app = Flask('app')

@app.route('/')
def hello_world():
  return 're'

app.run()
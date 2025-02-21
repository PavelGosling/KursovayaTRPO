from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
  if request.method == 'GET':
    return  render_template('helloworld.html')
  else:
    print(request.form['username'])
    print(request.form['password'])
    return 'Hi POST'

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0', port=8080)
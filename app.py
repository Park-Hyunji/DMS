from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('projectSystem.html') # 기본 실행 html 페이지

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) # 8080포트로 접속


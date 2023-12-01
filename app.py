from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Replace with your Power BI embed URL
    embed_url = "https://app.powerbi.com/reportEmbed?reportId=34efc983-b281-4498-9635-c19ee04ae3e3&autoAuth=true&embeddedDemo=true"
    return render_template('index.html', embed_url=embed_url)

if __name__ == '__main__':
    app.run(debug=True)

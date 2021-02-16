from flask import Flask, render_template, request,redirect, url_for, session

app = Flask(__name__)

@app.route('/')
def index():
    return "<a> Hello World </a>"
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

from Python_file import OPC_UA_Client

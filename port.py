import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
import requests
import webbrowser
from threading import Timer
from bson.json_util import dumps, loads
import json
import pymongo
from pymongo import MongoClient


client = MongoClient()
portfolio_ports_db = client["portfolio_ports"]
portfolios_col = portfolio_ports_db["portfolios"]

app = Flask(__name__)

@app.route("/create-portfolio", methods=["GET"])
def create_portfolio():

    username = request.args.get("username")
    portfolio_name = request.args.get("portfolio")
    stocks = float(request.args.get("stocks"))
    bonds = float(request.args.get("bonds"))
    cash = float(request.args.get("cash"))

    api_key = request.args.get("key")
    
    portfolio = {"portfolio_name": portfolio_name, "stocks": stocks, "bonds": bonds, "cash": cash}

    try:
        portfolios_col.update_one( {"username" : username, "APIkey": api_key, "portfolio_name" : portfolio_name }, 
                {"$set": portfolio}, upsert=True)
        results = {"success": 1}
    except:
        results = {"success": 0, "error_msg": "Something has gone wrong"}
    
    return jsonify({"results": results})


@app.route("/return-portfolios", methods=["GET"])
def return_portfolios():

    username = request.args.get("username")
    api_key = request.args.get("key")

    portfolios = list(portfolios_col.find({"username": username, "APIkey": api_key}))

    for portfolio in portfolios:
        del portfolio["_id"]

    return jsonify({"results": portfolios})

@app.route("/return-portfolio", methods=["GEt"])
def return_portfolio():

    username = request.args.get("username")
    portfolio_name = request.args.get("portfolio-name")
    api_key = request.args.get("key")

    portfolio = portfolios_col.find_one({"username": username, "APIkey": api_key, "portfolio_name": portfolio_name})

    del portfolio["_id"]

    return jsonify({"results": portfolio})


@app.route("/delete-portfolio", methods=["GET"])
def delete_portfolio():

    username = request.args.get("username")
    portfolio_name = request.args.get("portfolio-name")
    api_key = request.args.get("key")

    try:
        portfolios_col.delete_one({"username": username,  "APIkey": api_key, "portfolio_name": portfolio_name})
        results = {"success": 1}
    except:
        error_msg = "something has gone wrong"
        results = {"success": 0, "error_msg": error_msg}

    return jsonify({"results": results})
    



if __name__ == "__main__":
    app.run(port=8003, debug=True)
import re
from flask import Flask, render_template, request, make_response, redirect, url_for
import google.generativeai as genai
from pymongo import MongoClient
from sql_db import connect_to_mysql, run_sql_query
from mongo_db import run_mongo_query
from json import loads, dumps

import typing_extensions
from config import GOOGLE_API_KEY, safety_settings

g_use_mongo, g_user, g_pass, g_db = False, None, None, None


genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)


class Schema(typing_extensions.TypedDict):
    column_1: str
    column_2: str
    column_3: str
    column_4: str


# MongoDB connection setup
def get_explanation(model, query):
    explanation_query = f"""
                Explain this SQL Query:
                        ...
                        {query}
                        ...               
                """
    explanation = model.generate_content(
        explanation_query, safety_settings=safety_settings
    )

    return explanation.text


def convert_to_list(table_str):
    print(table_str)
    print(type(table_str))
    table_dict = loads(table_str)
    table_headings = list(table_dict[0].keys())
    table_list = [table_headings]

    for dict_record in table_dict:
        row = list(dict_record.values())
        table_list.append(row)

    return table_list


def get_expected_output(model, query):
    expected_output = f"""
                What would be the expected response of this query snippet {query}         
                fill sample data      
                
            """
    json_model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
    result = json_model.generate_content(
        expected_output,
        safety_settings=safety_settings,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=list[Schema]
        ),
    )
    print(result.text)

    return result.text

@app.route("/is_mongo",methods=["GET"])
def is_mongo():
    return {"use_mongo": g_use_mongo}

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    global g_use_mongo, g_user, g_pass, g_db
    data = request.form.to_dict()
    values = data.values()
    if len(values) == 4:
        g_user, g_pass, g_db,  g_use_mongo = values
    else:
        g_user, g_pass, g_db = values
        g_use_mongo = False

    return redirect(url_for("sql_editor"))


@app.route("/sql_editor")
def sql_editor():
    return render_template("editor.html")


# For generating SQL or MongoDB query using the text prompt
@app.route("/get_query", methods=["POST"])
def gen_query():
    data = request.get_json()
    query = data["text_prompt"]

    if g_use_mongo:
        # If MongoDB is selected, generate MongoDB query
        text_prompt = f"Without any formatting, only plain text Generate a MongoDB query for {query}"
    else:
        # Generate MySQL query
        text_prompt = (
            f"Without any formatting, only plain text Generate a SQL query for {query}"
        )

    response = model.generate_content(text_prompt, safety_settings=safety_settings)
    print(response)
    query = response.text

    explanation = get_explanation(model, query)
    table = get_expected_output(model, query)

    if not (g_use_mongo):
        table_list = convert_to_list(table)
    else:
        table_list = table

    result = {"gen_query": query, "explanation": explanation, "table": table_list}

    return make_response(result)


# To execute SQL queries on MySQL
@app.route("/run_query", methods=["POST"])
def run_query():
    data = request.get_json()
    query = data["query"]

    # print(type(data["use_mongo"]))
    if not g_use_mongo:
        conn = connect_to_mysql(user=g_user, database=g_db, password=g_pass)
        results = run_sql_query(conn, query)
    else:
        results = loads(run_mongo_query(g_user, g_db, g_pass, query))

    # print(loads(results))
    return make_response({"output": results})


if __name__ == "__main__":
    app.run(debug=True)

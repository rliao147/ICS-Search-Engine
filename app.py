from flask import Flask, render_template, request
from search import stem_query, get_results, load_json
import time


app = Flask(__name__)
#tfidf_dict = load_json('dictionary_data/tfidf.json')
tfidf_dict = load_json('dictionary_data/lasttfidf.json')
idf_dict = load_json('dictionary_data/idf.json')
url_dict = load_json('dictionary_data/urldictionary.json')

@app.route("/", methods=["GET", "POST"])
def start():
    return render_template("index.html", url_list=[], hidden="hidden")


@app.route("/handle-query", methods=["GET", "POST"])
def index():
    query = request.form['query']
    start_time = time.time()
    # processed_query = remove_duplicates(stem_query(query))
    processed_query = stem_query(query, idf_dict)
    info = get_results(tfidf_dict, processed_query)
    searchTime = time.time() - start_time
    info = [url_dict[x] for x in info]
    return render_template("index.html", url_list=info, search_time=searchTime, hidden="")


if __name__ == "__main__":
    app.run(port=2888, debug=True)

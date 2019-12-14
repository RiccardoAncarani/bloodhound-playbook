import nbformat as nbf
import glob 
import yaml
import os



def get_all_queries(query_path):
    return glob.glob(query_path + "*.yaml")



db_connection_template = """\
from py2neo import Graph
from scripts.vis import *
from IPython.core.display import HTML

g = Graph("bolt://{}:7687", auth=("{}", "{}"))
options = {{"Group": "name", "Computer": "name", "GPO": "name", "Domain": "name", "User": "name", "OU": "name"}}"""

graph_query_template = """\
res = g.run(\"\"\"
{}\"\"\")
subg = res.to_subgraph()
try:
    display(draw_subgraph(subg, options))
except:
    print("No results returned from the query.")"""

table_query_template = """\
res = g.run(\"\"\"
{}\"\"\").to_data_frame()
if not res.empty:
    display(HTML(res.to_html()))
else:
    print("No results returned from the query.")
"""

if __name__ == "__main__":

    nb = nbf.v4.new_notebook()
    connection_code = db_connection_template.format(os.getenv('NEO4J_HOST'), os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))
    nb['cells'] = [nbf.v4.new_code_cell(connection_code)]

    query_path = "queries/"
    queries = get_all_queries(query_path)
    for query in queries:
        with open(query, "r") as stream:
            q = yaml.safe_load(stream)
            nb["cells"].append(nbf.v4.new_markdown_cell("## " + q["name"]))
            nb["cells"].append(nbf.v4.new_markdown_cell(q["description"]))
            if q["type"] == "graph":
                nb['cells'].append(nbf.v4.new_code_cell(graph_query_template.format(q["query"])))
            if q["type"] == "table":
                nb['cells'].append(nbf.v4.new_code_cell(table_query_template.format(q["query"])))
    nbf.write(nb, 'result.ipynb')
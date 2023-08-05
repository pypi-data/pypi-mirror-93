TEMPLATE = """
# File List

Here is a list of all files with brief descriptions:

{% for node in nodes recursive %}
{%- if node.is_dir or node.is_file %}
* **{{node.kind.value}}** [**{{node.name_short}}**]({{node.url}}) {{node.brief}}
{%- if node.has_children %}
  {{- loop(node.children)|indent(2, true) }}
{%- endif %}
{%- endif -%}
{%- endfor %}
"""

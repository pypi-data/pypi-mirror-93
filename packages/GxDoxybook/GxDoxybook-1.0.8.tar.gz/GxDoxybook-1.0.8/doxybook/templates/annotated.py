TEMPLATE = """
# Class List

Here are the classes, structs, unions and interfaces with brief descriptions:

{% for node in nodes recursive %}
{%- if node.is_parent %}
* **{{node.kind.value}}** [**{{node.name_short}}**]({{node.url}}) {{node.brief}}
{%- if node.has_children %}
  {{- loop(node.children)|indent(2, true) }}
{%- endif %}
{%- endif -%}
{%- endfor %}
"""

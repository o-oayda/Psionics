---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

<!-- due to yml structure in powers_final,
    this returns key, val -->
{% for power in site.data.powers_final %}
{{ power[1].Name }}
{% endfor %}
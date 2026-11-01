// Lead Organisations
{% if page['lead-organisations'] %}
  {% for org_slug in page['lead-organisations'] %}
    {% assign org = site.organisations | where: "slug", org_slug | first %}
    {% if org and org['main-location'] %}
      {% for loc_slug in org['main-location'] %}
        {% assign loc = site.locations | where: "slug", loc_slug | first %}
        {% if loc and loc.latitude and loc.longitude %}
        {
          lat: parseFloat("{{ loc.latitude }}"),
          lng: parseFloat("{{ loc.longitude }}"),
          title: "{{ org.title | escape }} (Lead)",
          color: "#496a40",
          radius: 7,
          weight: 2
        },
        {% endif %}
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endif %}

// Involved Organisations
{% if page['involved-organisations'] %}
  {% for org_slug in page['involved-organisations'] %}
    {% assign org = site.organisations | where: "slug", org_slug | first %}
    {% if org and org['main-location'] %}
      {% for loc_slug in org['main-location'] %}
        {% assign loc = site.locations | where: "slug", loc_slug | first %}
        {% if loc and loc.latitude and loc.longitude %}
        {
          lat: parseFloat("{{ loc.latitude }}"),
          lng: parseFloat("{{ loc.longitude }}"),
          title: "{{ org.title | escape }} (Involved)",
          color: "#8fa68b",
          radius: 4.5,
          weight: 1.5
        },
        {% endif %}
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endif %}

// Participants
{% if page.participants %}
  {% for part_slug in page.participants %}
    {% assign part = site.participants | where: "slug", part_slug | first %}
    {% if part and part.locations %}
      {% for loc_slug in part.locations %}
        {% assign loc = site.locations | where: "slug", loc_slug | first %}
        {% if loc and loc.latitude and loc.longitude %}
        {
          lat: parseFloat("{{ loc.latitude }}"),
          lng: parseFloat("{{ loc.longitude }}"),
          title: "{{ part.title | escape }} (Participants)",
          color: "#e67e22",
          radius: 5.5,
          weight: 1.5
        },
        {% endif %}
      {% endfor %}
    {% endif %}
  {% endfor %}
{% endif %}

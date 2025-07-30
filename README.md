GLEIF Model Context Protocol (MCP) Server
========================================
This MCP server exposes a *tool* for each of the primary resources documented in
GLEIF's public REST API v1.0 – see the full list at
https://documenter.getpostman.com/view/7679680/SVYrrxuU?version=latest.

The goal is to make the GLEIF dataset easily accessible to large‑language‑model
agents via MCP by wrapping the most frequently‑used endpoints as individual
MCP **tools**.

Covered resources / tools
-------------------------
• LEI records
  • list_lei_records              GET /lei-records
  • get_lei_record                GET /lei-records/{lei}
  • search_lei_records            GET /lei-records?filter[…]
• Relationship helpers (fuzzy / auto completion)
  • fuzzy_completions             GET /fuzzycompletions
  • auto_completions              GET /autocompletions
• LEI issuers (Managing LOU)
  • list_lei_issuers              GET /lei-issuers
  • get_lei_issuer                GET /lei-issuers/{id}
• Reference data
  • list_countries                GET /countries
  • get_country                   GET /countries/{code}
  • list_entity_legal_forms       GET /entity-legal-forms
  • get_entity_legal_form         GET /entity-legal-forms/{id}
• Metadata
  • list_fields                   GET /fields
  • get_field_details             GET /fields/{id}

Each tool returns the raw JSON payload from the GLEIF API or a JSON structure
of the form {"error": "…"} when a problem occurs

DSL_JSON_TEMPLATE = """
[
    {
        "name": "Authority",
        "plural_name": "authorities",
        "package": "authority",
        "fields": [
            { "name": "id", "type": "str", "primary_key": true },
            { "name": "name", "type": "str" },
            { "name": "code", "type": "str" },
            { "name": "parent_uuid", "type": "str" }
        ]
    },
    {
        "name": "User",
        "plural_name": "users",
        "package": "user",
        "fields": [
            { "name": "id", "type": "str", "primary_key": true },
            { "name": "login", "type": "str", "required": true },
            { "name": "password", "type": "str" },
            { "name": "first_name", "type": "str" },
            { "name": "last_name", "type": "str" },
            { "name": "email", "type": "str" },
            { "name": "activated", "type": "bool" },
            { "name": "lang_key", "type": "str" },
            { "name": "image_url", "type": "str" },
            { "name": "activation_key", "type": "str" },
            { "name": "reset_key", "type": "str" },
            { "name": "reset_date", "type": "date" },
            { "name": "authorities", "type": "List", "relation": "many_to_many" }
        ]
    }
]
Remeber the package name should be the same as the model name lower snake case
"""
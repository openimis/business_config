from core import datetime

today = datetime.date.today()
yesterday = today - datetime.datetimedelta(days=1)
tomorrow = today + datetime.datetimedelta(days=1)
mutation_id = "gn3084h5g893745hg98h"

gql_query_payload = """
query q {
    businessConfig {
        edges {
            node {
                id
                key
                value
                dateValidFrom
                dateValidTo
            }
        }
    }
}
"""

gql_create_payload = f"""
mutation m {{
    createBusinessConfig(input: {{
        key: "key1"
        value: "value1"
        dateValidFrom: "{str(yesterday)}"
        dateValidTo: "{str(tomorrow)}"
        clientMutationId: "{mutation_id}"
    }}) {{
        clientMutationId
    }}
}}
"""

gql_update_payload = f"""
mutation m ($id: ID!) {{
    updateBusinessConfig(input: {{
        id: $id
        value: "value2"
        clientMutationId: "{mutation_id}"
    }}) {{
        clientMutationId
    }}
}}
"""

gql_delete_payload = f"""
mutation m ($id: ID!) {{
    deleteBusinessConfig(input: {{
        ids: [$id]
        clientMutationId: "{mutation_id}"
    }}) {{
        clientMutationId
    }}
}}
"""

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

gql_query_payload_current = """
query q {
    currentBusinessConfig(key: "key1") {
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

gql_query_payload_date = """
query q ($date: Date!) {
    currentBusinessConfig(key: "key1", date: $date) {
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
        key: "key1"
        value: "value2"
        dateValidFrom: "{str(yesterday)}"
        dateValidTo: "{str(tomorrow)}"
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

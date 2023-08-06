async def update_mapping(es, index_name, alias, *args, **kwargs):
    pass


async def transform_all_documents(es, index_name, alias, *args, **kwargs):
    pass


current_mapping = {
    "type": "nested",
    "properties": {
        "t_dependencies": {
            "type": "nested",
            "properties": {
                "value": {"type": "keyword"},
                "lemma": {"type": "keyword"},
                "pos": {"type": "keyword"},
                "pos2": {"type": "keyword"},
            },
        },
        "t_entities": {"type": "keyword"},
        "t_ngrams": {"type": "keyword"},
        "t_lemma": {"type": "keyword"},
        "pos": {"type": "keyword"},
        "value": {"type": "keyword"},
    },
}


async def per_index(es, index, alias, *args, **kwargs):
    pass


async def up(es, *args, **kwargs):
    options = {
        "mappings": {
            "properties": {
                "name": {"type": "keyword"},
                "awesome": {"type": "boolean"},
            }
        },
    }

    # Ignore the "already exists" error
    await es.indices.create("demo-person", options)

    await es.index(
        "demo-person",
        {
            "name": "David Moffett",
            "awesome": True,
        },
    )
    await es.index(
        "demo-person",
        {
            "name": "Jonathan Zapata",
            "awesome": True,
        },
    )

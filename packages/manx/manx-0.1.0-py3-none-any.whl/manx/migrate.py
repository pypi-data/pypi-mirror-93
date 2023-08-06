import logging
from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch._async.helpers import async_scan
from elasticsearch.exceptions import ElasticsearchException

from manx.filename import MigrationFile, get_python_files

log = logging.getLogger("manx.migrate")
meta_index = "manx-metadata"


async def migrate_index(alias: str, migration_package: str, es: AsyncElasticsearch):
    py_migrations = list(get_python_files(migration_package))
    previous = await _fetch_previous_migrations(alias, es)
    gen = next_migration_to_apply(py_migrations, previous)

    for m in gen:
        await _apply(alias, m, es)


def next_migration_to_apply(
    migrations: List[MigrationFile], prev_mig: List[MigrationFile]
):
    prev_mig_iter = iter(prev_mig)
    current_mig = _next_or_none(prev_mig_iter)

    for migration in migrations:
        while migration.is_after(current_mig):
            log.info(f"IGNORE  {current_mig.stamp} {current_mig.name}")
            current_mig = _next_or_none(prev_mig_iter)

        stamp_match = False
        try:
            if migration.is_equal(current_mig):
                log.info(f"SKIP    {migration.stamp} {migration.name}")
                stamp_match = True
        except ValueError:
            log.warning(
                f"BADHASH {migration.stamp} {migration.name} Expected {current_mig.hash_} got {migration.hash_}"
            )
            stamp_match = True

        if stamp_match:
            current_mig = _next_or_none(prev_mig_iter)
        else:
            yield migration


def _next_or_none(iterator):
    try:
        return next(iterator)
    except StopIteration:
        return None


async def _apply(alias: str, migration_file: MigrationFile, es: AsyncElasticsearch):
    log.info(f"EXECUTE {migration_file.stamp} {migration_file.name}")

    try:
        # Create new index
        new_index_name = f"{alias}-{migration_file.stamp}"
        config = migration_file.module.configuration()
        await es.indices.create(index=new_index_name, body=config)
    except ElasticsearchException as e:
        log.error(e)
        raise e

    try:
        # Find old index name
        get_alias = await es.indices.get_alias(alias)
        old_index_name = list(get_alias)[0]

        # Scan over every document in the old index, update it, and insert it into the new index
        scan = async_scan(es, query={"query": {"match_all": {}}}, index=alias)
        async for old_doc in scan:
            new_doc = migration_file.module.up_doc(es, old_doc["_source"])
            await es.index(new_index_name, new_doc)
    except ElasticsearchException as e:
        log.error(e)
        log.error(f"Deleting index {new_index_name}")
        await es.indices.delete(new_index_name)
        raise e

    # Everything worked, now move the alias to the new index
    await es.indices.delete_alias(index=old_index_name, name=alias)
    await es.indices.put_alias(index=new_index_name, name=alias)

    # Delete the old index
    await es.indices.delete(old_index_name)

    # Log the successful migration in manx metadata index
    await es.index(meta_index, migration_file.to_meta_doc(alias))


async def _fetch_previous_migrations(alias: str, es: AsyncElasticsearch):
    res = await es.search(
        {"query": {"match": {"alias": alias}}},
        index=meta_index,
        size=1000,
        sort="stamp:asc",
    )

    migrations = []
    for record in res["hits"]["hits"]:
        source = record["_source"]
        stamp = source["stamp"]
        name = source["name"]
        sha3 = source["sha3"]
        mf = MigrationFile(stamp, name, None, sha3)
        migrations.append(mf)

    return migrations


async def _prepare_meta_index(es: AsyncElasticsearch):
    options = {
        "settings": {"index": {"hidden": "true"}},
        "mappings": {
            "properties": {
                "stamp": {"type": "integer"},
                "name": {"type": "keyword"},
                "sha3": {"type": "keyword"},
                "alias": {"type": "keyword"},
                "applied_at": {"type": "date"},
            }
        },
    }

    # Ignore the "already exists" error
    return await es.indices.create(meta_index, options, ignore=400)

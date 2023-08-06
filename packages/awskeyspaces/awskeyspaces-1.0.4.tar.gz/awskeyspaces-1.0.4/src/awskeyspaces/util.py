#!/usr/bin/env/ python
"""
    AWS KEYSPACE CONNECTOR UTIL
"""
import logging
import os

import cassandra
from cassandra.cqlengine import management

from .connection import connect


__all__ = ["migrate", "run_migrate", "create_ksp", "proxydb"]

_models_to_migrate = set()


def migrate(cls):
    """
    migrate(ModelA)
    add tables for sync
    """
    _models_to_migrate.add(cls)


@connect
def run_migrate():
    """
    migrate(ModelA)
    migrate(ModelB)

    run_migrate()
    # connect once
    """
    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
    for model in _models_to_migrate:
        try:
            management.sync_table(model, keyspaces=[os.getenv("CLUSTER_KSP")])
            logging.info(f"{model.__table_name__} table successfully synchronized.")
        except KeyError as e:
            logging.warning(f"table creation {e} has started, please wait a minute.")
        except cassandra.InvalidRequest as e:
            logging.warning(e)
            logging.warning("the {model.__table_name__} is not ready yet, please wait a minute.")


@connect
def create_ksp(keyspace=None):
    if (ksp := keyspace) is None:
        ksp = os.getenv("CLUSTER_KSP")

    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
    management.create_keyspace_simple(ksp, 1)
    logging.info(f"the keyspace {ksp} was created.")


@connect
def proxydb():
    """
    initialize connection with cassandra
    """
    return True

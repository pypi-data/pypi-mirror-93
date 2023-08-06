# pylint: disable=unused-argument,invalid-name,line-too-long

from parse import parse
from sqlalchemy import text as sql_text

from alembic_utils.exceptions import SQLParseFailure
from alembic_utils.on_entity_mixin import OnEntityMixin
from alembic_utils.replaceable_entity import ReplaceableEntity


class PGTrigger(OnEntityMixin, ReplaceableEntity):
    """A PostgreSQL Trigger compatible with `alembic revision --autogenerate`

    **Parameters:**

    * **schema** - *str*: A SQL schema name
    * **signature** - *str*: A SQL function's call signature
    * **definition** - *str*:  The remainig function body and identifiers
    * **on_entity** - *str*:  fully qualifed entity that the policy applies

    Postgres Create Trigger Specification:

        CREATE [ CONSTRAINT ] TRIGGER name { BEFORE | AFTER | INSTEAD OF } { event [ OR ... ] }
        ON table
        [ FROM referenced_table_name ]
        [ NOT DEFERRABLE | [ DEFERRABLE ] { INITIALLY IMMEDIATE | INITIALLY DEFERRED } ]
        [ FOR [ EACH ] { ROW | STATEMENT } ]
        [ WHEN ( condition ) ]
        EXECUTE PROCEDURE function_name ( arguments )
    """

    _template = "create{:s}trigger{:s}{signature}{:s}{event}{:s}ON{:s}{on_entity}{:s}{action}"

    @classmethod
    def from_sql(cls, sql: str) -> "PGTrigger":
        """Create an instance instance from a SQL string"""
        result = parse(cls._template, sql, case_sensitive=False)
        if result is not None:
            # remove possible quotes from signature
            signature = result["signature"]
            event = result["event"]
            on_entity = result["on_entity"]
            action = result["action"]

            if "." not in on_entity:
                on_entity = "public" + "." + on_entity

            schema = on_entity.split(".")[0]

            definition_template = " {event} ON {on_entity} {action}"
            definition = definition_template.format(event=event, on_entity=on_entity, action=action)

            return cls(
                schema=schema,
                signature=signature,
                on_entity=on_entity,
                definition=definition,
            )
        raise SQLParseFailure(f'Failed to parse SQL into PGTrigger """{sql}"""')

    def to_sql_statement_create(self):
        """ Generates a SQL "create function" statement for PGFunction """

        # We need to parse and replace the schema qualifier on the table for simulate_entity to
        # operate
        _def = self.definition
        _template = "{event}{:s}ON{:s}{on_entity}{:s}{action}"
        match = parse(_template, _def)
        if not match:
            raise SQLParseFailure(f'Failed to parse SQL into PGTrigger.definition """{_def}"""')

        event = match["event"]
        action = match["action"]

        # Ensure entity is qualified with schema
        on_entity = match["on_entity"]
        if "." in on_entity:
            _, _, on_entity = on_entity.partition(".")
        on_entity = f"{self.schema}.{on_entity}"

        # Re-render the definition ensuring the table is qualified with
        def_rendered = _template.replace("{:s}", " ").format(
            event=event, on_entity=on_entity, action=action
        )

        return sql_text(f"CREATE TRIGGER {self.signature} {def_rendered}")

    def to_sql_statement_drop(self, cascade=False):
        """Generates a SQL "drop function" statement for PGFunction"""
        cascade = "cascade" if cascade else ""
        return sql_text(f"DROP TRIGGER {self.signature} ON {self.on_entity} {cascade}")

    def to_sql_statement_create_or_replace(self):
        """ Generates a SQL "create or replace function" statement for PGFunction """
        return f"""
        DROP TRIGGER IF EXISTS {self.signature} ON {self.on_entity};
        {self.to_sql_statement_create()}
        """

    @classmethod
    def from_database(cls, sess, schema):
        """Get a list of all functions defined in the db"""

        sql = sql_text(
            """
        select
            pc.relnamespace::regnamespace::text as table_schema,
            tgname trigger_name,
            pg_get_triggerdef(pgt.oid) definition
        from
            pg_trigger pgt
                inner join pg_class pc
                    on pgt.tgrelid = pc.oid
        where
            not tgisinternal
            and pc.relnamespace::regnamespace::text like :schema
        """
        )
        rows = sess.execute(sql, {"schema": schema}).fetchall()

        db_triggers = [PGTrigger.from_sql(x[2]) for x in rows]

        for trig in db_triggers:
            assert trig is not None

        return db_triggers

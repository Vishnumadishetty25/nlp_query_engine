from typing import Dict, List, Any
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine

class SchemaDiscovery:
    def analyze_database(self, connection_string: str) -> Dict[str, Any]:
        """
        Connect to the database and return tables, columns and foreign keys.
        Uses SQLAlchemy inspection.
        """
        engine = create_engine(connection_string)
        inspector = inspect(engine)
        tables = {}
        for table_name in inspector.get_table_names():
            cols = inspector.get_columns(table_name)
            tables[table_name] = [c['name'] for c in cols]

        # gather foreign keys
        relationships = []
        for table_name in inspector.get_table_names():
            fks = inspector.get_foreign_keys(table_name)
            for fk in fks:
                relationships.append({
                    "table": table_name,
                    "constrained_columns": fk.get('constrained_columns'),
                    "referred_table": fk.get('referred_table'),
                    "referred_columns": fk.get('referred_columns')
                })

        return {"tables": tables, "relationships": relationships}

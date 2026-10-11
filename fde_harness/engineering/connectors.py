"""Enterprise connectors and legacy data sanitization for Pillar 1."""

import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SchemaDefinition(BaseModel):
    table_name: str
    columns: Dict[str, str] = Field(default_factory=dict)
    primary_key: Optional[str] = None
    foreign_keys: List[str] = Field(default_factory=list)


class LegacyDataCleaner:
    """Sanitizes messy real-world enterprise data into clean normalized formats."""

    @staticmethod
    def sanitize_record(record: Dict[str, Any]) -> Dict[str, Any]:
        """Cleans empty strings, replaces common null sentinels ('N/A', 'NULL', '-'),

        and normalizes keys.
        """
        cleaned = {}
        null_sentinels = {"n/a", "null", "none", "-", "undefined", "nil", ""}
        for k, v in record.items():
            norm_key = re.sub(r"[^a-zA-Z0-9_]", "_", str(k).strip().lower())
            if v is None:
                cleaned[norm_key] = None
            elif isinstance(v, str):
                s_val = v.strip()
                if s_val.lower() in null_sentinels:
                    cleaned[norm_key] = None
                else:
                    cleaned[norm_key] = s_val
            else:
                cleaned[norm_key] = v
        return cleaned

    @classmethod
    def clean_batch(cls, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [cls.sanitize_record(r) for r in records]


class EnterpriseConnector:
    """Manages connections to client databases, REST endpoints, and legacy file stores.

    Enforces read-only safety checks by default to prevent accidental data corruption
    in client environments.
    """

    def __init__(self, client_name: str = "EnterpriseClient", read_only: bool = True):
        self.client_name = client_name
        self.read_only = read_only
        self._mock_db: Dict[str, List[Dict[str, Any]]] = {}

    def register_table(self, table_name: str, records: List[Dict[str, Any]]) -> None:
        """Register a mock legacy table with sanitization."""
        cleaned = LegacyDataCleaner.clean_batch(records)
        self._mock_db[table_name.lower()] = cleaned

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Safely inspects and executes queries against the registered store."""
        cleaned_query = query.strip()
        is_write = any(kw in cleaned_query.upper().split() for kw in ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER"])
        
        if self.read_only and is_write:
            return {
                "success": False,
                "error": "Safety Violation: Modifying queries are blocked in read-only enterprise inspection mode.",
            }

        # Basic query simulation for demonstration and evaluation
        match = re.search(r"FROM\s+([a-zA-Z0-9_]+)", cleaned_query, re.IGNORECASE)
        if match:
            tbl = match.group(1).lower()
            if tbl in self._mock_db:
                rows = self._mock_db[tbl]
                return {
                    "success": True,
                    "table": tbl,
                    "row_count": len(rows),
                    "rows": rows[:50],  # Return up to 50 rows defensively
                }
            return {
                "success": False,
                "error": f"Table '{tbl}' not found in registered client schema.",
            }

        return {
            "success": True,
            "message": "Query validated and parsed successfully.",
        }

    def inspect_schema(self) -> Dict[str, List[str]]:
        """Returns detected tables and available columns."""
        schema = {}
        for tbl, rows in self._mock_db.items():
            if rows:
                schema[tbl] = list(rows[0].keys())
            else:
                schema[tbl] = []
        return schema

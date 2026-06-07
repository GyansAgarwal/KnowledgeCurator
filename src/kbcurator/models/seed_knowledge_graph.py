"""
Seed Knowledge Graph Models and Enumerations
For storing predefined graph templates
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
import uuid
import json


class GraphPurpose(str, Enum):
    """Predefined purposes for seed knowledge graphs"""
    FINANCIAL_ANALYSIS = "financial_analysis"
    ORGANIZATIONAL_STRUCTURE = "organizational_structure"
    PRODUCT_CATALOG = "product_catalog"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    SUPPLY_CHAIN = "supply_chain"
    CUSTOM = "custom"


class SeedKnowledgeGraph:
    """
    Stores template seed knowledge graphs with predefined entities,
    relationships, and parameters
    """
    def __init__(
        self,
        id: str = None,
        name: str = None,
        purpose: GraphPurpose = None,
        description: str = None,
        seed_entities: List[Dict] = None,
        seed_relationships: List[Dict] = None,
        entity_types: List[str] = None,
        relationship_types: List[str] = None,
        parameters: Dict = None,
        created_by: str = None,
        created_at: datetime = None,
        is_public: bool = True,
        tags: List[str] = None,
    ):
        """
        Initialize a seed knowledge graph template

        Args:
            id: Unique identifier (auto-generated if None)
            name: Template name (must be unique)
            purpose: GraphPurpose enum value
            description: Human-readable description
            seed_entities: List of initial entities
                Format: [{"name": "Company", "type": "ENTITY", "description": "..."}]
            seed_relationships: List of initial relationships
                Format: [{"source": "Company", "target": "Asset", "description": "owns", "weight": 1.0}]
            entity_types: Valid entity types for this graph
                Example: ["COMPANY", "ASSET", "PERSON", "TRANSACTION"]
            relationship_types: Valid relationship types
                Example: ["OWNS", "MANAGES", "REPORTS_TO"]
            parameters: Custom parameters for graph building
                Example: {"chunk_size": 1000, "overlap": 200}
            created_by: User ID who created this template
            created_at: Creation timestamp
            is_public: Whether template is publicly available
            tags: Categorization tags
        """
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.purpose = purpose
        self.description = description
        self.seed_entities = seed_entities or []
        self.seed_relationships = seed_relationships or []
        self.entity_types = entity_types or []
        self.relationship_types = relationship_types or []
        self.parameters = parameters or {}
        self.created_by = created_by
        self.created_at = created_at or datetime.utcnow()
        self.is_public = is_public
        self.tags = tags or []

    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "name": self.name,
            "purpose": self.purpose.value if isinstance(self.purpose, GraphPurpose) else self.purpose,
            "description": self.description,
            "seed_entities": self.seed_entities,
            "seed_relationships": self.seed_relationships,
            "entity_types": self.entity_types,
            "relationship_types": self.relationship_types,
            "parameters": self.parameters,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_public": self.is_public,
            "tags": self.tags,
        }

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data: Dict) -> "SeedKnowledgeGraph":
        """Create from dictionary"""
        return SeedKnowledgeGraph(
            id=data.get("id"),
            name=data.get("name"),
            purpose=GraphPurpose(data.get("purpose")) if data.get("purpose") else None,
            description=data.get("description"),
            seed_entities=data.get("seed_entities", []),
            seed_relationships=data.get("seed_relationships", []),
            entity_types=data.get("entity_types", []),
            relationship_types=data.get("relationship_types", []),
            parameters=data.get("parameters", {}),
            created_by=data.get("created_by"),
            created_at=datetime.fromisoformat(data.get("created_at")) if data.get("created_at") else None,
            is_public=data.get("is_public", True),
            tags=data.get("tags", []),
        )

    @staticmethod
    def from_json(json_str: str) -> "SeedKnowledgeGraph":
        """Create from JSON string"""
        data = json.loads(json_str)
        return SeedKnowledgeGraph.from_dict(data)

    def validate(self) -> tuple[bool, str]:
        """
        Validate the seed graph configuration

        Returns:
            (is_valid, error_message)
        """
        if not self.name:
            return False, "Name is required"

        if not self.purpose:
            return False, "Purpose is required"

        if not isinstance(self.purpose, GraphPurpose):
            try:
                GraphPurpose(self.purpose)
            except ValueError:
                return False, f"Invalid purpose: {self.purpose}"

        if self.seed_entities and not isinstance(self.seed_entities, list):
            return False, "seed_entities must be a list"

        if self.seed_relationships and not isinstance(self.seed_relationships, list):
            return False, "seed_relationships must be a list"

        # Validate entity types
        if self.entity_types and not isinstance(self.entity_types, list):
            return False, "entity_types must be a list"

        # Validate relationship types
        if self.relationship_types and not isinstance(self.relationship_types, list):
            return False, "relationship_types must be a list"

        # Validate parameters
        if self.parameters and not isinstance(self.parameters, dict):
            return False, "parameters must be a dictionary"

        return True, ""

    def __repr__(self):
        return f"SeedKnowledgeGraph(id={self.id}, name={self.name}, purpose={self.purpose})"

    def __str__(self):
        return f"{self.name} ({self.purpose}) - {self.description}"


# Predefined template examples for quick setup

FINANCIAL_ANALYSIS_TEMPLATE = SeedKnowledgeGraph(
    name="Financial_Analysis_v1",
    purpose=GraphPurpose.FINANCIAL_ANALYSIS,
    description="Template for financial analysis with key financial entities and relationships",
    seed_entities=[
        {"name": "Company", "type": "ENTITY", "description": "Financial institution or company"},
        {"name": "Asset", "type": "ENTITY", "description": "Financial asset or holding"},
        {"name": "Account", "type": "ENTITY", "description": "Financial account"},
        {"name": "Transaction", "type": "ENTITY", "description": "Financial transaction"},
        {"name": "Portfolio", "type": "ENTITY", "description": "Investment portfolio"},
    ],
    seed_relationships=[
        {"source": "Company", "target": "Asset", "description": "owns", "weight": 1.0},
        {"source": "Company", "target": "Account", "description": "manages", "weight": 1.0},
        {"source": "Account", "target": "Transaction", "description": "contains", "weight": 1.0},
        {"source": "Portfolio", "target": "Asset", "description": "includes", "weight": 1.0},
    ],
    entity_types=["COMPANY", "ASSET", "ACCOUNT", "TRANSACTION", "PORTFOLIO", "CLIENT"],
    relationship_types=["OWNS", "MANAGES", "CONTAINS", "INCLUDES", "EXECUTES"],
    parameters={"chunk_size": 1000, "overlap": 200},
    is_public=True,
    tags=["finance", "banking", "analysis"],
)

ORGANIZATIONAL_STRUCTURE_TEMPLATE = SeedKnowledgeGraph(
    name="Organizational_Structure_v1",
    purpose=GraphPurpose.ORGANIZATIONAL_STRUCTURE,
    description="Template for organizational hierarchy and structure",
    seed_entities=[
        {"name": "Organization", "type": "ENTITY", "description": "Top-level organization"},
        {"name": "Department", "type": "ENTITY", "description": "Business department"},
        {"name": "Team", "type": "ENTITY", "description": "Work team"},
        {"name": "Employee", "type": "ENTITY", "description": "Individual employee"},
        {"name": "Role", "type": "ENTITY", "description": "Job role or position"},
    ],
    seed_relationships=[
        {"source": "Organization", "target": "Department", "description": "contains", "weight": 1.0},
        {"source": "Department", "target": "Team", "description": "has", "weight": 1.0},
        {"source": "Team", "target": "Employee", "description": "members", "weight": 1.0},
        {"source": "Employee", "target": "Role", "description": "holds", "weight": 1.0},
        {"source": "Employee", "target": "Employee", "description": "reports_to", "weight": 1.0},
    ],
    entity_types=["ORGANIZATION", "DEPARTMENT", "TEAM", "EMPLOYEE", "ROLE"],
    relationship_types=["CONTAINS", "HAS", "MEMBERS", "HOLDS", "REPORTS_TO", "MANAGES"],
    parameters={"chunk_size": 800, "overlap": 150},
    is_public=True,
    tags=["organization", "structure", "hr"],
)

PRODUCT_CATALOG_TEMPLATE = SeedKnowledgeGraph(
    name="Product_Catalog_v1",
    purpose=GraphPurpose.PRODUCT_CATALOG,
    description="Template for product catalogs and inventory management",
    seed_entities=[
        {"name": "Product", "type": "ENTITY", "description": "Product or service"},
        {"name": "Category", "type": "ENTITY", "description": "Product category"},
        {"name": "Supplier", "type": "ENTITY", "description": "Product supplier"},
        {"name": "Price", "type": "ENTITY", "description": "Pricing information"},
        {"name": "Review", "type": "ENTITY", "description": "Product review"},
    ],
    seed_relationships=[
        {"source": "Product", "target": "Category", "description": "belongs_to", "weight": 1.0},
        {"source": "Product", "target": "Supplier", "description": "supplied_by", "weight": 1.0},
        {"source": "Product", "target": "Price", "description": "has_price", "weight": 1.0},
        {"source": "Product", "target": "Review", "description": "has_review", "weight": 1.0},
    ],
    entity_types=["PRODUCT", "CATEGORY", "SUPPLIER", "PRICE", "REVIEW", "INVENTORY"],
    relationship_types=["BELONGS_TO", "SUPPLIED_BY", "HAS_PRICE", "HAS_REVIEW", "RELATED_TO"],
    parameters={"chunk_size": 1200, "overlap": 250},
    is_public=True,
    tags=["product", "catalog", "inventory"],
)

SUPPLY_CHAIN_TEMPLATE = SeedKnowledgeGraph(
    name="Supply_Chain_v1",
    purpose=GraphPurpose.SUPPLY_CHAIN,
    description="Template for supply chain management and logistics",
    seed_entities=[
        {"name": "Supplier", "type": "ENTITY", "description": "Supply chain supplier"},
        {"name": "Manufacturer", "type": "ENTITY", "description": "Manufacturing entity"},
        {"name": "Distributor", "type": "ENTITY", "description": "Distribution entity"},
        {"name": "Retailer", "type": "ENTITY", "description": "Retail store or entity"},
        {"name": "Customer", "type": "ENTITY", "description": "End customer"},
    ],
    seed_relationships=[
        {"source": "Supplier", "target": "Manufacturer", "description": "supplies", "weight": 1.0},
        {"source": "Manufacturer", "target": "Distributor", "description": "ships_to", "weight": 1.0},
        {"source": "Distributor", "target": "Retailer", "description": "distributes_to", "weight": 1.0},
        {"source": "Retailer", "target": "Customer", "description": "sells_to", "weight": 1.0},
    ],
    entity_types=["SUPPLIER", "MANUFACTURER", "DISTRIBUTOR", "RETAILER", "CUSTOMER", "WAREHOUSE"],
    relationship_types=["SUPPLIES", "SHIPS_TO", "DISTRIBUTES_TO", "SELLS_TO", "MANAGES"],
    parameters={"chunk_size": 1500, "overlap": 300},
    is_public=True,
    tags=["supply_chain", "logistics", "distribution"],
)

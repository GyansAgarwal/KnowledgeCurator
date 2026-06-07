# Seed Knowledge Graph Implementation Guide

## Overview
This document contains all the code and setup instructions needed to implement the **Seed Knowledge Graph** feature in KnowledgeCurator. This allows users to select predefined graph templates or build from scratch.

---

## 📁 File Structure

```
src/kbcurator/
├── models/
│   └── seed_knowledge_graph.py          # Data models
├── utils/
│   └── seed_graph_manager.py            # Database operations
├── tools/
│   └── ingestion_new.py                 # Updated with new MCP tools
└── migrations/
    └── add_seed_knowledge_graphs_table.sql  # Database schema
```

---

## 🗄️ Step 1: Database Schema

Create a new migration file or run these SQL commands:

**File:** `migrations/add_seed_knowledge_graphs_table.sql`

```sql
-- Create seed knowledge graphs table
CREATE TABLE IF NOT EXISTS seed_knowledge_graphs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    purpose VARCHAR(50) NOT NULL,
    description TEXT,
    seed_entities JSONB DEFAULT '[]'::JSONB,
    seed_relationships JSONB DEFAULT '[]'::JSONB,
    entity_types JSONB DEFAULT '[]'::JSONB,
    relationship_types JSONB DEFAULT '[]'::JSONB,
    parameters JSONB DEFAULT '{}'::JSONB,
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT TRUE,
    tags JSONB DEFAULT '[]'::JSONB
);

-- Create knowledge graph templates tracking table
CREATE TABLE IF NOT EXISTS knowledge_graph_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain VARCHAR(255) NOT NULL,
    kb_name VARCHAR(255) NOT NULL,
    workspace_id VARCHAR(255),
    seed_graph_id UUID NOT NULL REFERENCES seed_knowledge_graphs(id) ON DELETE CASCADE,
    build_mode VARCHAR(20) NOT NULL DEFAULT 'from_seed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(domain, kb_name, workspace_id)
);

-- Create indexes
CREATE INDEX idx_seed_kg_purpose ON seed_knowledge_graphs(purpose);
CREATE INDEX idx_seed_kg_workspace ON seed_knowledge_graphs(is_public);
CREATE INDEX idx_kg_template_seed_graph ON knowledge_graph_templates(seed_graph_id);
CREATE INDEX idx_kg_template_workspace ON knowledge_graph_templates(workspace_id);
```

---

## 📝 Step 2: Create Models

**File:** `src/kbcurator/models/seed_knowledge_graph.py`

[See the complete code in the attached Python file]

---

## 🔧 Step 3: Create Manager

**File:** `src/kbcurator/utils/seed_graph_manager.py`

[See the complete code in the attached Python file]

---

## 🚀 Step 4: Update ingestion_new.py

Add the following new functions and modify existing ones:

### A. New Function: initialize_rag_with_seed()
- Initializes RAG with optional seed graph
- Applies seed entities and relationships
- [See complete code in IMPLEMENTATION_FUNCTIONS.md]

### B. New MCP Tools:
1. `create_seed_knowledge_graph()` - Create new templates
2. `list_seed_knowledge_graphs()` - List available templates
3. `get_seed_knowledge_graph()` - Get template details
4. `initialize_rag_with_template()` - Initialize with template
5. `get_kb_template_info()` - Get KB template info
6. `query_rag_with_seed_context()` - Query with seed constraints

---

## 💾 Step 5: Migration Execution

### Option A: Using psycopg2
```python
import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    dbname=os.getenv("POSTGRESQL_DATABASE_DATABASE_2")
)
cur = conn.cursor()

with open("migrations/add_seed_knowledge_graphs_table.sql", "r") as f:
    sql = f.read()
    cur.execute(sql)

conn.commit()
cur.close()
conn.close()
```

### Option B: Direct CLI
```bash
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRESQL_DATABASE_DATABASE_2 -f migrations/add_seed_knowledge_graphs_table.sql
```

---

## 🧪 Testing Examples

### 1. Create a Financial Analysis Template
```python
seed_graph = SeedKnowledgeGraph(
    name="Financial_Analysis_v1",
    purpose="financial_analysis",
    description="Template for financial analysis with key entities",
    seed_entities=[
        {"name": "Company", "type": "ENTITY", "description": "Financial company"},
        {"name": "Asset", "type": "ENTITY", "description": "Financial asset"},
        {"name": "Transaction", "type": "ENTITY", "description": "Financial transaction"},
    ],
    seed_relationships=[
        {"source": "Company", "target": "Asset", "description": "owns", "weight": 1.0},
        {"source": "Company", "target": "Transaction", "description": "executes", "weight": 1.0},
    ],
    entity_types=["COMPANY", "ASSET", "TRANSACTION", "PORTFOLIO"],
    relationship_types=["OWNS", "EXECUTES", "MANAGES", "CONTAINS"],
    parameters={"chunk_size": 1000, "overlap": 200},
    created_by="admin",
    is_public=True,
    tags=["finance", "analysis"],
)

manager = SeedGraphManager()
graph_id = manager.create_seed_graph(seed_graph)
```

### 2. Initialize KB with Template
```python
rag = await initialize_rag_with_seed(
    domain="Finance",
    kb_name="Banking",
    seed_graph_id=graph_id,
    build_mode="from_seed"
)
```

### 3. Query with Seed Context
```python
result = await query_rag_with_seed_context(
    domain="Finance",
    kb_name="Banking",
    question="What are the key assets?",
    use_seed_context=True
)
```

---

## 📋 Provided Seed Graph Templates

### 1. Financial Analysis
- **Purpose**: financial_analysis
- **Entities**: Company, Asset, Transaction, Portfolio, Account
- **Relationships**: OWNS, MANAGES, EXECUTES, CONTAINS

### 2. Organizational Structure
- **Purpose**: organizational_structure
- **Entities**: Organization, Department, Employee, Role, Team
- **Relationships**: PART_OF, MANAGES, REPORTS_TO, BELONGS_TO

### 3. Product Catalog
- **Purpose**: product_catalog
- **Entities**: Product, Category, Supplier, Price, Review
- **Relationships**: BELONGS_TO, SUPPLIED_BY, HAS_REVIEW, HAS_PRICE

### 4. Regulatory Compliance
- **Purpose**: regulatory_compliance
- **Entities**: Regulation, Rule, Requirement, Audit, Violation
- **Relationships**: DEFINES, REQUIRES, AUDITS, VIOLATES

### 5. Supply Chain
- **Purpose**: supply_chain
- **Entities**: Supplier, Manufacturer, Distributor, Retailer, Customer
- **Relationships**: SUPPLIES, MANUFACTURES, DISTRIBUTES, SELLS_TO

---

## 🔄 User Workflow

1. **Admin creates seed graphs** (one-time setup)
   - Defines entity types, relationship types
   - Sets predefined seed entities/relationships
   - Makes public for all users

2. **User initializes knowledge base**
   - Choose: "From Seed" or "From Scratch"
   - If "From Seed": Select graph template
   - KB is created with seed structure

3. **User uploads documents**
   - Documents are indexed
   - New entities/relationships are discovered
   - Graph grows from the seed

4. **User queries knowledge base**
   - Optionally use seed context for filtering
   - Results constrained to valid entity/relationship types (if enabled)

---

## 🔌 API Integration Points

### Frontend Calls:
1. `POST /api/seed-graphs` - Create seed graph
2. `GET /api/seed-graphs?purpose=financial_analysis` - List templates
3. `GET /api/seed-graphs/{graph_id}` - Get details
4. `POST /api/kb/initialize?template_id=xxx` - Init KB with template
5. `GET /api/kb/{domain}/{kb_name}/template` - Get KB template info

### Backend Implementation:
All endpoints already defined as MCP tools in `ingestion_new.py`

---

## ⚠️ Important Notes

1. **Backward Compatibility**: Existing KBs can continue without templates
2. **Migration Safe**: New schema doesn't affect existing data
3. **Optional Feature**: Can be enabled/disabled per workspace
4. **Performance**: Seed graphs are loaded once at initialization
5. **Customizable**: Users can create custom seed graphs

---

## 🛠️ Troubleshooting

### Issue: UUID not recognized in PostgreSQL
**Solution**: Ensure `uuid-ossp` extension is installed:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Issue: JSONB column errors
**Solution**: PostgreSQL version must be 9.4+. Check:
```sql
SELECT version();
```

### Issue: Foreign key constraint violations
**Solution**: Ensure seed_knowledge_graphs table exists before knowledge_graph_templates:
```sql
ALTER TABLE knowledge_graph_templates 
DROP CONSTRAINT IF EXISTS knowledge_graph_templates_seed_graph_id_fkey;
```

---

## 📞 Support

For issues or questions:
1. Check logs in `src/kbcurator/utils/seed_graph_manager.py`
2. Verify database connection parameters
3. Ensure all migrations have run
4. Check workspace_id is properly configured


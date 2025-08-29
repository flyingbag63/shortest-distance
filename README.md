## Order Routing

Given a batch of orders (with restaurants and customers), 
find a minimum cost path that visits all nodes in the batch 
such that each restaurant node is 
visited before its corresponding customer node.

---

### **Assumptions**

- **Data Store**: In-memory storage
- **Order Batch Size**: Up to **8–10 orders** per batch
- **Vanilla Python**
---

### **Entities**

- **Restaurant**
- **Customer**
- **Rider**
- **Location**
  - `object_id`
  - `location_type`
  - `timestamp`
- **Order**
  - `customer_id`
  - `restaurant_id`

---

### **DTOs**

- **Node**
- **Edge**
- **Graph**
  - `root`
  - `nodes`
  - `edges`

---

### **Services**

- **Service & Repository Layer**: Implemented for each entity
- **NodeTransformer (Abstract)**
  - Responsibility: Transform `Location` → `Node`
  - Methods:
    - `transform_one(Location) → Node`
    - `transform_many(List<Location>) → List<Node>`
    - `get_strategy() → StrategyType`
  - Factory: Provides transformer for a given strategy
- **DistanceCalculator (Abstract)**
  - Responsibility: Compute distance between two nodes
  - Methods:
    - `calculate(Node, Node) → distance`
    - `get_strategy() → StrategyType`
  - Factory: Provides calculator for a given strategy
  - Note: Number of calculators = Number of node transformers
- **GraphBuilder**
  - Takes a set of locations
  - Builds nodes and edges
  - Returns a `Graph` object
- **RouteFinder (Abstract)**
  - Responsibility: Find the optimal route for a given graph with a root
  - Factory: Provides finder for a given strategy

**Note**: Class variables, class methods provide ~ singleton and stateless behaviour for business classes.

---

## Data Flow

![Alt text for the image](data%20flow.png "Data Flow")

---

### **Approach: Dijkstra with Masking**

**`DijkstraWithMaskRouteFinder`**

- **Mask**: Bitmask of length = (#restaurants + #customers) in a batch

#### Algorithm Steps

1. Initialize with **root node (rider)**
2. Push `(cost=0, root_node, initial_mask)` into a priority heap
3. While heap is not empty:
   - Pop the current node and state
   - If `(current_node, mask)` is already visited → continue
   - For each neighbor (edge):
     - Compute new cost:
       - If neighbor is a **restaurant** → `max(current_cost + weight, min_available_time)`
       - Else → `current_cost + weight`
     - Update mask
     - Push `(new_cost, neighbor, updated_mask)` into heap
4. **Best cost** is reached when mask has **all bits set to 1** (all locations visited)

---

### **Textual Class Diagram**

```
Entity Layer:
-------------
Restaurant
Customer
Rider
Location(object_id, location_type)
Order(customer_id, restaurant_id)

DTO Layer:
----------
Node
Edge
Graph(root, nodes, edges)

Service Layer:
--------------
Repository<T>  // per entity
Service<T>     // per entity

NodeTransformer (Abstract)
  + transform_one(Location) → Node
  + transform_many(List<Location>) → List<Node>
  + get_strategy() → StrategyType
  ^-- Factory provides concrete strategy

DistanceCalculator (Abstract)
  + calculate(Node, Node) → distance
  + get_strategy() → StrategyType
  ^-- Factory provides concrete strategy

GraphBuilder
  + build(locations) → Graph

RouteFinder (Abstract)
  + findBestRoute(Graph, root) → Route
  ^-- Factory provides concrete strategy

Concrete Implementations:
--------------------------
NodeTransformer:
  HaversineNodeTransformer
    + transform_one(Location) → Node
    + transform_many(List<Location>) → List<Node>
    + get_strategy() → HAVERSINE

DistanceCalculator:
  HaversineDistanceCalculator
    + calculate(Node, Node) → distance
    + get_strategy() → HAVERSINE

RouteFinder:
  DijkstraWithMaskRouteFinder
    + findBestRoute(Graph, root) → Route
    - Uses bitmask for visited nodes
```


---

## Sample Response

```json
{
  "route": [
    {
      "node": {
        "latitude": "-47.71",
        "longitude": "3.98",
        "object_id": "e722a0db-da13-48df-ba15-bef1fad19155",
        "node_type": "Rider",
        "min_available_time": "0.00",
        "cost": "0",
        "mask": 0
      },
      "cost_till_here": "0"
    },
    {
      "node": {
        "latitude": "81.79",
        "longitude": "171.84",
        "object_id": "0d5d09a1-6971-44ab-bc37-ce22d748dfac",
        "node_type": "Restaurant",
        "min_available_time": "25.00",
        "cost": "810.06",
        "mask": 4
      },
      "cost_till_here": "810.06"
    },
    {
      "node": {
        "latitude": "-71.50",
        "longitude": "142.10",
        "object_id": "151d86f0-a1ea-42dc-ba13-6f54c2dfdcbe",
        "node_type": "Restaurant",
        "min_available_time": "45.00",
        "cost": "1666.60",
        "mask": 12
      },
      "cost_till_here": "1666.60"
    },
    {
      "node": {
        "latitude": "-79.02",
        "longitude": "120.44",
        "object_id": "5e396ba4-7f0c-4327-a78a-15a066b6bb16",
        "node_type": "Customer",
        "min_available_time": "0.00",
        "cost": "1717.76",
        "mask": 14
      },
      "cost_till_here": "1717.76"
    },
    {
      "node": {
        "latitude": "-17.46",
        "longitude": "-138.23",
        "object_id": "c5010a9e-250c-4297-b5f4-d0c81e927ee8",
        "node_type": "Customer",
        "min_available_time": "0.00",
        "cost": "2134.73",
        "mask": 15
      },
      "cost_till_here": "2134.73"
    }
  ]
}

```


---

## How to Run

1. cd `project directory`
2. Run `python main.py`

---

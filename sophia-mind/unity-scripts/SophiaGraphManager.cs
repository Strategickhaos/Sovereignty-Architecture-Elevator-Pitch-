using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System.Linq;

/// <summary>
/// SOPHIA MIND Brain Visualizer - Graph Manager
/// Loads and manages the 3D knowledge graph from parsed Obsidian data
/// 
/// Part of the Strategickhaos Sovereignty Architecture
/// </summary>
public class SophiaGraphManager : MonoBehaviour
{
    [Header("Graph Data")]
    public string graphDataPath = "graph_data.json";
    
    [Header("Node Prefab")]
    public GameObject nodePrefab;
    
    [Header("Layout Settings")]
    public float nodeSpacing = 5f;
    public LayoutType layoutType = LayoutType.Force;
    public int maxIterations = 100;
    
    [Header("Physics Settings")]
    public float springStrength = 0.1f;
    public float repulsionStrength = 100f;
    public float damping = 0.9f;
    
    private Dictionary<string, GameObject> nodeObjects;
    private List<NodeData> nodes;
    private List<EdgeData> edges;
    
    public enum LayoutType
    {
        Force,      // Force-directed layout
        Circular,   // Circular layout
        Grid,       // Grid layout
        Hierarchical // Tree-like hierarchical layout
    }
    
    [System.Serializable]
    public class GraphData
    {
        public MetaData metadata;
        public List<NodeData> nodes;
        public List<EdgeData> edges;
    }
    
    [System.Serializable]
    public class MetaData
    {
        public string vault_path;
        public int node_count;
        public int edge_count;
        public string export_version;
    }
    
    [System.Serializable]
    public class NodeData
    {
        public string id;
        public string title;
        public string path;
        public string[] glyphs;
        public int frequency;
        public string[] connections;
        public string[] tags;
    }
    
    [System.Serializable]
    public class EdgeData
    {
        public string source;
        public string target;
    }
    
    void Start()
    {
        nodeObjects = new Dictionary<string, GameObject>();
        LoadGraphData();
        CreateGraph();
        ApplyLayout();
        CreateConnections();
    }
    
    void LoadGraphData()
    {
        if (!File.Exists(graphDataPath))
        {
            Debug.LogError($"Graph data file not found: {graphDataPath}");
            return;
        }
        
        string json = File.ReadAllText(graphDataPath);
        GraphData data = JsonUtility.FromJson<GraphData>(json);
        
        nodes = data.nodes;
        edges = data.edges;
        
        Debug.Log($"Loaded {nodes.Count} nodes and {edges.Count} edges");
    }
    
    void CreateGraph()
    {
        if (nodes == null) return;
        
        // Create sphere prefab if not provided
        if (nodePrefab == null)
        {
            nodePrefab = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        }
        
        foreach (NodeData nodeData in nodes)
        {
            // Instantiate node
            GameObject nodeObj = Instantiate(nodePrefab);
            nodeObj.name = nodeData.id;
            nodeObj.transform.parent = transform;
            
            // Add SophiaGraphNode component
            SophiaGraphNode nodeComponent = nodeObj.AddComponent<SophiaGraphNode>();
            nodeComponent.nodeId = nodeData.id;
            nodeComponent.title = nodeData.title;
            nodeComponent.filePath = nodeData.path;
            nodeComponent.glyphTags = nodeData.glyphs;
            nodeComponent.frequency = nodeData.frequency;
            nodeComponent.connections = nodeData.connections;
            
            nodeObjects[nodeData.id] = nodeObj;
        }
        
        Debug.Log($"Created {nodeObjects.Count} node objects");
    }
    
    void ApplyLayout()
    {
        switch (layoutType)
        {
            case LayoutType.Force:
                ApplyForceDirectedLayout();
                break;
            case LayoutType.Circular:
                ApplyCircularLayout();
                break;
            case LayoutType.Grid:
                ApplyGridLayout();
                break;
            case LayoutType.Hierarchical:
                ApplyHierarchicalLayout();
                break;
        }
    }
    
    void ApplyForceDirectedLayout()
    {
        // Initialize random positions
        foreach (var nodeObj in nodeObjects.Values)
        {
            nodeObj.transform.position = Random.insideUnitSphere * 10f;
        }
        
        // Force-directed algorithm
        // NOTE: O(n²) complexity - for graphs with 1000+ nodes, consider:
        // 1. Reducing maxIterations
        // 2. Using spatial partitioning (octree/quadtree)
        // 3. Limiting force calculations to nearby nodes
        // 4. Using Grid or Hierarchical layout instead
        for (int iter = 0; iter < maxIterations; iter++)
        {
            Dictionary<string, Vector3> forces = new Dictionary<string, Vector3>();
            
            // Initialize forces
            foreach (string id in nodeObjects.Keys)
            {
                forces[id] = Vector3.zero;
            }
            
            // Repulsion between all nodes (O(n²) - expensive for large graphs)
            foreach (var kvp1 in nodeObjects)
            {
                foreach (var kvp2 in nodeObjects)
                {
                    if (kvp1.Key == kvp2.Key) continue;
                    
                    Vector3 delta = kvp1.Value.transform.position - kvp2.Value.transform.position;
                    float distance = delta.magnitude;
                    
                    if (distance > 0.1f)
                    {
                        forces[kvp1.Key] += delta.normalized * (repulsionStrength / (distance * distance));
                    }
                }
            }
            
            // Attraction for connected nodes
            foreach (EdgeData edge in edges)
            {
                if (nodeObjects.ContainsKey(edge.source) && nodeObjects.ContainsKey(edge.target))
                {
                    Vector3 delta = nodeObjects[edge.target].transform.position - 
                                  nodeObjects[edge.source].transform.position;
                    float distance = delta.magnitude;
                    
                    Vector3 force = delta.normalized * distance * springStrength;
                    forces[edge.source] += force;
                    forces[edge.target] -= force;
                }
            }
            
            // Apply forces with damping
            foreach (var kvp in nodeObjects)
            {
                Vector3 displacement = forces[kvp.Key] * damping;
                kvp.Value.transform.position += displacement;
            }
        }
        
        Debug.Log("Force-directed layout applied");
    }
    
    void ApplyCircularLayout()
    {
        int count = nodeObjects.Count;
        float radius = count * nodeSpacing / (2f * Mathf.PI);
        int index = 0;
        
        foreach (var nodeObj in nodeObjects.Values)
        {
            float angle = 2f * Mathf.PI * index / count;
            nodeObj.transform.position = new Vector3(
                Mathf.Cos(angle) * radius,
                0,
                Mathf.Sin(angle) * radius
            );
            index++;
        }
        
        Debug.Log("Circular layout applied");
    }
    
    void ApplyGridLayout()
    {
        int gridSize = Mathf.CeilToInt(Mathf.Sqrt(nodeObjects.Count));
        int index = 0;
        
        foreach (var nodeObj in nodeObjects.Values)
        {
            int x = index % gridSize;
            int z = index / gridSize;
            nodeObj.transform.position = new Vector3(x * nodeSpacing, 0, z * nodeSpacing);
            index++;
        }
        
        Debug.Log("Grid layout applied");
    }
    
    void ApplyHierarchicalLayout()
    {
        // Find root nodes (nodes with no incoming edges)
        HashSet<string> hasIncoming = new HashSet<string>();
        foreach (EdgeData edge in edges)
        {
            hasIncoming.Add(edge.target);
        }
        
        List<string> roots = nodeObjects.Keys.Where(id => !hasIncoming.Contains(id)).ToList();
        
        if (roots.Count == 0)
        {
            // Fallback to circular if no clear hierarchy
            ApplyCircularLayout();
            return;
        }
        
        // Position nodes by level
        Dictionary<string, int> levels = new Dictionary<string, int>();
        Queue<string> queue = new Queue<string>();
        
        foreach (string root in roots)
        {
            levels[root] = 0;
            queue.Enqueue(root);
        }
        
        while (queue.Count > 0)
        {
            string current = queue.Dequeue();
            int currentLevel = levels[current];
            
            foreach (EdgeData edge in edges.Where(e => e.source == current))
            {
                if (!levels.ContainsKey(edge.target))
                {
                    levels[edge.target] = currentLevel + 1;
                    queue.Enqueue(edge.target);
                }
            }
        }
        
        // Group nodes by level and position them
        var levelGroups = levels.GroupBy(kvp => kvp.Value);
        
        foreach (var group in levelGroups)
        {
            int level = group.Key;
            var nodesAtLevel = group.ToList();
            float y = -level * nodeSpacing;
            
            for (int i = 0; i < nodesAtLevel.Count; i++)
            {
                string nodeId = nodesAtLevel[i].Key;
                float x = (i - nodesAtLevel.Count / 2f) * nodeSpacing;
                nodeObjects[nodeId].transform.position = new Vector3(x, y, 0);
            }
        }
        
        Debug.Log("Hierarchical layout applied");
    }
    
    void CreateConnections()
    {
        foreach (var nodeObj in nodeObjects.Values)
        {
            SophiaGraphNode node = nodeObj.GetComponent<SophiaGraphNode>();
            if (node != null)
            {
                node.CreateConnections();
            }
        }
        
        Debug.Log("Connections created");
    }
    
    /// <summary>
    /// Get statistics about the loaded graph
    /// </summary>
    public void PrintStatistics()
    {
        Debug.Log($"=== SOPHIA MIND Graph Statistics ===");
        Debug.Log($"Total Nodes: {nodes.Count}");
        Debug.Log($"Total Edges: {edges.Count}");
        
        // Count glyphs
        Dictionary<string, int> glyphCounts = new Dictionary<string, int>();
        foreach (NodeData node in nodes)
        {
            foreach (string glyph in node.glyphs)
            {
                if (!glyphCounts.ContainsKey(glyph))
                    glyphCounts[glyph] = 0;
                glyphCounts[glyph]++;
            }
        }
        
        Debug.Log($"Glyph Distribution:");
        foreach (var kvp in glyphCounts.OrderByDescending(x => x.Value))
        {
            Debug.Log($"  {kvp.Key}: {kvp.Value} nodes");
        }
    }
}

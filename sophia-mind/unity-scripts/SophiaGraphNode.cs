using UnityEngine;
using System.Collections.Generic;

/// <summary>
/// SOPHIA MIND Brain Visualizer - Graph Node Component
/// Represents a single knowledge node in 3D space with FlameLang glyph support
/// 
/// Part of the Strategickhaos Sovereignty Architecture
/// Zero Vendor Lock-in | Own Your Knowledge
/// </summary>
public class SophiaGraphNode : MonoBehaviour
{
    [Header("Node Identity")]
    public string nodeId;
    public string title;
    public string filePath;
    
    [Header("FlameLang Integration")]
    public string[] glyphTags;
    public float frequency = 432f;  // Default: Coherence
    
    [Header("Connections")]
    public string[] connections;
    
    [Header("Visual Settings")]
    public float nodeScale = 1.0f;
    public bool showLabel = true;
    public float labelDistance = 2.0f;
    
    private Material nodeMaterial;
    private List<LineRenderer> connectionLines;
    private TextMesh labelText;
    private Color nodeColor;
    
    void Start()
    {
        // Initialize components
        connectionLines = new List<LineRenderer>();
        
        // Get renderer and material with null check
        Renderer renderer = GetComponent<Renderer>();
        if (renderer != null)
        {
            nodeMaterial = renderer.material;
            
            // Set color based on FlameLang frequency
            nodeColor = FrequencyToColor(frequency);
            nodeMaterial.color = nodeColor;
        }
        else
        {
            Debug.LogWarning($"Node {nodeId} has no Renderer component");
            nodeColor = Color.white;
        }
        
        // Create label
        if (showLabel)
        {
            CreateLabel();
        }
        
        // Scale the node
        transform.localScale = Vector3.one * nodeScale;
    }
    
    void Update()
    {
        // Rotate node slowly for visual effect
        transform.Rotate(Vector3.up, 10f * Time.deltaTime);
        
        // Update label to face camera
        if (labelText != null && Camera.main != null)
        {
            labelText.transform.LookAt(Camera.main.transform);
            labelText.transform.Rotate(0, 180, 0);
        }
    }
    
    /// <summary>
    /// Map Solfeggio frequencies to colors based on FlameLang specification
    /// </summary>
    Color FrequencyToColor(float freq)
    {
        // Solfeggio frequency color mapping
        if (freq >= 963) return new Color(1f, 0.84f, 0f);      // Gold - Oneness (AT1-AT3)
        if (freq >= 852) return new Color(0.58f, 0f, 0.83f);   // Purple - Intuition (LY1-LY3)
        if (freq >= 741) return new Color(0f, 0.5f, 1f);       // Blue - Expression (FB1-FB3)
        if (freq >= 639) return new Color(0f, 1f, 0.5f);       // Green - Connection (RC1-RC3)
        if (freq >= 528) return new Color(1f, 1f, 0f);         // Yellow - Transformation (FL1-FL3)
        if (freq >= 432) return new Color(1f, 0.5f, 0f);       // Orange - Coherence (AE1-AE3)
        
        return Color.white; // Fallback
    }
    
    /// <summary>
    /// Create connection lines to linked nodes
    /// Note: For large graphs, consider using SophiaGraphManager to create connections
    /// </summary>
    public void CreateConnections()
    {
        foreach (string targetId in connections)
        {
            GameObject targetNode = GameObject.Find(targetId);
            
            if (targetNode != null)
            {
                SophiaGraphNode targetNodeComponent = targetNode.GetComponent<SophiaGraphNode>();
                if (targetNodeComponent == null)
                {
                    Debug.LogWarning($"Target node {targetId} has no SophiaGraphNode component");
                    continue;
                }
                
                // Create line renderer for connection
                GameObject lineObj = new GameObject($"Connection_{nodeId}_to_{targetId}");
                lineObj.transform.parent = transform;
                
                LineRenderer lr = lineObj.AddComponent<LineRenderer>();
                lr.startWidth = 0.05f;
                lr.endWidth = 0.05f;
                lr.material = new Material(Shader.Find("Sprites/Default"));
                lr.startColor = nodeColor;
                lr.endColor = targetNodeComponent.nodeColor;
                
                // Set positions
                lr.SetPosition(0, transform.position);
                lr.SetPosition(1, targetNode.transform.position);
                
                connectionLines.Add(lr);
            }
        }
    }
    
    /// <summary>
    /// Create text label for node
    /// </summary>
    void CreateLabel()
    {
        GameObject labelObj = new GameObject($"Label_{nodeId}");
        labelObj.transform.parent = transform;
        labelObj.transform.localPosition = Vector3.up * labelDistance;
        
        labelText = labelObj.AddComponent<TextMesh>();
        labelText.text = title;
        labelText.fontSize = 24;
        labelText.color = Color.white;
        labelText.anchor = TextAnchor.MiddleCenter;
        labelText.alignment = TextAlignment.Center;
        labelText.characterSize = 0.1f;
    }
    
    /// <summary>
    /// Update connection line endpoints (call when nodes move)
    /// </summary>
    public void UpdateConnections()
    {
        foreach (LineRenderer lr in connectionLines)
        {
            if (lr != null)
            {
                lr.SetPosition(0, transform.position);
            }
        }
    }
    
    /// <summary>
    /// Get node information as JSON-compatible dictionary
    /// </summary>
    public Dictionary<string, object> GetNodeInfo()
    {
        return new Dictionary<string, object>
        {
            { "id", nodeId },
            { "title", title },
            { "glyphs", glyphTags },
            { "frequency", frequency },
            { "position", transform.position },
            { "connection_count", connections.Length }
        };
    }
    
    void OnMouseDown()
    {
        // Node clicked - could open file, show details, etc.
        Debug.Log($"Clicked node: {title} (ID: {nodeId})");
        Debug.Log($"Glyphs: {string.Join(", ", glyphTags)}");
        Debug.Log($"Frequency: {frequency}Hz");
        Debug.Log($"Connections: {connections.Length}");
    }
    
    void OnMouseEnter()
    {
        // Highlight on hover
        if (nodeMaterial != null)
        {
            nodeMaterial.color = Color.Lerp(nodeColor, Color.white, 0.5f);
        }
    }
    
    void OnMouseExit()
    {
        // Restore original color
        if (nodeMaterial != null)
        {
            nodeMaterial.color = nodeColor;
        }
    }
}

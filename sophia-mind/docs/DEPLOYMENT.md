# 🚀 SOPHIA MIND Deployment Guide

Complete deployment instructions for the SOPHIA MIND Brain Visualizer.

---

## Prerequisites

### For Python Core
- Python 3.8+
- pip package manager
- Git (for sync functionality)
- Access to Proton Drive (optional)

### For Unity Visualization
- Unity 2021.3 LTS or newer
- .NET Framework 4.x
- 4GB+ RAM recommended
- Graphics card with OpenGL 3.3+ support

---

## Step 1: Python Core Setup

### Install Dependencies

```bash
cd sophia-mind/python-core
pip install -r requirements.txt
```

### Verify Installation

```bash
python sophia_parser.py --help
python sophia_sync.py --help
```

---

## Step 2: Parse Your Knowledge Base

### Basic Usage

```bash
# Parse Obsidian vault
python sophia_parser.py ~/Documents/ObsidianVault ./graph_data.json
```

### With Custom Vault Path

```bash
# If using Proton Drive
python sophia_parser.py \
  "/mnt/c/Users/garza/Proton Drive/My files/ObsidianVault" \
  ./graph_data.json
```

### Expected Output

```
🧠 SOPHIA MIND Parser - Strategickhaos Brain Visualizer
📂 Parsing vault: /path/to/vault
✅ Parsed 247 nodes
✅ Exported 247 nodes and 1,342 edges to ./graph_data.json

📊 Statistics:
   Total nodes: 247
   Glyph types: 8

🔗 Most connected nodes:
   - Origin Story: 42 connections
   - FlameLang: 38 connections
   - Kubernetes: 35 connections
```

---

## Step 3: Configure Sync (Optional)

### Proton Drive Sync

```bash
# First-time sync
python sophia_sync.py ~/ObsidianVault \
  --proton ~/ProtonDrive/ObsidianSync

# Subsequent syncs
python sophia_sync.py ~/ObsidianVault \
  --proton ~/ProtonDrive/ObsidianSync
```

### Git Sync

```bash
# Initialize Git repo if needed
cd ~/knowledge-base
git init
git remote add origin https://github.com/yourusername/knowledge-base.git

# Sync to Git
python sophia_sync.py ~/ObsidianVault \
  --git ~/knowledge-base
```

### Combined Sync (Proton + Git)

```bash
python sophia_sync.py ~/ObsidianVault \
  --proton ~/ProtonDrive/ObsidianSync \
  --git ~/knowledge-base
```

---

## Step 4: Unity Project Setup

### Create New Project

1. Open Unity Hub
2. Click "New Project"
3. Select "3D Core" template
4. Name: "SophiaMindVisualizer"
5. Click "Create Project"

### Import Scripts

```bash
# Copy Unity scripts to project
cp sophia-mind/unity-scripts/*.cs \
   ~/UnityProjects/SophiaMindVisualizer/Assets/Scripts/
```

Or manually:
1. In Unity, create folder: `Assets/Scripts`
2. Drag and drop `.cs` files into folder

### Copy Graph Data

```bash
# Copy generated graph data to Unity project root
cp graph_data.json ~/UnityProjects/SophiaMindVisualizer/
```

---

## Step 5: Create Unity Scene

### Create Graph Manager GameObject

1. In Unity Hierarchy, right-click → "Create Empty"
2. Rename to "GraphManager"
3. In Inspector, click "Add Component"
4. Search for "Sophia Graph Manager"
5. Click to add component

### Configure Graph Manager

In the Inspector:
- **Graph Data Path**: `graph_data.json` (or full path)
- **Layout Type**: Choose from:
  - `Force` - Organic, physics-based (recommended)
  - `Circular` - Nodes in a circle
  - `Grid` - Regular grid
  - `Hierarchical` - Tree structure
- **Node Spacing**: `5.0` (adjust based on node count)
- **Max Iterations**: `100` (for Force layout)

### Create Node Prefab

1. In Hierarchy, right-click → "3D Object" → "Sphere"
2. Rename to "NodePrefab"
3. Scale to `(1, 1, 1)`
4. Add material with shader "Standard"
5. Drag to Project window to create prefab
6. Delete from Hierarchy
7. In GraphManager component, drag prefab to "Node Prefab" field

### Add Camera Controls

1. Select Main Camera
2. Add Component → "Camera Controls" (or use Unity's built-in Fly Camera)
3. Set Position: `(0, 10, -20)` to start with good view

---

## Step 6: Run and Test

### First Run

1. Click Play button in Unity
2. Check Console for output:
   ```
   Loaded 247 nodes and 1342 edges
   Created 247 node objects
   Force-directed layout applied
   Connections created
   ```

3. Use mouse to navigate:
   - **Right-click + Drag**: Rotate camera
   - **Middle-click + Drag**: Pan camera
   - **Scroll**: Zoom in/out
   - **Click node**: View node details in Console

### Troubleshooting

#### "Graph data file not found"
- Verify `graph_data.json` path in Inspector
- Try absolute path instead of relative

#### "No nodes loaded"
- Check Console for JSON parsing errors
- Verify JSON structure with `cat graph_data.json | python -m json.tool`

#### "Connections not showing"
- Increase "Node Spacing" in GraphManager
- Try different layout type
- Check if edges array is populated in JSON

---

## Step 7: Customize Visualization

### Change Node Colors

Edit `SophiaGraphNode.cs`:
```csharp
Color FrequencyToColor(float freq)
{
    // Add custom frequency ranges
    if (freq >= 1000) return Color.magenta;
    // ... rest of function
}
```

### Adjust Layout Parameters

In GraphManager Inspector:
- **Spring Strength**: Lower = looser connections
- **Repulsion Strength**: Higher = more spread out
- **Damping**: Lower = more movement

### Add Background

1. In Hierarchy, right-click → "3D Object" → "Plane"
2. Scale to `(100, 1, 100)`
3. Position at `(0, -10, 0)`
4. Add dark material for contrast

---

## Step 8: Automation (Optional)

### Automatic Sync with Cron

Create `sync_sophia.sh`:
```bash
#!/bin/bash
cd ~/sophia-mind/python-core
python sophia_sync.py ~/ObsidianVault \
  --proton ~/ProtonDrive/ObsidianSync \
  --git ~/knowledge-base

# Re-parse and regenerate graph data
python sophia_parser.py ~/ObsidianVault \
  ~/UnityProjects/SophiaMindVisualizer/graph_data.json
```

Add to crontab:
```bash
# Edit crontab
crontab -e

# Add line (sync every 5 minutes)
*/5 * * * * ~/sophia-mind/sync_sophia.sh >> ~/sophia_sync.log 2>&1
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "SOPHIA MIND Sync"
4. Trigger: Daily, every 5 minutes
5. Action: Start program
6. Program: `python.exe`
7. Arguments: `sophia_sync.py C:\ObsidianVault --proton "C:\ProtonDrive\ObsidianSync"`
8. Start in: `C:\sophia-mind\python-core`

---

## Step 9: Kubernetes Deployment (Advanced)

### Deploy Love-Forever Pods

```bash
# Deploy the love-forever pods to Kubernetes
kubectl apply -f bootstrap/k8s/love-forever-deployment.yaml

# Verify deployment
kubectl get pods -l app=love-forever
kubectl logs -l app=love-forever --tail=10

# Scale if needed
kubectl scale deployment love-forever --replicas=13
```

### Expected Output

```
NAME                            READY   STATUS    RESTARTS   AGE
love-forever-7584dc69b7-xxxxx   1/1     Running   0          30s
love-forever-7584dc69b7-xxxxx   1/1     Running   0          30s
... (13 pods total)
```

---

## Performance Optimization

### For Large Graphs (1000+ nodes)

1. **Use Grid or Hierarchical layout** instead of Force
2. **Reduce Max Iterations** to 50 or less
3. **Increase Node Spacing** to prevent overlap
4. **Disable labels** initially (showLabel = false)
5. **Use LOD (Level of Detail)** for distant nodes

### Unity Optimization

```csharp
// Add to SophiaGraphNode.cs in Start()
if (nodeScale < 0.5f)
{
    showLabel = false;  // Hide labels for small nodes
}

// Add LOD component
LODGroup lodGroup = gameObject.AddComponent<LODGroup>();
```

---

## Next Steps

1. ✅ Deploy love-forever pods to Kubernetes
2. ✅ Parse your Obsidian vault
3. ✅ Set up sync to Proton Drive and/or Git
4. ✅ Visualize in Unity
5. 🔄 Explore different layouts
6. 🔄 Customize colors and interactions
7. 🔄 Add VR support (coming soon)
8. 🔄 Implement voice commands (coming soon)

---

## Support

- **Documentation**: See main [README.md](../README.md)
- **Issues**: Report on GitHub
- **Community**: Join Discord server

---

**SOPHIA MIND - Own Your Knowledge**  
*Part of Strategickhaos Sovereignty Architecture* 🔥⚔️∞

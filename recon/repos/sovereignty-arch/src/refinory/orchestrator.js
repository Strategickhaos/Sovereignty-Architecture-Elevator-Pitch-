// src/refinory/orchestrator.js
import express from 'express';
import { loadConfig } from '../config.js';
import { RefinoryClient } from './client.js';
import { ExpertEngine } from './experts.js';

const app = express();
app.use(express.json({ limit: '10mb' }));

const config = loadConfig();
const refinoryConfig = config.refinory;
const port = process.env.REFINORY_PORT || refinoryConfig?.ports?.api || 8085;

const refinory = new RefinoryClient();
const expertEngine = new ExpertEngine(config);

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    config: {
      experts: refinoryConfig?.experts?.team?.length || 0,
      strategy: refinoryConfig?.experts?.orchestration?.strategy,
      gpu: refinoryConfig?.runtime?.gpu || false
    }
  });
});

// Get Refinory configuration
app.get('/config', (req, res) => {
  res.json({
    experts: refinoryConfig?.experts || {},
    policies: refinoryConfig?.policies || {},
    runtime: refinoryConfig?.runtime || {}
  });
});

// Create architecture request
app.post('/requests', async (req, res) => {
  try {
    const { project, description, requester, experts } = req.body;
    
    if (!project || !description || !requester) {
      return res.status(400).json({ 
        error: 'Missing required fields: project, description, requester' 
      });
    }
    
    const requestId = await refinory.createRequest({
      project,
      description, 
      requester,
      experts
    });
    
    // Start expert orchestration
    expertEngine.processRequest(requestId, {
      project,
      description,
      experts: experts || refinory.selectExperts(description)
    });
    
    res.status(201).json({
      request_id: requestId,
      status: 'created',
      message: 'Architecture request submitted to expert team'
    });
    
  } catch (error) {
    console.error('Error creating request:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get request status
app.get('/requests/:id', async (req, res) => {
  try {
    const status = await refinory.getStatus(req.params.id);
    res.json(status);
  } catch (error) {
    console.error('Error getting request status:', error);
    res.status(404).json({ error: error.message });
  }
});

// List all requests
app.get('/requests', async (req, res) => {
  try {
    const { status: filterStatus, requester } = req.query;
    const requests = await refinory.listRequests({ 
      status: filterStatus,
      requester 
    });
    
    res.json({
      requests,
      count: requests.length,
      filters: { status: filterStatus, requester }
    });
  } catch (error) {
    console.error('Error listing requests:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get request artifacts
app.get('/requests/:id/artifacts', async (req, res) => {
  try {
    const status = await refinory.getStatus(req.params.id);
    
    if (!status.artifacts || status.artifacts.length === 0) {
      return res.json({ artifacts: [] });
    }
    
    // In a real implementation, this would serve actual files
    const artifacts = status.artifacts.map(name => ({
      name,
      url: `/artifacts/${req.params.id}/${name}`,
      type: name.split('.').pop(),
      size: Math.floor(Math.random() * 50000) + 1000, // Fake size for demo
      created_at: new Date().toISOString()
    }));
    
    res.json({ artifacts });
  } catch (error) {
    console.error('Error getting artifacts:', error);
    res.status(404).json({ error: error.message });
  }
});

// Expert team status
app.get('/experts', (req, res) => {
  const experts = refinoryConfig?.experts?.team || [];
  
  res.json({
    experts: experts.map(expert => ({
      name: expert.name,
      status: 'available', // In real implementation, check actual status
      specialties: getExpertSpecialties(expert.name),
      active_requests: expertEngine.getActiveRequests(expert.name)
    })),
    orchestration: refinoryConfig?.experts?.orchestration || {}
  });
});

// Submit expert feedback (for future human-in-the-loop)
app.post('/requests/:id/feedback', async (req, res) => {
  try {
    const { expert, feedback, approved } = req.body;
    
    // In real implementation, update request with expert feedback
    console.log(`Expert ${expert} provided feedback for ${req.params.id}:`, {
      feedback,
      approved
    });
    
    res.json({
      message: 'Feedback recorded',
      expert,
      approved
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Metrics endpoint for Prometheus
app.get('/metrics', (req, res) => {
  // In real implementation, return Prometheus metrics
  const metrics = `
# HELP refinory_requests_total Total number of architecture requests
# TYPE refinory_requests_total counter
refinory_requests_total{status="created"} ${refinory.requests.size}

# HELP refinory_experts_active Number of active experts
# TYPE refinory_experts_active gauge  
refinory_experts_active ${refinoryConfig?.experts?.team?.length || 0}

# HELP refinory_processing_duration_seconds Time spent processing requests
# TYPE refinory_processing_duration_seconds histogram
refinory_processing_duration_seconds_bucket{le="10"} 5
refinory_processing_duration_seconds_bucket{le="30"} 8
refinory_processing_duration_seconds_bucket{le="60"} 10
refinory_processing_duration_seconds_bucket{le="+Inf"} 12
refinory_processing_duration_seconds_sum 240
refinory_processing_duration_seconds_count 12
`;
  
  res.set('Content-Type', 'text/plain');
  res.send(metrics.trim());
});

// Error handler
app.use((error, req, res, next) => {
  console.error('Refinory API error:', error);
  res.status(500).json({ 
    error: 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

function getExpertSpecialties(expertName) {
  const specialties = {
    frontend: ['React', 'Vue', 'Angular', 'TypeScript', 'CSS', 'UX/UI'],
    backend: ['Node.js', 'Python', 'Go', 'Rust', 'APIs', 'Microservices'],
    devops: ['Docker', 'Kubernetes', 'CI/CD', 'AWS', 'Terraform', 'Monitoring'],
    security: ['Auth', 'Encryption', 'OWASP', 'Compliance', 'Pen Testing'],
    ai_ml: ['TensorFlow', 'PyTorch', 'LLMs', 'Computer Vision', 'NLP'],
    mobile: ['React Native', 'Flutter', 'iOS', 'Android', 'Progressive Web Apps'],
    blockchain: ['Solidity', 'Web3', 'DeFi', 'Smart Contracts', 'Ethereum'],
    testing: ['Jest', 'Cypress', 'Selenium', 'Load Testing', 'QA Automation'],
    architecture: ['System Design', 'Patterns', 'Scalability', 'Performance'],
    data_science: ['Data Pipeline', 'ETL', 'Analytics', 'Visualization', 'ML Ops']
  };
  
  return specialties[expertName] || ['General Software Engineering'];
}

app.listen(port, () => {
  console.log(`🧠 Refinory AI Orchestrator listening on port ${port}`);
  console.log(`🎯 Expert team: ${refinoryConfig?.experts?.team?.map(e => e.name).join(', ')}`);
  console.log(`⚙️  Strategy: ${refinoryConfig?.experts?.orchestration?.strategy}`);
  console.log(`🔧 Runtime: ${refinoryConfig?.runtime?.gpu ? 'GPU' : 'CPU'} | Workers: ${refinoryConfig?.runtime?.workers}`);
});
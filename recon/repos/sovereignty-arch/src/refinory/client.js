// src/refinory/client.js
import { v4 as uuid } from 'uuid';
import axios from 'axios';
import { loadConfig } from '../config.js';

export class RefinoryClient {
  constructor() {
    this.config = loadConfig();
    this.baseUrl = `http://localhost:${this.config.refinory?.ports?.api || 8085}`;
    this.requests = new Map(); // In-memory storage for dev
  }

  async createRequest({ project, description, requester, experts = null }) {
    const requestId = uuid();
    const timestamp = new Date().toISOString();
    
    const request = {
      id: requestId,
      project,
      description,
      requester,
      experts: experts || this.selectExperts(description),
      status: 'created',
      progress: 0,
      created_at: timestamp,
      updated_at: timestamp,
      artifacts: [],
      active_experts: []
    };
    
    this.requests.set(requestId, request);
    
    // Simulate async processing start
    this.processRequest(requestId);
    
    return requestId;
  }

  async getStatus(requestId) {
    const request = this.requests.get(requestId);
    if (!request) {
      throw new Error(`Request ${requestId} not found`);
    }
    
    return request;
  }

  async listRequests(filter = {}) {
    const requests = Array.from(this.requests.values());
    
    if (filter.status) {
      return requests.filter(r => r.status === filter.status);
    }
    
    return requests;
  }

  selectExperts(description) {
    const allExperts = this.config.refinory?.experts?.team || [];
    const keywords = {
      frontend: ['ui', 'react', 'vue', 'angular', 'web', 'interface'],
      backend: ['api', 'server', 'database', 'service', 'microservice'],
      devops: ['deploy', 'docker', 'kubernetes', 'ci/cd', 'infrastructure'],
      security: ['auth', 'security', 'encryption', 'vulnerability', 'compliance'],
      ai_ml: ['ai', 'ml', 'machine learning', 'neural', 'model', 'training'],
      mobile: ['mobile', 'ios', 'android', 'react native', 'flutter'],
      blockchain: ['blockchain', 'crypto', 'smart contract', 'web3', 'defi'],
      testing: ['test', 'qa', 'quality', 'automation', 'junit'],
      architecture: ['architecture', 'design', 'pattern', 'system'],
      data_science: ['data', 'analytics', 'visualization', 'etl', 'pipeline']
    };
    
    const text = description.toLowerCase();
    const selectedExperts = [];
    
    for (const [expert, terms] of Object.entries(keywords)) {
      if (terms.some(term => text.includes(term))) {
        const expertConfig = allExperts.find(e => e.name === expert);
        if (expertConfig) {
          selectedExperts.push(expert);
        }
      }
    }
    
    // Always include architecture for coordination
    if (!selectedExperts.includes('architecture')) {
      selectedExperts.push('architecture');
    }
    
    return selectedExperts.slice(0, 5); // Limit to 5 experts
  }

  async processRequest(requestId) {
    const request = this.requests.get(requestId);
    if (!request) return;
    
    // Simulate expert activation and progress
    setTimeout(() => {
      request.status = 'analyzing';
      request.progress = 25;
      request.active_experts = request.experts.slice(0, 2);
      request.updated_at = new Date().toISOString();
    }, 2000);
    
    setTimeout(() => {
      request.status = 'architecting';
      request.progress = 50;
      request.active_experts = request.experts;
      request.artifacts.push('architecture_diagram.png', 'technical_spec.md');
      request.updated_at = new Date().toISOString();
    }, 5000);
    
    setTimeout(() => {
      request.status = 'implementing';
      request.progress = 75;
      request.artifacts.push('docker-compose.yml', 'src/main.py', 'README.md');
      request.updated_at = new Date().toISOString();
    }, 8000);
    
    setTimeout(() => {
      request.status = 'completed';
      request.progress = 100;
      request.active_experts = [];
      request.artifacts.push('deployment_guide.md', 'test_suite.py');
      request.updated_at = new Date().toISOString();
    }, 12000);
  }
}

export default RefinoryClient;
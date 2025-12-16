# Swarm Module - GitHub Issue as Distress Signal

## Purpose
This module treats GitHub Issues not as tickets, but as **distress signals** that automatically deploy the most relevant AI agent to fix them.

## Biological Analogy

In a bee swarm or ant colony, when a threat is detected:
1. Scout sends distress pheromones
2. Nearby workers detect the signal
3. Appropriate responders (soldiers, foragers) mobilize
4. Colony responds collectively

Similarly, when a GitHub Issue is created:
1. Issue = Distress signal
2. AI agents detect and analyze
3. Most relevant agent deploys
4. Legion responds collectively

## Architecture

```rust
pub struct SwarmDispatcher {
    issue_monitor: GitHubIssueMonitor,
    agent_selector: AgentSelector,
    response_coordinator: ResponseCoordinator,
    legion: Vec<Box<dyn SwarmAgent>>
}

impl SwarmDispatcher {
    
    /// Monitor GitHub Issues continuously
    pub async fn monitor_issues(&mut self) -> Result<()> {
        loop {
            // Poll for new issues
            let new_issues = self.issue_monitor.poll().await?;
            
            for issue in new_issues {
                // Treat as distress signal
                let distress = DistressSignal::from_issue(issue);
                
                // Dispatch to swarm
                self.handle_distress(distress).await?;
            }
            
            tokio::time::sleep(Duration::from_secs(30)).await;
        }
    }
    
    /// Handle a distress signal
    async fn handle_distress(&self, signal: DistressSignal) -> Result<()> {
        log::info!("🚨 Distress signal detected: {}", signal.title);
        
        // 1. Analyze signal
        let analysis = self.analyze_distress(&signal).await?;
        
        // 2. Select best agent(s)
        let agents = self.agent_selector.select_agents(&analysis);
        
        // 3. Coordinate response
        let response = self.response_coordinator.coordinate(agents, signal).await?;
        
        // 4. Apply fix
        self.apply_response(response).await?;
        
        Ok(())
    }
}
```

## Distress Signal Classification

```rust
enum DistressType {
    /// Bug in production - HIGH PRIORITY
    ProductionBug {
        severity: Severity,
        affected_users: u64
    },
    
    /// Security vulnerability - CRITICAL
    SecurityVulnerability {
        cvss_score: f64,
        exploit_public: bool
    },
    
    /// Feature request - NORMAL
    FeatureRequest {
        complexity: Complexity,
        business_value: f64
    },
    
    /// Documentation gap - LOW
    DocumentationGap {
        area: String
    },
    
    /// Performance degradation - HIGH
    PerformanceDegradation {
        latency_increase: f64,
        throughput_decrease: f64
    },
    
    /// Technical debt - NORMAL
    TechnicalDebt {
        entropy_increase: f64
    }
}

fn classify_distress(issue: &GitHubIssue) -> DistressType {
    // Use AI to classify the issue
    let classification = ai_classify(issue).await?;
    
    // Extract severity from labels
    let severity = if issue.labels.contains("critical") {
        Severity::Critical
    } else if issue.labels.contains("high") {
        Severity::High
    } else {
        Severity::Normal
    };
    
    match classification {
        "bug" => DistressType::ProductionBug { severity, affected_users: 0 },
        "security" => DistressType::SecurityVulnerability { cvss_score: 0.0, exploit_public: false },
        // ... other classifications
    }
}
```

## Agent Selection

```rust
trait SwarmAgent {
    fn name(&self) -> &str;
    fn specialization(&self) -> Vec<String>;
    fn can_handle(&self, signal: &DistressSignal) -> f64;  // 0.0 - 1.0 confidence
    async fn respond(&self, signal: DistressSignal) -> Result<Response>;
}

/// Select the best agent(s) for a distress signal
struct AgentSelector {
    agents: Vec<Box<dyn SwarmAgent>>
}

impl AgentSelector {
    fn select_agents(&self, analysis: &DistressAnalysis) -> Vec<&dyn SwarmAgent> {
        let mut candidates: Vec<_> = self.agents.iter()
            .map(|agent| {
                let confidence = agent.can_handle(&analysis.signal);
                (agent.as_ref(), confidence)
            })
            .collect();
        
        // Sort by confidence
        candidates.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        
        // Take top 3 agents or all with confidence > 0.5
        candidates.iter()
            .take(3)
            .filter(|(_, confidence)| *confidence > 0.5)
            .map(|(agent, _)| *agent)
            .collect()
    }
}
```

## Swarm Agents

### 1. Bug Hunter Agent
```rust
struct BugHunterAgent {
    name: String,
    claude: ClaudeAPI
}

impl SwarmAgent for BugHunterAgent {
    fn name(&self) -> &str { "Bug Hunter" }
    
    fn specialization(&self) -> Vec<String> {
        vec!["debugging", "error_analysis", "root_cause"]
    }
    
    fn can_handle(&self, signal: &DistressSignal) -> f64 {
        match signal.distress_type {
            DistressType::ProductionBug { .. } => 0.9,
            _ => 0.2
        }
    }
    
    async fn respond(&self, signal: DistressSignal) -> Result<Response> {
        // 1. Analyze the bug
        let analysis = self.claude.analyze_bug(&signal).await?;
        
        // 2. Search codebase for root cause
        let root_cause = search_code(&analysis.likely_location).await?;
        
        // 3. Generate fix
        let fix = self.claude.generate_fix(&root_cause).await?;
        
        // 4. Validate fix
        let validation = validate_fix(&fix).await?;
        
        Ok(Response::BugFix {
            analysis,
            fix,
            validation
        })
    }
}
```

### 2. Security Agent
```rust
struct SecurityAgent {
    name: String,
    scanner: VulnerabilityScanner
}

impl SwarmAgent for SecurityAgent {
    fn name(&self) -> &str { "Security Sentinel" }
    
    fn specialization(&self) -> Vec<String> {
        vec!["security", "vulnerabilities", "exploits"]
    }
    
    fn can_handle(&self, signal: &DistressSignal) -> f64 {
        match signal.distress_type {
            DistressType::SecurityVulnerability { .. } => 1.0,
            _ => 0.1
        }
    }
    
    async fn respond(&self, signal: DistressSignal) -> Result<Response> {
        // 1. Scan for vulnerability
        let vuln = self.scanner.scan(&signal).await?;
        
        // 2. Assess severity
        let severity = assess_severity(&vuln).await?;
        
        // 3. Generate patch
        let patch = generate_security_patch(&vuln).await?;
        
        // 4. Test patch
        let test_result = test_patch(&patch).await?;
        
        Ok(Response::SecurityPatch {
            vulnerability: vuln,
            severity,
            patch,
            test_result
        })
    }
}
```

### 3. Documentation Agent
```rust
struct DocumentationAgent {
    name: String,
    grok: GrokAPI
}

impl SwarmAgent for DocumentationAgent {
    fn name(&self) -> &str { "Doc Writer" }
    
    fn specialization(&self) -> Vec<String> {
        vec!["documentation", "tutorials", "examples"]
    }
    
    fn can_handle(&self, signal: &DistressSignal) -> f64 {
        match signal.distress_type {
            DistressType::DocumentationGap { .. } => 0.95,
            _ => 0.15
        }
    }
    
    async fn respond(&self, signal: DistressSignal) -> Result<Response> {
        // 1. Understand what needs documentation
        let topic = extract_topic(&signal).await?;
        
        // 2. Generate documentation
        let docs = self.grok.generate_docs(&topic).await?;
        
        // 3. Link to knowledge base
        let links = link_to_obsidian(&docs).await?;
        
        Ok(Response::Documentation {
            topic,
            content: docs,
            links
        })
    }
}
```

## Response Coordination

```rust
struct ResponseCoordinator;

impl ResponseCoordinator {
    async fn coordinate(
        &self,
        agents: Vec<&dyn SwarmAgent>,
        signal: DistressSignal
    ) -> Result<CoordinatedResponse> {
        
        // Get responses from all selected agents in parallel
        let futures: Vec<_> = agents.iter()
            .map(|agent| agent.respond(signal.clone()))
            .collect();
        
        let responses = join_all(futures).await;
        
        // Synthesize responses if multiple agents responded
        let synthesized = if responses.len() > 1 {
            self.synthesize_responses(responses).await?
        } else {
            responses[0].clone()
        };
        
        // Validate with Legion of Minds
        let validation = validate_response_with_legion(&synthesized).await?;
        
        Ok(CoordinatedResponse {
            responses,
            synthesized,
            validation
        })
    }
}
```

## Automated PR Creation

```rust
async fn apply_response(response: CoordinatedResponse) -> Result<()> {
    // 1. Create branch
    let branch_name = format!("swarm-fix-{}", response.issue_id);
    git_create_branch(&branch_name)?;
    
    // 2. Apply changes
    apply_code_changes(&response.changes)?;
    
    // 3. Run tests
    let test_results = run_tests().await?;
    
    if !test_results.passed() {
        return Err("Tests failed".into());
    }
    
    // 4. Commit and push
    git_commit(&format!("🤖 Swarm response: {}", response.summary))?;
    git_push(&branch_name)?;
    
    // 5. Create PR
    let pr = github::create_pr(CreatePRRequest {
        title: format!("🐝 Swarm Fix: {}", response.title),
        body: response.detailed_explanation,
        branch: branch_name,
        labels: vec!["swarm-generated", "automated-fix"]
    }).await?;
    
    log::info!("✅ Created PR #{} for issue #{}", pr.number, response.issue_id);
    
    Ok(())
}
```

## Example Flow

```
1. GitHub Issue Created:
   Title: "API endpoint /users returns 500 error"
   Labels: ["bug", "high"]

2. Swarm Detects Distress:
   🚨 Distress signal detected
   Type: ProductionBug
   Severity: High

3. Agent Selection:
   Selected: Bug Hunter (0.9 confidence)
   Selected: Security Agent (0.4 confidence)

4. Agents Respond:
   Bug Hunter: "Found null pointer dereference in user_service.rs:42"
   Security Agent: "No security implications detected"

5. Response Synthesis:
   Fix: Add null check before dereferencing
   Tests: Added unit test for null case
   
6. PR Created:
   PR #123: "🐝 Swarm Fix: Add null check in user_service"
   Status: ✅ All checks passed

7. Human Review:
   Domenic reviews and merges PR
   Issue automatically closed
```

## Metrics

```rust
struct SwarmMetrics {
    distress_signals_detected: u64,
    responses_generated: u64,
    prs_created: u64,
    prs_merged: u64,
    
    // Response times
    avg_detection_latency: Duration,
    avg_response_latency: Duration,
    avg_fix_latency: Duration,
    
    // Quality metrics
    success_rate: f64,  // Fixes that actually worked
    false_positive_rate: f64
}
```

This creates a **self-healing system** where problems are automatically detected and resolved by the appropriate AI agents.

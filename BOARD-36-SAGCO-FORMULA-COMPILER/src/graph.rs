use std::collections::{HashMap, HashSet, VecDeque};

/// Dependency graph for cells — used for topological ordering
pub struct DependencyGraph {
    /// edges: addr -> list of addrs it depends on
    pub deps: HashMap<String, Vec<String>>,
}

impl DependencyGraph {
    pub fn new() -> Self {
        DependencyGraph {
            deps: HashMap::new(),
        }
    }

    pub fn set_deps(&mut self, addr: &str, deps: Vec<String>) {
        self.deps.insert(addr.to_string(), deps);
    }

    /// Kahn's topological sort. Returns ordered list or Err("#CIRCULAR!") on cycle.
    pub fn topo_sort(&self) -> Result<Vec<String>, String> {
        // Build in-degree map and adjacency (who depends on whom -> reverse)
        let all_nodes: HashSet<&String> = self
            .deps
            .keys()
            .chain(self.deps.values().flatten())
            .collect();

        let mut in_degree: HashMap<String, usize> = HashMap::new();
        // dependents[b] = list of nodes that depend on b
        let mut dependents: HashMap<String, Vec<String>> = HashMap::new();

        for node in &all_nodes {
            in_degree.entry((*node).clone()).or_insert(0);
            dependents.entry((*node).clone()).or_insert_with(Vec::new);
        }

        for (node, deps) in &self.deps {
            for dep in deps {
                *in_degree.entry(node.clone()).or_insert(0) += 1;
                dependents.entry(dep.clone()).or_insert_with(Vec::new).push(node.clone());
            }
        }

        let mut queue: VecDeque<String> = in_degree
            .iter()
            .filter(|(_, &deg)| deg == 0)
            .map(|(k, _)| k.clone())
            .collect();

        // Sort for determinism
        let mut sorted_queue: Vec<String> = queue.drain(..).collect();
        sorted_queue.sort();
        let mut queue: VecDeque<String> = sorted_queue.into();

        let mut order = Vec::new();

        while let Some(node) = queue.pop_front() {
            order.push(node.clone());
            if let Some(deps_list) = dependents.get(&node) {
                let mut next: Vec<String> = Vec::new();
                for dep_node in deps_list {
                    let deg = in_degree.get_mut(dep_node).unwrap();
                    *deg -= 1;
                    if *deg == 0 {
                        next.push(dep_node.clone());
                    }
                }
                next.sort();
                for n in next {
                    queue.push_back(n);
                }
            }
        }

        if order.len() == all_nodes.len() {
            Ok(order)
        } else {
            Err("#CIRCULAR!".to_string())
        }
    }
}

impl Default for DependencyGraph {
    fn default() -> Self {
        Self::new()
    }
}

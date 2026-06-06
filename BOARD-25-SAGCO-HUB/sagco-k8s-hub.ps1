##############################################################################
#  SAGCO K8s Hub Deployer
#  Paste in Admin PowerShell — deploys all SAGCO namespaces, ConfigMaps,
#  Secrets template, PVCs, Deployments, Services, NetworkPolicies,
#  ResourceQuotas, and PodDisruptionBudgets to the local Kubernetes cluster.
#
#  Cluster: kubernetes / 10.96.0.1:443 (Docker Desktop K8s)
##############################################################################

$WORLD    = "E:\SAGCO-WORLD"
$REPO     = "$WORLD\Sovereignty-Architecture-Elevator-Pitch-"
$K8S_DIR  = "$REPO\BOARD-25-SAGCO-HUB\k8s"
$AGENTS   = "$REPO\sagco-agents"

Write-Host "`n╔═══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  SAGCO K8s Hub Deployer                               ║" -ForegroundColor Cyan
Write-Host "║  Cluster: kubernetes / 10.96.0.1:443                  ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# ── Preflight ─────────────────────────────────────────────────────────────────
Write-Host "  [PREFLIGHT] Checking kubectl..." -ForegroundColor Yellow
kubectl cluster-info 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: kubectl cannot reach cluster. Enable Kubernetes in Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Cluster reachable`n" -ForegroundColor Green

# ── Step 1: Namespaces ────────────────────────────────────────────────────────
Write-Host "  [1/7] Applying namespaces..." -ForegroundColor Yellow
kubectl apply -f "$K8S_DIR\00-namespaces.yaml"
Write-Host "  ✓ Namespaces: sagco-genesis, sagco-eru, sagco-trinity, sagco-industrial, sagco-frequency`n" -ForegroundColor Green

# ── Step 2: ConfigMaps ────────────────────────────────────────────────────────
Write-Host "  [2/7] Applying ConfigMaps..." -ForegroundColor Yellow
kubectl apply -f "$K8S_DIR\01-configmap-sagco.yaml"
Write-Host "  ✓ ConfigMaps: sagco-os-config, sagco-daemon-config, sagco-mcp-config, sagco-eru-config`n" -ForegroundColor Green

# ── Step 3: Secrets (template — skip if values not filled) ───────────────────
Write-Host "  [3/7] Secrets check..." -ForegroundColor Yellow
$secretsFile = "$K8S_DIR\02-secrets-template.yaml"
$secretsContent = Get-Content $secretsFile -Raw
if ($secretsContent -match '<base64_encoded_value>') {
    Write-Host "  ⚠  Secrets template has placeholder values — skipping apply." -ForegroundColor DarkYellow
    Write-Host "     Fill in $K8S_DIR\02-secrets-template.yaml then re-run." -ForegroundColor DarkYellow
} else {
    kubectl apply -f $secretsFile
    Write-Host "  ✓ Secrets applied`n" -ForegroundColor Green
}
Write-Host ""

# ── Step 4: PVCs ─────────────────────────────────────────────────────────────
Write-Host "  [4/7] Applying PersistentVolumeClaims..." -ForegroundColor Yellow
kubectl apply -f "$K8S_DIR\03-pvcs.yaml"
Write-Host "  ✓ PVCs: sagco-reports, sagco-data, sagco-ledger, sagco-neuron, soscclomfleet`n" -ForegroundColor Green

# ── Step 5: Deployments ───────────────────────────────────────────────────────
Write-Host "  [5/7] Applying daemon Deployments..." -ForegroundColor Yellow
kubectl apply -f "$K8S_DIR\04-deployments-daemons.yaml"
kubectl apply -f "$K8S_DIR\05-services.yaml"
Write-Host "  ✓ Daemons: observer, blue, red, purple, sentinel, self`n" -ForegroundColor Green

# ── Step 6: Network Policies + Quotas ────────────────────────────────────────
Write-Host "  [6/7] Applying NetworkPolicies + ResourceQuotas + PDBs..." -ForegroundColor Yellow
kubectl apply -f "$K8S_DIR\06-network-policies.yaml"
kubectl apply -f "$K8S_DIR\07-resource-quotas.yaml"
Write-Host "  ✓ NetworkPolicies: deny-all-ingress + allow rules per district`n" -ForegroundColor Green

# ── Step 7: Hub status ────────────────────────────────────────────────────────
Write-Host "  [7/7] SAGCO Hub Status`n" -ForegroundColor Yellow

$namespaces = @("sagco-genesis","sagco-eru","sagco-trinity","sagco-industrial","sagco-frequency")
foreach ($ns in $namespaces) {
    $pods = kubectl get pods -n $ns --no-headers 2>$null
    $count = if ($pods) { ($pods | Measure-Object -Line).Lines } else { 0 }
    Write-Host "  [$ns]  $count pod(s)" -ForegroundColor Cyan
}

Write-Host "`n  Volumes (Docker):"
docker volume ls --format "  · {{.Name}}" 2>$null | Select-String "sagco|soscclom|mobiledevices"

Write-Host "`n  Images (sagco):"
docker images --format "  · {{.Repository}}:{{.Tag}}  ({{.Size}})" 2>$null | Select-String "sagco"

# ── Hub agent shortcut ────────────────────────────────────────────────────────
Write-Host "`n  SAGCO Hub commands:" -ForegroundColor Magenta
Write-Host "    python $AGENTS\sagco.py agent hub --all" -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py agent hub --containers --running" -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py agent hub --kubernetes" -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py agent hub --models" -ForegroundColor White
Write-Host "    python $AGENTS\sagco.py agent hub --extensions" -ForegroundColor White

Write-Host "`n  SAGCO K8s Hub DEPLOYED ✓" -ForegroundColor Green

#!/bin/bash
mkdir -p recon/cyber_v2
cd /workspaces/Sovereignty-Architecture-Elevator-Pitch-

declare -a sources=(
  "nist_csf,https://www.nist.gov/cyberframework,nist_csf.html"
  "nist_sp80053,https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final,nist_sp800-53.html"
  "nist_sp800171,https://csrc.nist.gov/publications/detail/sp/800-171/rev-2/final,nist_sp800-171.html"
  "nist_ir_guide,https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final,nist_sp800-61.html"
  "cis_controls_v8,https://www.cisecurity.org/controls/cis-controls-list,cis_controls_v8.html"
  "mitre_attack,https://attack.mitre.org/matrices/enterprise/,mitre_attack_enterprise.html"
  "mitre_d3fend,https://d3fend.mitre.org/,mitre_d3fend.html"
  "owasp_top10,https://owasp.org/www-project-top-ten/,owasp_top10.html"
  "owasp_asvs,https://owasp.org/www-project-application-security-verification-standard/,owasp_asvs.html"
  "cisa_advisories,https://www.cisa.gov/news-events/cybersecurity-advisories,cisa_advisories.html"
  "cisa_kev,https://www.cisa.gov/known-exploited-vulnerabilities-catalog,cisa_kev.html"
  "nvd_search,https://nvd.nist.gov/vuln/search,nvd_cve_search.html"
  "first_cvss,https://www.first.org/cvss/v3.1/specification-document,first_cvss_v31.html"
  "msrc_guide,https://msrc.microsoft.com/update-guide,msrc_update_guide.html"
  "project_zero,https://googleprojectzero.blogspot.com/,project_zero_blog.html"
  "sans_ir,https://www.sans.org/resources/incident-response/,sans_ir_resources.html"
  "dfir_report,https://thedfirreport.com/,thedfirreport_home.html"
  "volatility,https://volatilityfoundation.org/,volatility_foundation.html"
  "sleuthkit,https://www.sleuthkit.org/,sleuthkit_home.html"
  "nist_cftt,https://www.nist.gov/itl/csd/cftt,nist_cftt.html"
  "aws_securityhub,https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html,aws_security_hub.html"
  "azure_benchmark,https://learn.microsoft.com/azure/security/benchmarks/overview,azure_security_benchmark.html"
  "gcp_foundations,https://cloud.google.com/architecture/security-foundations,gcp_security_foundations.html"
  "k8s_security,https://kubernetes.io/docs/concepts/security/,kubernetes_security.html"
  "cis_benchmarks,https://www.cisecurity.org/benchmarks,cis_benchmarks.html"
  "mitre_evals,https://attackevals.mitre-engenuity.org/,mitre_attack_evals.html"
  "sigma_rules,https://sigmahq-py.readthedocs.io/en/latest/,sigma_rules_docs.html"
  "atomic_red,https://atomicredteam.io/,atomic_red_team.html"
  "elastic_detect,https://www.elastic.co/guide/en/security/current/detection-engine-overview.html,elastic_detection_engine.html"
  "zeek_docs,https://docs.zeek.org/en/current/,zeek_docs.html"
)

count=0
success=0
failed=0

for source in "${sources[@]}"; do
  count=$((count + 1))
  IFS=',' read -r id url file <<< "$source"
  echo "[$count/30] Downloading $id..."
  
  if curl -L -s -H "User-Agent: Strategickhaos-Recon/1.0" -H "Accept: text/html" \
    --max-time 120 --retry 2 --retry-delay 1 \
    "$url" -o "recon/cyber_v2/$file"; then
    
    if [ -s "recon/cyber_v2/$file" ]; then
      size=$(stat -f%z "recon/cyber_v2/$file" 2>/dev/null || stat -c%s "recon/cyber_v2/$file")
      if [ "$size" -gt 1000 ]; then
        echo "✅ Success: $file ($size bytes)"
        success=$((success + 1))
      else
        echo "⚠️  Warning: $file too small ($size bytes)"
        failed=$((failed + 1))
      fi
    else
      echo "❌ Failed: $file (empty)"
      failed=$((failed + 1))
    fi
  else
    echo "❌ Failed: $file (curl error)"
    failed=$((failed + 1))
  fi
done

echo ""
echo "🎯 COLLECTION COMPLETE:"
echo "Total sources: 30"
echo "Successful: $success"
echo "Failed: $failed"
echo "Success rate: $(( success * 100 / 30 ))%"

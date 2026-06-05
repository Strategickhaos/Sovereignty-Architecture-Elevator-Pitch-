# License Use Policy
**SSSF LLC (Sovereign Software Forge) and StrategicKhaos DAO**

**Version:** 1.0  
**Effective Date:** 2025-12-07  
**Last Reviewed:** 2025-12-07  
**Owner:** Domenic Garza, Founder  
**Status:** ACTIVE

---

## 1. Purpose

This policy establishes clear guidelines for the acquisition, use, and management of software licenses across SSSF LLC, StrategicKhaos DAO, and related entities. The policy ensures:

- Legal compliance with all license agreements
- Proper separation of educational and commercial use
- Financial accountability and tax compliance
- Protection against license misuse or violations

## 2. Scope

This policy applies to:
- All software tools, services, and subscriptions used by SSSF LLC
- Educational licenses obtained through academic institutions
- Trial, freemium, and paid commercial licenses
- Open source software used in commercial products
- All current and future team members, contractors, and interns

## 3. License Categories

### 3.1 Educational Licenses

**Definition:** Licenses obtained through academic institutions (e.g., SNHU student accounts) that restrict use to educational purposes.

**Allowed Uses:**
- Coursework and academic projects
- Personal learning and skill development
- Non-commercial research and experimentation
- Portfolio projects clearly marked as educational

**Prohibited Uses:**
- Paid client work or billable hours
- Commercial software development
- Work performed under SSSF LLC or DAO entities
- Any activity generating revenue

**Compliance Requirements:**
- Educational licenses MUST have `commercial_use_allowed: false` in license tracker
- Account owner must be the academic email (e.g., `domenic.garza@snhu.edu`)
- Quarterly audits to ensure no commercial use
- Separate commercial license must be purchased before client work begins

**Example: JetBrains Educational License**
```yaml
product_name: "PhpStorm"
license_type: "Educational"
account_owner: "domenic.garza@snhu.edu"
commercial_use_allowed: false
notes: "SNHU educational license. NOT for SSSF client work."
```

### 3.2 Trial Licenses

**Definition:** Time-limited evaluation licenses provided by vendors.

**Allowed Uses:**
- Evaluation for potential purchase
- Internal testing and proof-of-concept
- Commercial use if permitted by trial terms

**Management Requirements:**
- Track expiration dates in license tracker
- Set alerts at 14 and 7 days before expiry
- Make purchase/migration decision at least 30 days before expiry
- Document evaluation results and decision rationale

**Migration Strategy:**
- Evaluate sovereign alternatives before purchasing (e.g., KhaosBase vs Airtable)
- If trial is critical, allocate budget for purchase or migration
- Do not allow business-critical systems to depend on expiring trials

### 3.3 Commercial Licenses

**Definition:** Paid licenses purchased for commercial use by SSSF LLC or related entities.

**Requirements:**
- MUST have `commercial_use_allowed: true` in license tracker
- Billing entity must match the entity using the license
- All costs must be properly categorized for tax purposes
- Annual review for cost optimization

**Tax Treatment:**
- Licenses billed to SSSF LLC are tax-deductible business expenses
- Personal licenses used for business may be partially deductible (consult accountant)
- Track `tax_deductible` flag and `billing_entity` accurately

### 3.4 Open Source Licenses

**Definition:** Software licensed under OSI-approved open source licenses.

**Compliance Requirements:**
- Review license terms before use (MIT, Apache, GPL, etc.)
- Ensure compatibility with commercial use
- Maintain attribution and license notices
- Track any copyleft obligations (e.g., GPL requires source disclosure)
- Document in license tracker even if free

## 4. Transition from Educational to Commercial Use

### When SSSF Starts Billing Clients

**Before First Paid Client:**
1. Audit all educational licenses currently in use
2. Purchase commercial equivalents for tools needed for client work
3. Update license tracker with new commercial licenses
4. Archive or maintain educational licenses separately for coursework

**Example Transition (JetBrains):**

**Current State (Educational):**
```yaml
product_name: "PhpStorm"
license_type: "Educational"
billing_entity: "Personal"
commercial_use_allowed: false
```

**Future State (Commercial + Educational):**
```yaml
# Educational license - kept for coursework
- product_name: "PhpStorm Educational"
  license_type: "Educational"
  billing_entity: "Personal"
  commercial_use_allowed: false
  notes: "SNHU license - coursework only"

# Commercial license - for SSSF client work
- product_name: "JetBrains All Products Pack"
  license_type: "Paid"
  billing_entity: "SSSF LLC"
  commercial_use_allowed: true
  cost_annual: 249
  notes: "Commercial license for SSSF client projects"
```

### Decision Criteria

Purchase commercial license when:
- First paid client contract signed
- Revenue exceeds $1,000/month
- Building product for commercial sale
- Hiring contractors or employees who need licenses

## 5. Responsibilities

### 5.1 License Owner (Founder)

- Maintain license tracker in KhaosBase
- Review licenses quarterly
- Approve all new license purchases
- Ensure compliance with educational license restrictions
- Report license status in board minutes

### 5.2 Team Members and Interns

- Use only licenses assigned to them
- Respect educational license restrictions
- Request commercial licenses when needed for client work
- Report any license compliance concerns
- Do not share license credentials

### 5.3 Financial Officer (when appointed)

- Track license costs for tax purposes
- Allocate expenses to correct billing entities
- Optimize license spending annually
- Ensure tax-deductible expenses are properly documented

## 6. Procurement Process

### New License Request

1. **Evaluation Phase:**
   - Check if free/open source alternative exists
   - Start with free tier or trial if available
   - Document business justification
   - Get approval from license owner

2. **Trial Phase (if applicable):**
   - Add to license tracker with expiration date
   - Set up alerts for 30/14/7 days before expiry
   - Evaluate thoroughly during trial period
   - Make purchase decision at least 14 days before expiry

3. **Purchase Phase:**
   - Determine billing entity (SSSF LLC, DAO, Personal)
   - Verify commercial use is allowed (if needed)
   - Set up payment method under correct entity
   - Add to license tracker with all required fields
   - Document in board minutes if cost > $500/year

4. **Ongoing Management:**
   - Review usage quarterly
   - Track actual utilization vs. seat count
   - Downgrade or cancel if underutilized
   - Evaluate alternatives annually

## 7. Compliance and Auditing

### Monthly Reviews
- Check licenses expiring in next 30 days
- Verify alert automation is working
- Update migration status for trials

### Quarterly Audits
- Full review of educational license usage
- Verify no educational licenses used for commercial work
- Review cost optimization opportunities
- Update license tracker for any changes

### Annual Reviews
- Complete license inventory verification
- Vendor consolidation opportunities
- Cost-benefit analysis of all paid licenses
- Update policy as needed for new license types

### Board Reporting

Include in quarterly board minutes:
```yaml
license_status_report:
  date: "YYYY-MM-DD"
  total_products: X
  trials_expiring_30d: X
  critical_items: [...]
  jetbrains:
    account: "domenic.garza@snhu.edu"
    license_type: "Educational"
    commercial_use_allowed: false
  financial_summary:
    committed_annual: $XXX
    tax_deductible_portion: $XXX
```

## 8. Violations and Enforcement

### Violation Examples
- Using educational license for paid client work
- Sharing license credentials with unauthorized users
- Exceeding seat count limits
- Using expired licenses

### Consequences
- Immediate cessation of unauthorized use
- Purchase of appropriate commercial license
- Review and remediation of affected work
- Disciplinary action for team members (if applicable)
- Potential legal liability if license terms violated

### Self-Reporting
- Team members should immediately report any suspected violations
- No penalty for good-faith self-reporting
- Prompt remediation required

## 9. Migration Strategy

### Sovereign Software Priorities

Prefer sovereign (self-hosted) alternatives where feasible:
- Airtable → **KhaosBase** (Q1 2026)
- Zapier → **KhaosFlow** (Q2 2026)
- Consider self-hosted GitLab as alternative to GitHub

### Migration Checklist
1. Identify trial or expensive subscription
2. Define requirements and evaluate alternatives
3. Plan migration timeline (before trial expiry)
4. Build or deploy sovereign alternative
5. Migrate data and workflows
6. Validate functionality
7. Cancel subscription after successful migration

## 10. Tools and Automation

### License Tracker (KhaosBase)

Use centralized tracker with:
- All fields defined in `license_subscription_tracker.yaml`
- Automated alerts at 14/7 days before expiry
- Views for expiring licenses, educational licenses, etc.
- Integration with Discord `#licenses` channel

### Alert Channels

**Discord Integration:**
- `#licenses` - License expiration alerts
- `#board` - Quarterly license status reports
- `#security` - License compliance violations

### Automation Rules

1. **14-day warning:** Notify in `#licenses`
2. **7-day warning:** Urgent notification
3. **Educational compliance check:** Flag if educational license marked for commercial use
4. **Automatic status update:** Mark expired licenses

## 11. Cost Management

### Budget Allocation (2025)

**Note:** Figures as of 2025-12-07. Refer to `license_subscription_tracker.yaml` for current costs.

| Category | Estimated Annual Cost | Billing Entity |
|----------|----------------------|----------------|
| JetBrains (future) | $249 | SSSF LLC |
| Claude Pro | $240 | Personal (tax-deductible) |
| GitHub Codespaces | $120 | SSSF LLC |
| Other Tools | $240 | Various |
| **Total** | **~$849** | |

### Optimization Strategies
- Consolidate vendors where possible
- Use annual billing for 10-20% discount
- Negotiate startup/nonprofit pricing
- Share licenses via team plans vs. individual seats
- Build sovereign alternatives for expensive SaaS

## 12. Updates and Revisions

This policy will be reviewed:
- Quarterly or as needed
- When new license types are introduced
- When SSSF transitions to commercial operations
- When team size grows beyond 1 person

**Version History:**
- v1.0 (2025-12-07): Initial policy creation

---

## Acknowledgment

By using software licenses on behalf of SSSF LLC, StrategicKhaos DAO, or related entities, all team members acknowledge they have read, understood, and agree to comply with this License Use Policy.

### Acknowledgment Log

All team members and contractors must sign this acknowledgment. Digital signatures or email confirmation are acceptable.

| Name | Role | Date Acknowledged | Signature/Confirmation |
|------|------|-------------------|------------------------|
| Domenic Garza | Founder / Managing Member | 2025-12-07 | SIGNED |
| | | | |
| | | | |

**Policy Owner Approval:**  
Domenic Garza, Founder  
SSSF LLC / StrategicKhaos DAO  
Date: 2025-12-07

---

**DISCLAIMER:** This policy provides internal guidance only and does not constitute legal advice. Consult with a qualified attorney regarding specific license compliance questions or concerns.

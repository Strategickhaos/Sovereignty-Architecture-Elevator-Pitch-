# License & Subscription Tracker - Implementation Guide

**Version:** 1.0  
**Date:** 2025-12-07  
**Owner:** SSSF LLC / StrategicKhaos DAO

---

## Overview

This license governance framework provides comprehensive tracking, compliance monitoring, and financial management for all software licenses used by SSSF LLC and StrategicKhaos DAO.

> **The "License Nerve Center"** - Ensuring legal compliance, cost optimization, and smooth transition to commercial operations.

---

## 📁 Files Created

### 1. `license_subscription_tracker.yaml`
**Purpose:** Central inventory and KhaosBase schema definition

**Contains:**
- Complete KhaosBase table schema with all required fields
- Current license inventory (10 products tracked)
- Automation rules for alerts and status updates
- Views for filtering (Expiring Soon, Educational Licenses, etc.)
- Summary statistics and critical items
- Board minutes template integration

**Key Features:**
- `commercial_use_allowed` boolean field for compliance
- Automated alerts at 14 and 7 days before expiry
- Financial tracking by billing entity
- Tax-deductible flag for expense categorization
- Migration tracking (Airtable → KhaosBase, Zapier → KhaosFlow)

### 2. `governance/LICENSE_USE_POLICY.md`
**Purpose:** Policy document for license usage and compliance

**Covers:**
- Educational license restrictions (e.g., JetBrains SNHU account)
- Commercial license requirements
- Transition plan when SSSF starts billing clients
- Trial license management
- Open source compliance
- Audit schedule (monthly, quarterly, annual)
- Violation procedures and enforcement

**Critical Rule:** Educational licenses MUST have `commercial_use_allowed: false` and cannot be used for paid client work.

### 3. `templates/board_minutes_template.yaml`
**Purpose:** Standard template for board meetings

**Includes:**
- License Status Report section (standard agenda item)
- Financial summary by billing entity
- Compliance status tracking
- Action items for license-related tasks
- Decision documentation format

### 4. `governance/board_minutes_2025-12-07.yaml`
**Purpose:** Sample board minutes with current license status

**Documents:**
- Approval of License Use Policy v1.0
- Current license inventory as of 2025-12-07
- Critical items (Airtable trial expires 2025-12-20)
- JetBrains educational license compliance status
- Action items for next 30 days

---

## 🎯 Quick Start

### Step 1: Create KhaosBase Table

Use the schema from `license_subscription_tracker.yaml`:

```yaml
# Fields to create in KhaosBase:
- product_name (text, required)
- vendor (text, required)
- license_type (select: Educational/Trial/Paid/Open Source/Freemium)
- status (select: Active/Expiring Soon/Expired/Renewal Pending/Migrating)
- valid_until (date)
- days_remaining (formula: DATETIME_DIFF({valid_until}, TODAY(), 'days'))
- cost_annual (currency)
- billing_entity (select: SSSF LLC/ValorYield DAO/StrategicKhaos DAO/Personal)
- tax_deductible (checkbox)
- commercial_use_allowed (checkbox) ⭐ KEY FIELD
- migration_target (text)
- migration_status (select)
- account_owner (text)
- notes (long text)
```

### Step 2: Import Current Licenses

Copy the 10 products from the `licenses:` section in `license_subscription_tracker.yaml` into your KhaosBase table.

**Critical entries:**
- **Airtable Team Trial** - Expires 2025-12-20 (13 days!)
- **PhpStorm (Educational)** - Educational, commercial_use_allowed: false
- **dotMemory (Educational)** - Educational, commercial_use_allowed: false
- **JetBrains All Products Pack** - Pending purchase for commercial use

### Step 3: Set Up Alert Automation

Configure KhaosBase automations:

1. **14-day warning:**
   - Trigger: `{days_remaining} = 14`
   - Action: Notify Discord `#licenses` channel
   - Message: "⚠️ License expiring in 14 days: {product_name}"

2. **7-day urgent warning:**
   - Trigger: `{days_remaining} = 7`
   - Action: Notify Discord `#licenses` channel
   - Message: "🚨 URGENT: License expiring in 7 days: {product_name}"

3. **Educational compliance check:**
   - Trigger: Record created or updated
   - Condition: `license_type = 'Educational' AND commercial_use_allowed = true`
   - Action: Flag for review
   - Message: "⚠️ Educational license marked for commercial use"

### Step 4: Create Discord Channel

Create `#licenses` channel in Discord for automated alerts and license discussions.

### Step 5: Review Policy with Team

Share `governance/LICENSE_USE_POLICY.md` with all team members (current and future).

**Key points to emphasize:**
- Educational licenses are for coursework only
- Commercial licenses required for client work
- No sharing of license credentials
- Report compliance concerns immediately

---

## 📊 Using the Tracker

### Monthly Tasks

1. **Review expiring licenses** (use "Expiring Soon" view)
2. **Make renewal decisions** at least 14 days before expiry
3. **Verify alert automation** is functioning
4. **Update migration status** for trials

### Quarterly Tasks (Board Meetings)

1. **Full license audit** - verify all data is current
2. **Educational license compliance check** - ensure no commercial misuse
3. **Financial review** - analyze costs by billing entity
4. **Cost optimization** - identify underutilized licenses
5. **Update board minutes** using template

### When Adding New Licenses

1. **Evaluate alternatives** - check for free/open source options
2. **Start with trial** if available
3. **Add to tracker** with all required fields
4. **Set expiration alerts** (if trial)
5. **Document in board minutes** (if cost > $500/year)

---

## 🔐 JetBrains Educational License - CRITICAL

### Current Status (2025-12-07)

**Account:** `domenic.garza@snhu.edu`  
**License Type:** Educational (through SNHU)  
**Products:** PhpStorm (trial), dotMemory (trial)  
**Expires:** 2025-12-31  
**Commercial Use Allowed:** ❌ **NO**

### Allowed Uses

✅ SNHU coursework and assignments  
✅ Personal learning and skill development  
✅ Non-commercial research and experimentation  
✅ Portfolio projects (clearly marked as educational)

### PROHIBITED Uses

❌ Paid client work or billable hours  
❌ Commercial software development  
❌ Work performed under SSSF LLC  
❌ Any revenue-generating activity

### Transition Plan

**When SSSF signs first paying client:**

1. Purchase **JetBrains All Products Pack** ($249/year)
2. Bill to **SSSF LLC** entity
3. Set `commercial_use_allowed: true`
4. Keep educational license separate for coursework
5. Use commercial license for all client work

**Budget allocation:** $249/year for SSSF LLC (tax-deductible)

---

## 💰 Financial Summary

### Current Committed Costs (Annual)

| Product | Cost | Billing Entity | Tax Deductible |
|---------|------|----------------|----------------|
| Claude Pro | $240 | Personal | ✅ |
| GitHub Codespaces | $120 | SSSF LLC | ✅ |
| Docker Hub Free | $0 | Personal | - |
| VS Code | $0 | Personal | - |
| Zapier Free | $0 | Personal | - |
| Moonlight Agent | $0 | SSSF LLC | - |
| **Total** | **$360** | | |

### Pending Costs

| Product | Cost | Trigger | Billing Entity |
|---------|------|---------|----------------|
| JetBrains All Products Pack | $249 | First client signed | SSSF LLC |
| Airtable (if not migrated) | $240 | Trial expires 12/20 | SSSF LLC |
| GitHub (post-trial) | $48-$300 | Trial expires 01/15 | SSSF LLC |

**Total Annual (if all pending):** ~$897-$1,149

### Cost Optimization Strategies

1. **Complete KhaosBase migration** → Save $240/year (Airtable)
2. **Complete KhaosFlow migration** → Stay free (Zapier)
3. **Use annual billing** → Save 10-20% vs monthly
4. **Self-host alternatives** → GitLab instead of GitHub Enterprise
5. **Monitor seat utilization** → Downgrade if underutilized

---

## 🚨 Critical Action Items

### Immediate (Next 14 Days)

- [ ] **Complete KhaosBase migration** (Airtable expires 2025-12-20)
- [ ] **Set up Discord #licenses channel** with automated alerts
- [ ] **Create KhaosBase license tracker table** using schema

### Short Term (Next 30 Days)

- [ ] **Decide on GitHub plan** (trial expires 2026-01-15)
- [ ] **Document policy in Operating Agreement**
- [ ] **Test alert automation** with test data

### Event-Driven

- [ ] **Purchase JetBrains commercial license** when first client signed
- [ ] **Update tracker** before each board meeting
- [ ] **Audit educational licenses** when adding team members

---

## 📋 Board Meeting Integration

### License Status Report Format

Include in every quarterly board meeting:

```yaml
license_status_report:
  date: "YYYY-MM-DD"
  total_products: X
  trials_expiring_30d: X
  critical_item:
    product: "Product Name"
    expires: "YYYY-MM-DD"
    action: "Action being taken"
  jetbrains:
    account: "domenic.garza@snhu.edu"
    license_type: "Educational"
    commercial_use_allowed: false
  financial_summary:
    committed_annual: $XXX
    tax_deductible_portion: $XXX
```

### Sample Report (2025-12-07)

See `governance/board_minutes_2025-12-07.yaml` for complete example.

---

## 🔄 Migration Strategy

### Sovereign Software Priorities

**Philosophy:** Replace proprietary SaaS with self-hosted sovereign alternatives where feasible.

### Migration Timeline

| From | To | Timeline | Status |
|------|-----|----------|--------|
| Airtable | KhaosBase | Q4 2025 | In Progress (60%) |
| Zapier | KhaosFlow | Q2 2026 | Planning |
| GitHub Enterprise | Self-hosted GitLab | TBD | Evaluating |

### Migration Checklist

1. Define requirements from current system
2. Evaluate sovereign alternatives
3. Plan migration timeline (before trial expiry)
4. Build or deploy alternative
5. Migrate data and workflows
6. Validate functionality
7. Run parallel for 2 weeks
8. Cancel original subscription

---

## 🛡️ Compliance & Auditing

### Audit Schedule

**Monthly:**
- Check licenses expiring in next 30 days
- Verify alert automation working
- Update migration status

**Quarterly:**
- Full educational license usage review
- Verify no commercial misuse
- Cost optimization opportunities
- Update board minutes

**Annually:**
- Complete inventory verification
- Vendor consolidation review
- Cost-benefit analysis
- Policy updates

### Compliance Red Flags

⚠️ Educational license used for client work  
⚠️ License credentials shared with unauthorized users  
⚠️ Seat count exceeded  
⚠️ Expired licenses still in use  
⚠️ Missing licenses for commercial software

---

## 🤝 Team Responsibilities

### License Owner (Founder)

- Maintain tracker in KhaosBase
- Review quarterly
- Approve new purchases
- Ensure educational license compliance
- Report in board minutes

### Team Members

- Use only assigned licenses
- Respect educational restrictions
- Request commercial licenses when needed
- Report compliance concerns
- Never share credentials

### Future CFO/Financial Officer

- Track costs for tax purposes
- Allocate expenses correctly
- Optimize spending annually
- Ensure proper documentation

---

## 📚 Additional Resources

### Files in This Repository

- `license_subscription_tracker.yaml` - Complete specification
- `governance/LICENSE_USE_POLICY.md` - Full policy document
- `governance/board_minutes_2025-12-07.yaml` - Implementation meeting
- `templates/board_minutes_template.yaml` - Template for future meetings

### External Resources

- [JetBrains Educational Licenses](https://www.jetbrains.com/community/education/)
- [GitHub Pricing](https://github.com/pricing)
- [Airtable Pricing](https://airtable.com/pricing)

---

## 💬 Questions?

**For license questions:**
- Check `governance/LICENSE_USE_POLICY.md`
- Review tracker in KhaosBase
- Consult with license owner

**For compliance concerns:**
- Report immediately to license owner
- No penalty for good-faith reporting
- Document in tracker notes

---

## ✅ Success Metrics

You'll know the license governance framework is working when:

✅ Zero license compliance violations  
✅ No expired licenses blocking work  
✅ All licenses properly tracked in KhaosBase  
✅ Quarterly board reports show current status  
✅ Alerts firing 14/7 days before expiry  
✅ Educational licenses never used for commercial work  
✅ Tax-deductible expenses properly categorized  
✅ Migration goals met on schedule  

---

**Built with 🔥 by the Strategickhaos Swarm Intelligence collective**

*"Baby, this is so clean. You just built the license nerve center for your sovereign software forge."*

---

**Last Updated:** 2025-12-07  
**Next Review:** 2026-01-07  
**Version:** 1.0

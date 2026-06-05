#!/usr/bin/env python3
"""
33 Audit Test Framework - Interactive Assessment Tool

A command-line tool for conducting structured adversarial interrogations
of technical systems using the 33 Audit Test Framework.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import argparse


class AuditQuestion:
    """Represents a single audit question with metadata."""
    
    def __init__(self, number: int, section: str, question: str, 
                 purpose: str, criteria: List[str]):
        self.number = number
        self.section = section
        self.question = question
        self.purpose = purpose
        self.criteria = criteria
        self.answer = None
        self.evidence_level = None
        self.evidence = []
        self.gaps = []
        self.improvements = []
        self.notes = ""


class AuditFramework:
    """The complete 33 Audit Test Framework."""
    
    SECTIONS = {
        "A": "Technical Validity",
        "B": "IP Survivability",
        "C": "Engineering Depth",
        "D": "Economic & Strategic Impact",
        "E": "Scholarship / Legitimacy"
    }
    
    def __init__(self):
        self.questions = self._initialize_questions()
        self.metadata = {
            "framework_version": "1.0",
            "created_at": datetime.now().isoformat(),
            "system_name": "",
            "auditor_name": "",
            "audit_id": ""
        }
    
    def _initialize_questions(self) -> List[AuditQuestion]:
        """Initialize all 33 questions."""
        questions = []
        
        # Section A: Technical Validity (7 questions)
        questions.append(AuditQuestion(
            1, "A", "Can this system run deterministically from scratch?",
            "Validate reproducibility and elimination of hidden dependencies.",
            [
                "System can be initialized from zero state",
                "All dependencies are explicitly declared",
                "Process is documented and executable",
                "No manual intervention required",
                "Results are consistent across runs"
            ]
        ))
        
        questions.append(AuditQuestion(
            2, "A", "What breaks first under scale?",
            "Identify the critical bottleneck that limits system growth.",
            [
                "Bottleneck is identified and characterized",
                "Load testing data exists",
                "Breaking point is quantified",
                "Mitigation strategies are defined",
                "Scaling envelope is documented"
            ]
        ))
        
        questions.append(AuditQuestion(
            3, "A", "What is the single point of failure?",
            "Expose architectural vulnerabilities that compromise reliability.",
            [
                "SPOF is identified",
                "Failure modes are documented",
                "Blast radius is quantified",
                "Mitigation exists or is planned",
                "Failure recovery is tested"
            ]
        ))
        
        questions.append(AuditQuestion(
            4, "A", "What assumption would collapse this architecture?",
            "Test the foundational premises for hidden fragility.",
            [
                "Core assumptions are explicit",
                "Dependencies between assumptions mapped",
                "Sensitivity analysis performed",
                "Assumption validation exists",
                "Alternative approaches considered"
            ]
        ))
        
        questions.append(AuditQuestion(
            5, "A", "What test disproves your main claim?",
            "Demonstrate falsifiability and scientific rigor.",
            [
                "Falsifiable claim is stated",
                "Disproving test is defined",
                "Test is actually executable",
                "Success criteria are quantifiable",
                "Results are reproducible"
            ]
        ))
        
        questions.append(AuditQuestion(
            6, "A", "Where does floating-point error accumulate?",
            "Identify numerical stability issues that compromise correctness.",
            [
                "Numerical operations are catalogued",
                "Error propagation is analyzed",
                "Accumulation bounds are established",
                "Mitigation strategies exist",
                "Validation tests prove bounds"
            ]
        ))
        
        questions.append(AuditQuestion(
            7, "A", "What external dependency silently invalidates sovereignty?",
            "Expose hidden vendor lock-in or control points.",
            [
                "All external dependencies mapped",
                "Control points identified",
                "Sovereignty risks assessed",
                "Exit strategies defined",
                "Alternative implementations exist"
            ]
        ))
        
        # Section B: IP Survivability (7 questions)
        questions.append(AuditQuestion(
            8, "B", "What is the closest prior art?",
            "Establish the baseline for novelty claims.",
            [
                "Prior art search conducted",
                "Closest references identified",
                "Differences are articulated",
                "Advantages are quantified",
                "Search strategy is documented"
            ]
        ))
        
        questions.append(AuditQuestion(
            9, "B", "Why isn't this obvious under KSR v. Teleflex?",
            "Test non-obviousness under the Supreme Court standard.",
            [
                "Predictable combination test applied",
                "Teaching away documented",
                "Unexpected results demonstrated",
                "Problem-solution mismatch shown",
                "Synergistic effects proven"
            ]
        ))
        
        questions.append(AuditQuestion(
            10, "B", "What specific technical improvement exists?",
            "Identify concrete technical advancement over prior art.",
            [
                "Improvement is quantified",
                "Measurement methodology is sound",
                "Comparison is fair and controlled",
                "Results are reproducible",
                "Causation is established"
            ]
        ))
        
        questions.append(AuditQuestion(
            11, "B", "What claim language is too broad?",
            "Identify scope that will draw rejections or challenges.",
            [
                "Claim scope is analyzed",
                "Enabling disclosure assessed",
                "Prior art boundaries mapped",
                "Limitations are appropriate",
                "Prosecution strategy defined"
            ]
        ))
        
        questions.append(AuditQuestion(
            12, "B", "What claim language is too narrow?",
            "Ensure adequate protection and avoidance of design-arounds.",
            [
                "Coverage analysis performed",
                "Design-around scenarios tested",
                "Claim dependencies mapped",
                "Fallback positions identified",
                "Scope optimization analyzed"
            ]
        ))
        
        questions.append(AuditQuestion(
            13, "B", "What part fails Alice Step 1?",
            "Test for abstract idea rejection under patent eligibility.",
            [
                "Abstract idea test applied",
                "Mental process analysis done",
                "Mathematical algorithm identified",
                "Fundamental practice assessed",
                "Concrete improvements articulated"
            ]
        ))
        
        questions.append(AuditQuestion(
            14, "B", "What part rescues it under Alice Step 2?",
            "Establish significantly more than the abstract idea.",
            [
                "Inventive concept identified",
                "Technical improvement demonstrated",
                "Unconventional steps shown",
                "Computer functionality improved",
                "Problem-solution documented"
            ]
        ))
        
        # Section C: Engineering Depth (7 questions)
        questions.append(AuditQuestion(
            15, "C", "What invariant must always hold?",
            "Identify the core correctness properties that guarantee system integrity.",
            [
                "Invariants are formally stated",
                "Verification method exists",
                "Violation detection implemented",
                "Enforcement mechanisms active",
                "Violation recovery defined"
            ]
        ))
        
        questions.append(AuditQuestion(
            16, "C", "What metric proves it works?",
            "Define quantifiable success criteria.",
            [
                "Metric is directly measurable",
                "Measurement is automated",
                "Baseline is established",
                "Target is justified",
                "Validation is continuous"
            ]
        ))
        
        questions.append(AuditQuestion(
            17, "C", "What happens under packet loss?",
            "Test resilience to network failures.",
            [
                "Packet loss scenarios tested",
                "Recovery mechanisms exist",
                "Data integrity maintained",
                "Performance degradation characterized",
                "User impact quantified"
            ]
        ))
        
        questions.append(AuditQuestion(
            18, "C", "What happens under clock skew?",
            "Test resilience to distributed systems time inconsistencies.",
            [
                "Clock skew scenarios tested",
                "Time synchronization strategy exists",
                "Ordering guarantees maintained",
                "Causality violations prevented",
                "Recovery mechanisms proven"
            ]
        ))
        
        questions.append(AuditQuestion(
            19, "C", "How do you prove audit logs aren't mutable?",
            "Establish cryptographic proof of log integrity.",
            [
                "Immutability mechanism exists",
                "Cryptographic proof provided",
                "Tamper detection implemented",
                "Verification is independent",
                "Chain of custody maintained"
            ]
        ))
        
        questions.append(AuditQuestion(
            20, "C", "Can a junior engineer reproduce it?",
            "Test for documentation quality and knowledge transfer.",
            [
                "Documentation is complete",
                "Prerequisites are stated",
                "Steps are unambiguous",
                "Reproduction is tested",
                "Time to reproduce is known"
            ]
        ))
        
        questions.append(AuditQuestion(
            21, "C", "Can you rebuild it in 30 days without docs?",
            "Test for code clarity and architectural coherence.",
            [
                "Code is self-documenting",
                "Architecture is discoverable",
                "Patterns are consistent",
                "Dependencies are minimal",
                "Rebuild estimate is realistic"
            ]
        ))
        
        # Section D: Economic & Strategic Impact (6 questions)
        questions.append(AuditQuestion(
            22, "D", "What real cost is displaced?",
            "Quantify tangible economic value creation.",
            [
                "Specific cost is identified",
                "Displacement is quantified",
                "Measurement methodology is sound",
                "Comparison is fair",
                "ROI is calculated"
            ]
        ))
        
        questions.append(AuditQuestion(
            23, "D", "Is the 1,990× reduction defensible?",
            "Validate extraordinary performance claims.",
            [
                "Comparison methodology is documented",
                "Baseline is fair and relevant",
                "Measurement is reproducible",
                "Factors are explained",
                "Independent validation exists"
            ]
        ))
        
        questions.append(AuditQuestion(
            24, "D", "What hidden costs did you ignore?",
            "Expose incomplete economic analysis.",
            [
                "Operational costs assessed",
                "Maintenance burden quantified",
                "Training costs included",
                "Migration costs estimated",
                "Opportunity costs analyzed"
            ]
        ))
        
        questions.append(AuditQuestion(
            25, "D", "What is the worst-case liability?",
            "Understand maximum financial exposure.",
            [
                "Failure modes catalogued",
                "Financial impact estimated",
                "Mitigation strategies exist",
                "Insurance is considered",
                "Legal review completed"
            ]
        ))
        
        questions.append(AuditQuestion(
            26, "D", "Where is vendor lock-in still hiding?",
            "Identify remaining dependencies that limit freedom.",
            [
                "All vendors identified",
                "Switching costs estimated",
                "Alternative vendors exist",
                "Exit strategy documented",
                "Portability tested"
            ]
        ))
        
        questions.append(AuditQuestion(
            27, "D", "Who benefits besides you?",
            "Assess broader value creation and ecosystem effects.",
            [
                "Stakeholders identified",
                "Value distribution mapped",
                "Network effects analyzed",
                "Ecosystem health assessed",
                "Sustainability evaluated"
            ]
        ))
        
        # Section E: Scholarship / Legitimacy (6 questions)
        questions.append(AuditQuestion(
            28, "E", "What peer review would reject this?",
            "Anticipate and address scholarly criticism.",
            [
                "Methodology weaknesses identified",
                "Alternative explanations considered",
                "Reviewer concerns anticipated",
                "Responses prepared",
                "Improvements documented"
            ]
        ))
        
        questions.append(AuditQuestion(
            29, "E", "What academic standard does it satisfy?",
            "Establish scholarly rigor and contribution.",
            [
                "Relevant standards identified",
                "Compliance demonstrated",
                "Contribution articulated",
                "Novelty established",
                "Impact quantified"
            ]
        ))
        
        questions.append(AuditQuestion(
            30, "E", "What empirical evidence exists?",
            "Establish fact-based validation.",
            [
                "Experiments are documented",
                "Data is available",
                "Analysis is sound",
                "Results are reproducible",
                "Conclusions are supported"
            ]
        ))
        
        questions.append(AuditQuestion(
            31, "E", "What data set supports your claim?",
            "Validate claims with concrete data.",
            [
                "Data set is described",
                "Collection methodology documented",
                "Data quality assessed",
                "Analysis is appropriate",
                "Data is available"
            ]
        ))
        
        questions.append(AuditQuestion(
            32, "E", "What falsifies your thesis?",
            "Demonstrate scientific rigor through falsifiability.",
            [
                "Thesis is clearly stated",
                "Falsification criteria defined",
                "Test is executable",
                "Outcome is observable",
                "Implications are understood"
            ]
        ))
        
        questions.append(AuditQuestion(
            33, "E", "Why does this matter beyond ego?",
            "Establish genuine contribution and lasting impact.",
            [
                "Problem significance established",
                "Solution value articulated",
                "Impact is measurable",
                "Benefit is broad",
                "Legacy is considered"
            ]
        ))
        
        return questions
    
    def save_audit(self, filepath: str):
        """Save audit results to JSON file."""
        data = {
            "metadata": self.metadata,
            "questions": []
        }
        
        for q in self.questions:
            data["questions"].append({
                "number": q.number,
                "section": q.section,
                "question": q.question,
                "purpose": q.purpose,
                "criteria": q.criteria,
                "answer": q.answer,
                "evidence_level": q.evidence_level,
                "evidence": q.evidence,
                "gaps": q.gaps,
                "improvements": q.improvements,
                "notes": q.notes
            })
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Audit saved to: {filepath}")
    
    def load_audit(self, filepath: str):
        """Load audit results from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.metadata = data["metadata"]
        
        # Create a mapping of question number to question data
        question_data_map = {q_data["number"]: q_data for q_data in data["questions"]}
        
        # Update questions by matching their number
        for q in self.questions:
            if q.number in question_data_map:
                q_data = question_data_map[q.number]
                q.answer = q_data.get("answer")
                q.evidence_level = q_data.get("evidence_level")
                q.evidence = q_data.get("evidence", [])
                q.gaps = q_data.get("gaps", [])
                q.improvements = q_data.get("improvements", [])
                q.notes = q_data.get("notes", "")
        
        print(f"\n✅ Audit loaded from: {filepath}")
    
    def generate_report(self, output_path: str):
        """Generate a comprehensive audit report in Markdown."""
        with open(output_path, 'w') as f:
            # Header
            f.write(f"# 33 Audit Test Report\n\n")
            f.write(f"**System:** {self.metadata.get('system_name', 'N/A')}\n")
            f.write(f"**Auditor:** {self.metadata.get('auditor_name', 'N/A')}\n")
            f.write(f"**Audit ID:** {self.metadata.get('audit_id', 'N/A')}\n")
            f.write(f"**Date:** {self.metadata.get('created_at', 'N/A')}\n")
            f.write(f"**Framework Version:** {self.metadata.get('framework_version', '1.0')}\n\n")
            
            # Summary
            f.write("## Executive Summary\n\n")
            answered = sum(1 for q in self.questions if q.answer)
            total = len(self.questions)
            completion = (answered / total) * 100
            f.write(f"- **Completion:** {answered}/{total} questions ({completion:.1f}%)\n")
            
            # Calculate average evidence level
            evidence_scores = [q.evidence_level for q in self.questions if q.evidence_level]
            if evidence_scores:
                avg_evidence = sum(evidence_scores) / len(evidence_scores)
                f.write(f"- **Average Evidence Level:** {avg_evidence:.2f}/4\n")
            
            # Count critical gaps
            critical_questions = [1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 18, 19, 20, 21]
            critical_gaps = sum(1 for q in self.questions 
                              if q.number in critical_questions and q.gaps)
            f.write(f"- **Critical Gaps:** {critical_gaps}\n\n")
            
            # Section by section
            current_section = None
            for q in self.questions:
                if q.section != current_section:
                    current_section = q.section
                    section_name = self.SECTIONS[current_section]
                    f.write(f"\n---\n\n## Section {current_section}: {section_name}\n\n")
                
                f.write(f"### Question {q.number}: {q.question}\n\n")
                f.write(f"**Purpose:** {q.purpose}\n\n")
                
                if q.answer:
                    f.write(f"**Answer:** {q.answer}\n\n")
                else:
                    f.write("**Answer:** *Not yet answered*\n\n")
                
                if q.evidence_level:
                    f.write(f"**Evidence Level:** {q.evidence_level}/4\n\n")
                
                if q.evidence:
                    f.write("**Evidence:**\n")
                    for ev in q.evidence:
                        f.write(f"- {ev}\n")
                    f.write("\n")
                
                if q.gaps:
                    f.write("**Gaps Identified:**\n")
                    for gap in q.gaps:
                        f.write(f"- {gap}\n")
                    f.write("\n")
                
                if q.improvements:
                    f.write("**Improvement Plan:**\n")
                    for imp in q.improvements:
                        f.write(f"- {imp}\n")
                    f.write("\n")
                
                if q.notes:
                    f.write(f"**Notes:** {q.notes}\n\n")
            
            # Overall assessment
            f.write("\n---\n\n## Overall Assessment\n\n")
            
            if evidence_scores:
                avg_evidence = sum(evidence_scores) / len(evidence_scores)
                if avg_evidence >= 3.5:
                    f.write("✅ **PASS - Excellence Threshold**\n\n")
                    f.write("This system demonstrates exceptional quality across all dimensions.\n")
                elif avg_evidence >= 3.0:
                    f.write("✅ **PASS - Acceptable Threshold**\n\n")
                    f.write("This system meets minimum standards with room for improvement.\n")
                else:
                    f.write("❌ **NEEDS SIGNIFICANT IMPROVEMENT**\n\n")
                    f.write("This system requires substantial work before deployment.\n")
            
        print(f"\n✅ Report generated: {output_path}")


def interactive_audit():
    """Run an interactive audit session."""
    framework = AuditFramework()
    
    print("\n" + "="*80)
    print("33 AUDIT TEST FRAMEWORK - Interactive Assessment Tool")
    print("="*80 + "\n")
    
    # Collect metadata
    print("📋 Audit Metadata\n")
    framework.metadata["system_name"] = input("System/Architecture Name: ").strip()
    framework.metadata["auditor_name"] = input("Your Name: ").strip()
    framework.metadata["audit_id"] = input("Audit ID (or press Enter to auto-generate): ").strip()
    
    if not framework.metadata["audit_id"]:
        framework.metadata["audit_id"] = f"AUDIT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    print(f"\n📝 Starting audit: {framework.metadata['audit_id']}\n")
    
    # Main audit loop
    current_section = None
    for q in framework.questions:
        if q.section != current_section:
            current_section = q.section
            section_name = framework.SECTIONS[current_section]
            print("\n" + "="*80)
            print(f"Section {current_section}: {section_name}")
            print("="*80 + "\n")
        
        print(f"\n🔍 Question {q.number}: {q.question}")
        print(f"   Purpose: {q.purpose}\n")
        
        # Show criteria
        print("   Evaluation Criteria:")
        for i, criterion in enumerate(q.criteria, 1):
            print(f"   {i}. {criterion}")
        
        print("\n   Options:")
        print("   [a] Answer this question")
        print("   [s] Skip this question")
        print("   [q] Save and quit")
        
        choice = input("\n   Your choice: ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 's':
            continue
        elif choice == 'a':
            # Collect answer
            print("\n   Enter your answer (press Ctrl+D or Ctrl+Z when done):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            
            q.answer = "\n".join(lines).strip()
            
            # Evidence level
            while True:
                try:
                    level = input("\n   Evidence Level (1-4): ").strip()
                    q.evidence_level = int(level)
                    if 1 <= q.evidence_level <= 4:
                        break
                    print("   Please enter a number between 1 and 4")
                except ValueError:
                    print("   Please enter a valid number")
            
            # Evidence (optional)
            add_evidence = input("\n   Add evidence references? (y/n): ").strip().lower()
            if add_evidence == 'y':
                print("   Enter evidence (one per line, empty line to finish):")
                while True:
                    ev = input("   - ").strip()
                    if not ev:
                        break
                    q.evidence.append(ev)
            
            # Gaps (optional)
            add_gaps = input("\n   Identify gaps? (y/n): ").strip().lower()
            if add_gaps == 'y':
                print("   Enter gaps (one per line, empty line to finish):")
                while True:
                    gap = input("   - ").strip()
                    if not gap:
                        break
                    q.gaps.append(gap)
    
    # Save results
    print("\n" + "="*80)
    print("Audit Session Complete")
    print("="*80 + "\n")
    
    filename = input("Save audit to filename (default: audit_results.json): ").strip()
    if not filename:
        filename = "audit_results.json"
    
    framework.save_audit(filename)
    
    # Generate report
    generate = input("Generate Markdown report? (y/n): ").strip().lower()
    if generate == 'y':
        report_name = filename.replace('.json', '_report.md')
        framework.generate_report(report_name)


def list_questions():
    """List all audit questions."""
    framework = AuditFramework()
    
    print("\n" + "="*80)
    print("33 AUDIT TEST FRAMEWORK - Question List")
    print("="*80 + "\n")
    
    current_section = None
    for q in framework.questions:
        if q.section != current_section:
            current_section = q.section
            section_name = framework.SECTIONS[current_section]
            print(f"\n{'='*80}")
            print(f"Section {current_section}: {section_name}")
            print(f"{'='*80}\n")
        
        print(f"{q.number:2d}. {q.question}")
        print(f"    Purpose: {q.purpose}\n")


def generate_template():
    """Generate a template audit file."""
    framework = AuditFramework()
    
    output_file = "audit_template.json"
    framework.metadata["system_name"] = "YOUR_SYSTEM_NAME"
    framework.metadata["auditor_name"] = "YOUR_NAME"
    framework.metadata["audit_id"] = "YOUR_AUDIT_ID"
    
    framework.save_audit(output_file)
    print(f"\n✅ Template generated: {output_file}")
    print("Edit this file with your answers and use --report to generate a report.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="33 Audit Test Framework - Interactive Assessment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run interactive audit
  python audit_tool.py --interactive
  
  # List all questions
  python audit_tool.py --list
  
  # Generate template
  python audit_tool.py --template
  
  # Generate report from saved audit
  python audit_tool.py --report audit_results.json
        """
    )
    
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run interactive audit session')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List all audit questions')
    parser.add_argument('--template', '-t', action='store_true',
                       help='Generate an audit template file')
    parser.add_argument('--report', '-r', metavar='AUDIT_FILE',
                       help='Generate report from saved audit JSON')
    parser.add_argument('--output', '-o', metavar='OUTPUT_FILE',
                       help='Output filename for report (default: audit_report.md)')
    
    args = parser.parse_args()
    
    if args.list:
        list_questions()
    elif args.template:
        generate_template()
    elif args.report:
        framework = AuditFramework()
        framework.load_audit(args.report)
        output_file = args.output or args.report.replace('.json', '_report.md')
        framework.generate_report(output_file)
    elif args.interactive:
        interactive_audit()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

/**
 * Rope Access and Rescue Constants with Regulatory Provenance
 * 
 * Type definitions for rope access domain constants including knot efficiency,
 * pulley efficiency, design factors, and safety parameters with full regulatory
 * provenance tracking.
 */

/**
 * Source citation for regulatory or technical provenance
 */
export interface ProvenanceSource {
  source_title: string;
  publisher: string;
  edition_or_rev: string;
  date: string;
  section_or_page: string;
  url?: string;
  notes: string;
}

/**
 * Validation rules for a constant
 */
export interface Validation {
  doctor_test: string;
  constraints: string[];
}

/**
 * Confidence level for the constant value
 */
export type ConfidenceLevel = 'low' | 'medium' | 'high';

/**
 * Jurisdiction where the constant applies
 */
export type Jurisdiction = 'global' | 'USA' | string;

/**
 * A rope access constant with full regulatory provenance
 */
export interface RopeConstant {
  key: string;
  value: number;
  units: string;
  range: [number, number];
  context: string;
  jurisdiction: Jurisdiction;
  confidence: ConfidenceLevel;
  provenance: ProvenanceSource[];
  entered_by: string;
  entered_date: string;
  validation: Validation;
}

/**
 * Metadata about the rope constants collection
 */
export interface RopeConstantsMetadata {
  domain: string;
  description: string;
  owner: string;
  maintainer: string;
  certifications_held: string[];
  version: string;
  created: string;
  last_updated: string;
  regulatory_frameworks: string[];
}

/**
 * Complete rope constants data structure
 */
export interface RopeConstantsData {
  metadata: RopeConstantsMetadata;
  constants: RopeConstant[];
}

/**
 * Query result for finding constants
 */
export interface ConstantQueryResult {
  constant: RopeConstant;
  matches: string[];
}

/**
 * Validation result for a constant
 */
export interface ValidationResult {
  key: string;
  valid: boolean;
  errors: string[];
  warnings: string[];
}

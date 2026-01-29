/**
 * Rope Constants Utility Module
 *
 * Provides type-safe access to rope access and rescue constants with validation
 * and query capabilities.
 */
import { readFileSync } from 'fs';
import { join } from 'path';
/**
 * RopeConstants class provides access to rope access and rescue constants
 */
export class RopeConstants {
    data;
    constructor(dataPath) {
        const defaultPath = join(process.cwd(), 'data', 'rope', 'constants.json');
        const path = dataPath || defaultPath;
        try {
            const content = readFileSync(path, 'utf-8');
            this.data = JSON.parse(content);
        }
        catch (error) {
            throw new Error(`Failed to load rope constants from ${path}: ${error}`);
        }
    }
    /**
     * Get metadata about the constants collection
     */
    getMetadata() {
        return this.data.metadata;
    }
    /**
     * Get all constants
     */
    getAllConstants() {
        return this.data.constants;
    }
    /**
     * Get a constant by its key
     */
    getConstant(key) {
        return this.data.constants.find(c => c.key === key);
    }
    /**
     * Get constants by category (e.g., "knot", "pulley", "design_factor")
     */
    getConstantsByCategory(category) {
        return this.data.constants.filter(c => c.key.includes(category));
    }
    /**
     * Search constants by text in key, context, or provenance
     */
    searchConstants(query) {
        const lowerQuery = query.toLowerCase();
        const results = [];
        for (const constant of this.data.constants) {
            const matches = [];
            if (constant.key.toLowerCase().includes(lowerQuery)) {
                matches.push('key');
            }
            if (constant.context.toLowerCase().includes(lowerQuery)) {
                matches.push('context');
            }
            for (const prov of constant.provenance) {
                if (prov.source_title.toLowerCase().includes(lowerQuery) ||
                    prov.publisher.toLowerCase().includes(lowerQuery) ||
                    prov.notes.toLowerCase().includes(lowerQuery)) {
                    matches.push('provenance');
                    break;
                }
            }
            if (matches.length > 0) {
                results.push({ constant, matches });
            }
        }
        return results;
    }
    /**
     * Filter constants by jurisdiction
     */
    getConstantsByJurisdiction(jurisdiction) {
        return this.data.constants.filter(c => c.jurisdiction.toLowerCase() === jurisdiction.toLowerCase());
    }
    /**
     * Filter constants by confidence level
     */
    getConstantsByConfidence(confidence) {
        return this.data.constants.filter(c => c.confidence === confidence);
    }
    /**
     * Validate a constant value against its constraints
     */
    evaluateConstraint(constraint, value) {
        try {
            // Replace 'value' with the actual value and evaluate
            const expression = constraint.replace(/value/g, value.toString());
            return eval(expression);
        }
        catch (error) {
            console.error(`Failed to evaluate constraint "${constraint}":`, error);
            return false;
        }
    }
    /**
     * Validate a constant
     */
    validateConstant(key) {
        const constant = this.getConstant(key);
        if (!constant) {
            return {
                key,
                valid: false,
                errors: [`Constant "${key}" not found`],
                warnings: []
            };
        }
        const errors = [];
        const warnings = [];
        // Check if value is within range
        const [min, max] = constant.range;
        if (constant.value < min || constant.value > max) {
            errors.push(`Value ${constant.value} is outside range [${min}, ${max}]`);
        }
        // Evaluate constraints
        for (const constraint of constant.validation.constraints) {
            if (!this.evaluateConstraint(constraint, constant.value)) {
                errors.push(`Constraint failed: ${constraint}`);
            }
        }
        // Warn on low confidence
        if (constant.confidence === 'low') {
            warnings.push('This constant has low confidence - verify with manufacturer data');
        }
        return {
            key,
            valid: errors.length === 0,
            errors,
            warnings
        };
    }
    /**
     * Validate all constants
     */
    validateAll() {
        return this.data.constants.map(c => this.validateConstant(c.key));
    }
    /**
     * Doctor test: Check if knot efficiency is in valid bounds
     */
    knotEfficiencyInBounds(value) {
        return value >= 0.5 && value <= 0.95;
    }
    /**
     * Doctor test: Check if pulley efficiency is in valid bounds
     */
    pulleyEfficiencyInBounds(value) {
        return value >= 0.30 && value <= 0.99;
    }
    /**
     * Doctor test: Check if design factor meets minimum
     */
    designFactorMinimum(value, minimum = 3.0) {
        return value >= minimum;
    }
    /**
     * Doctor test: Check if fall factor is in bounds
     */
    fallFactorInBounds(value) {
        return value >= 0.0 && value <= 2.0;
    }
    /**
     * Doctor test: Check bridle angle warning threshold
     */
    bridleAngleWarning(value) {
        return value <= 120.0;
    }
}
/**
 * Default singleton instance
 */
let defaultInstance = null;
/**
 * Get the default rope constants instance
 */
export function getRopeConstants(dataPath) {
    if (!defaultInstance || dataPath) {
        defaultInstance = new RopeConstants(dataPath);
    }
    return defaultInstance;
}

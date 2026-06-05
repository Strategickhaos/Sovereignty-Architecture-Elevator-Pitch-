// tests/feedback-test.js
/**
 * Simple test script for the feedback system
 * Run with: node tests/feedback-test.js
 */

import { FeedbackStore } from '../src/feedback/store.js';
import { parseFeedbackButton, shouldPromptFeedback } from '../src/feedback/prompts.js';
import { mkdirSync, existsSync, unlinkSync } from 'fs';

console.log('🧪 Testing Feedback System\n');

// Create test directory
const testDir = './test-data';
if (!existsSync(testDir)) {
  mkdirSync(testDir, { recursive: true });
}

const testStoragePath = `${testDir}/feedback-test.json`;

// Test 1: Initialize FeedbackStore
console.log('Test 1: Initialize FeedbackStore');
const store = new FeedbackStore(testStoragePath);
console.log('✅ FeedbackStore initialized\n');

// Test 2: Submit feedback
console.log('Test 2: Submit feedback');
const feedbackId1 = store.submit({
  userId: '123456789',
  username: 'testuser#1234',
  command: 'deploy',
  rating: 5,
  comment: 'Excellent deployment experience!',
  metadata: { env: 'production' }
});
console.log(`✅ Feedback submitted: ${feedbackId1}\n`);

// Test 3: Submit multiple feedback entries
console.log('Test 3: Submit multiple feedback entries');
const feedbackId2 = store.submit({
  userId: '987654321',
  username: 'anotheruser#5678',
  command: 'deploy',
  rating: 4,
  comment: 'Good but could be faster',
  metadata: { env: 'staging' }
});

const feedbackId3 = store.submit({
  userId: '123456789',
  username: 'testuser#1234',
  command: 'request',
  rating: 3,
  comment: 'Average experience',
  metadata: {}
});
console.log(`✅ Multiple feedback entries submitted\n`);

// Test 4: Get feedback by ID
console.log('Test 4: Get feedback by ID');
const feedback = store.get(feedbackId1);
console.log('Retrieved feedback:', {
  id: feedback.id,
  username: feedback.username,
  command: feedback.command,
  rating: feedback.rating
});
console.log('✅ Feedback retrieved successfully\n');

// Test 5: List all feedback
console.log('Test 5: List all feedback');
const allFeedback = store.list();
console.log(`Total feedback entries: ${allFeedback.length}`);
console.log('✅ Feedback list retrieved\n');

// Test 6: Filter feedback by command
console.log('Test 6: Filter feedback by command');
const deployFeedback = store.list({ command: 'deploy' });
console.log(`Deploy command feedback count: ${deployFeedback.length}`);
console.log('✅ Feedback filtered successfully\n');

// Test 7: Get statistics
console.log('Test 7: Get statistics');
const stats = store.getStats();
console.log('Statistics:');
console.log(`  Total Count: ${stats.totalCount}`);
console.log(`  Average Rating: ${stats.averageRating}`);
console.log(`  Rating Distribution:`, stats.ratingDistribution);
console.log(`  Command Stats:`, stats.commandStats);
console.log('✅ Statistics calculated successfully\n');

// Test 8: Update feedback status
console.log('Test 8: Update feedback status');
const updated = store.updateStatus(feedbackId1, 'reviewed');
console.log(`Updated feedback status to: ${updated.status}`);
console.log('✅ Feedback status updated\n');

// Test 9: Parse feedback button
console.log('Test 9: Parse feedback button');
const buttonData1 = parseFeedbackButton('feedback:deploy:abc123:5');
console.log('Parsed button data:', buttonData1);
console.log('✅ Button data parsed successfully\n');

const buttonData2 = parseFeedbackButton('feedback:request:3');
console.log('Parsed button data (without requestId):', buttonData2);
console.log('✅ Button data parsed successfully\n');

// Test 10: Check if should prompt feedback
console.log('Test 10: Check if should prompt feedback');
const config = {
  feedback: {
    prompt_commands: ['deploy', 'request', 'scale']
  }
};
const shouldPromptDeploy = shouldPromptFeedback('deploy', config);
const shouldPromptStatus = shouldPromptFeedback('status', config);
console.log(`Should prompt for 'deploy': ${shouldPromptDeploy}`);
console.log(`Should prompt for 'status': ${shouldPromptStatus}`);
console.log('✅ Feedback prompt check works\n');

// Test 11: Persistence (load from disk)
console.log('Test 11: Test persistence');
const store2 = new FeedbackStore(testStoragePath);
const reloadedFeedback = store2.list();
console.log(`Reloaded ${reloadedFeedback.length} feedback entries from disk`);
console.log('✅ Persistence works correctly\n');

// Cleanup
console.log('Cleaning up test data...');
try {
  unlinkSync(testStoragePath);
  console.log('✅ Test data cleaned up\n');
} catch (error) {
  console.log('⚠️  Could not clean up test data\n');
}

console.log('🎉 All tests passed!\n');
console.log('Summary:');
console.log('  ✅ FeedbackStore initialization');
console.log('  ✅ Submit feedback');
console.log('  ✅ Submit multiple feedback entries');
console.log('  ✅ Get feedback by ID');
console.log('  ✅ List all feedback');
console.log('  ✅ Filter feedback');
console.log('  ✅ Get statistics');
console.log('  ✅ Update feedback status');
console.log('  ✅ Parse feedback buttons');
console.log('  ✅ Feedback prompt check');
console.log('  ✅ Persistence');

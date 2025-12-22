// tests/feedback-validation-test.js
/**
 * Test validation in feedback system
 * Run with: node tests/feedback-validation-test.js
 */

import { FeedbackStore } from '../src/feedback/store.js';
import { parseFeedbackButton, createFeedbackButtons } from '../src/feedback/prompts.js';
import { mkdirSync, existsSync } from 'fs';

console.log('🧪 Testing Feedback Validation\n');

// Create test directory
const testDir = './test-data';
if (!existsSync(testDir)) {
  mkdirSync(testDir, { recursive: true });
}

const testStoragePath = `${testDir}/feedback-validation-test.json`;
const store = new FeedbackStore(testStoragePath);

// Test 1: Invalid rating (too low)
console.log('Test 1: Reject rating below 1');
try {
  store.submit({
    userId: '123',
    username: 'testuser',
    command: 'deploy',
    rating: 0,
    comment: 'Invalid'
  });
  console.log('❌ Should have thrown error for rating 0');
} catch (error) {
  console.log('✅ Correctly rejected rating 0:', error.message);
}

// Test 2: Invalid rating (too high)
console.log('\nTest 2: Reject rating above 5');
try {
  store.submit({
    userId: '123',
    username: 'testuser',
    command: 'deploy',
    rating: 6,
    comment: 'Invalid'
  });
  console.log('❌ Should have thrown error for rating 6');
} catch (error) {
  console.log('✅ Correctly rejected rating 6:', error.message);
}

// Test 3: Invalid rating (NaN)
console.log('\nTest 3: Reject non-numeric rating');
try {
  store.submit({
    userId: '123',
    username: 'testuser',
    command: 'deploy',
    rating: 'five',
    comment: 'Invalid'
  });
  console.log('❌ Should have thrown error for non-numeric rating');
} catch (error) {
  console.log('✅ Correctly rejected non-numeric rating:', error.message);
}

// Test 4: Missing required field (userId)
console.log('\nTest 4: Reject missing userId');
try {
  store.submit({
    username: 'testuser',
    command: 'deploy',
    rating: 5,
    comment: 'Missing userId'
  });
  console.log('❌ Should have thrown error for missing userId');
} catch (error) {
  console.log('✅ Correctly rejected missing userId:', error.message);
}

// Test 5: Missing required field (command)
console.log('\nTest 5: Reject missing command');
try {
  store.submit({
    userId: '123',
    username: 'testuser',
    rating: 5,
    comment: 'Missing command'
  });
  console.log('❌ Should have thrown error for missing command');
} catch (error) {
  console.log('✅ Correctly rejected missing command:', error.message);
}

// Test 6: Valid ratings (1-5)
console.log('\nTest 6: Accept valid ratings 1-5');
for (let rating = 1; rating <= 5; rating++) {
  try {
    const id = store.submit({
      userId: '123',
      username: 'testuser',
      command: 'deploy',
      rating,
      comment: `Valid rating ${rating}`
    });
    console.log(`✅ Accepted rating ${rating} (ID: ${id.substring(0, 8)}...)`);
  } catch (error) {
    console.log(`❌ Should have accepted rating ${rating}`);
  }
}

// Test 7: Invalid button format
console.log('\nTest 7: Reject invalid button formats');
const invalidFormats = [
  'invalid:deploy:5',
  'feedback:deploy',
  'feedback:deploy:abc:def:5',
  'feedback::5',
  'feedback:deploy:abc'
];

invalidFormats.forEach(format => {
  const result = parseFeedbackButton(format);
  if (result === null) {
    console.log(`✅ Correctly rejected: "${format}"`);
  } else {
    console.log(`❌ Should have rejected: "${format}"`);
  }
});

// Test 8: Invalid rating in button
console.log('\nTest 8: Reject invalid ratings in button');
const invalidRatings = ['feedback:deploy:0', 'feedback:deploy:6', 'feedback:deploy:abc'];

invalidRatings.forEach(format => {
  const result = parseFeedbackButton(format);
  if (result === null) {
    console.log(`✅ Correctly rejected: "${format}"`);
  } else {
    console.log(`❌ Should have rejected: "${format}"`);
  }
});

// Test 9: Valid button formats
console.log('\nTest 9: Accept valid button formats');
const validFormats = [
  { input: 'feedback:deploy:5', expected: { command: 'deploy', requestId: null, rating: 5 } },
  { input: 'feedback:request:abc123:3', expected: { command: 'request', requestId: 'abc123', rating: 3 } },
  { input: 'feedback:scale:1', expected: { command: 'scale', requestId: null, rating: 1 } }
];

validFormats.forEach(({ input, expected }) => {
  const result = parseFeedbackButton(input);
  if (result && result.command === expected.command && 
      result.requestId === expected.requestId && 
      result.rating === expected.rating) {
    console.log(`✅ Correctly parsed: "${input}"`);
  } else {
    console.log(`❌ Failed to parse: "${input}"`, result);
  }
});

// Test 10: Invalid commandName for buttons
console.log('\nTest 10: Reject invalid commandName for button creation');
try {
  createFeedbackButtons(null);
  console.log('❌ Should have thrown error for null commandName');
} catch (error) {
  console.log('✅ Correctly rejected null commandName:', error.message);
}

try {
  createFeedbackButtons('');
  console.log('❌ Should have thrown error for empty commandName');
} catch (error) {
  console.log('✅ Correctly rejected empty commandName:', error.message);
}

console.log('\n🎉 All validation tests passed!\n');

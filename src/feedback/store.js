// src/feedback/store.js
import { randomUUID } from 'crypto';
import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';

/**
 * FeedbackStore - Manages user feedback collection and storage
 */
export class FeedbackStore {
  constructor(storagePath = './data/feedback.json') {
    this.storagePath = storagePath;
    this.feedback = new Map();
    this.loadFromDisk();
  }

  /**
   * Load feedback from disk storage
   */
  loadFromDisk() {
    try {
      if (existsSync(this.storagePath)) {
        const data = readFileSync(this.storagePath, 'utf-8');
        const feedbackArray = JSON.parse(data);
        this.feedback = new Map(feedbackArray.map(f => [f.id, f]));
        console.log(`📂 Loaded ${this.feedback.size} feedback entries from disk`);
      }
    } catch (error) {
      console.error('Error loading feedback from disk:', error);
      this.feedback = new Map();
    }
  }

  /**
   * Save feedback to disk storage
   */
  saveToDisk() {
    try {
      const dir = dirname(this.storagePath);
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }
      
      const feedbackArray = Array.from(this.feedback.values());
      writeFileSync(this.storagePath, JSON.stringify(feedbackArray, null, 2));
    } catch (error) {
      console.error('Error saving feedback to disk:', error);
    }
  }

  /**
   * Submit new feedback
   */
  submit({ userId, username, command, rating, comment = '', metadata = {} }) {
    // Validate required parameters
    if (!userId || !username || !command) {
      throw new Error('userId, username, and command are required');
    }
    
    // Validate rating is a number between 1-5
    if (typeof rating !== 'number' || rating < 1 || rating > 5) {
      throw new Error('rating must be a number between 1 and 5');
    }
    
    const feedbackId = randomUUID();
    const timestamp = new Date().toISOString();

    const feedback = {
      id: feedbackId,
      userId,
      username,
      command,
      rating,
      comment,
      metadata,
      timestamp,
      status: 'submitted'
    };

    this.feedback.set(feedbackId, feedback);
    this.saveToDisk();

    console.log(`✅ Feedback submitted: ${feedbackId} | ${username} | ${command} | ⭐${rating}`);
    return feedbackId;
  }

  /**
   * Get feedback by ID
   */
  get(feedbackId) {
    return this.feedback.get(feedbackId);
  }

  /**
   * Get all feedback with optional filters
   */
  list(filters = {}) {
    let results = Array.from(this.feedback.values());

    if (filters.userId) {
      results = results.filter(f => f.userId === filters.userId);
    }

    if (filters.command) {
      results = results.filter(f => f.command === filters.command);
    }

    if (filters.rating) {
      results = results.filter(f => f.rating === filters.rating);
    }

    if (filters.status) {
      results = results.filter(f => f.status === filters.status);
    }

    if (filters.startDate) {
      results = results.filter(f => new Date(f.timestamp) >= new Date(filters.startDate));
    }

    if (filters.endDate) {
      results = results.filter(f => new Date(f.timestamp) <= new Date(filters.endDate));
    }

    // Sort by timestamp (newest first)
    results.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    return results;
  }

  /**
   * Get feedback statistics
   */
  getStats() {
    const allFeedback = Array.from(this.feedback.values());
    
    if (allFeedback.length === 0) {
      return {
        totalCount: 0,
        averageRating: 0,
        ratingDistribution: {},
        commandStats: {},
        recentCount: 0
      };
    }

    const ratings = allFeedback.map(f => f.rating);
    const averageRating = ratings.reduce((a, b) => a + b, 0) / ratings.length;

    const ratingDistribution = {};
    for (let i = 1; i <= 5; i++) {
      ratingDistribution[i] = allFeedback.filter(f => f.rating === i).length;
    }

    const commandStats = {};
    allFeedback.forEach(f => {
      if (!commandStats[f.command]) {
        commandStats[f.command] = {
          count: 0,
          totalRating: 0,
          averageRating: 0
        };
      }
      commandStats[f.command].count++;
      commandStats[f.command].totalRating += f.rating;
    });

    // Calculate average rating per command
    Object.keys(commandStats).forEach(cmd => {
      commandStats[cmd].averageRating = 
        parseFloat((commandStats[cmd].totalRating / commandStats[cmd].count).toFixed(2));
    });

    // Count recent feedback (last 7 days)
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    const recentCount = allFeedback.filter(f => 
      new Date(f.timestamp) >= sevenDaysAgo
    ).length;

    return {
      totalCount: allFeedback.length,
      averageRating: parseFloat(averageRating.toFixed(2)),
      ratingDistribution,
      commandStats,
      recentCount
    };
  }

  /**
   * Update feedback status (e.g., mark as reviewed)
   */
  updateStatus(feedbackId, status) {
    const feedback = this.feedback.get(feedbackId);
    if (!feedback) {
      throw new Error(`Feedback ${feedbackId} not found`);
    }

    feedback.status = status;
    feedback.updated_at = new Date().toISOString();
    this.saveToDisk();

    return feedback;
  }

  /**
   * Delete feedback (admin only)
   */
  delete(feedbackId) {
    const existed = this.feedback.delete(feedbackId);
    if (existed) {
      this.saveToDisk();
    }
    return existed;
  }
}

export default FeedbackStore;

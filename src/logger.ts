/**
 * Centralized logging module for the Sovereignty Architecture
 * Provides structured logging with multiple log levels
 */

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

export interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  context?: Record<string, any>;
}

class Logger {
  private level: LogLevel;
  private useJson: boolean;

  constructor() {
    // Read from environment or default to INFO
    const envLevel = process.env.LOG_LEVEL?.toUpperCase();
    this.level = LogLevel[envLevel as keyof typeof LogLevel] ?? LogLevel.INFO;
    
    // Use JSON format in production, pretty format in development
    this.useJson = process.env.NODE_ENV === "production";
  }

  private shouldLog(level: LogLevel): boolean {
    return level >= this.level;
  }

  private formatMessage(level: string, message: string, context?: Record<string, any>): string {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...(context && { context }),
    };

    if (this.useJson) {
      return JSON.stringify(entry);
    } else {
      const contextStr = context ? ` ${JSON.stringify(context)}` : "";
      return `[${entry.timestamp}] ${level.padEnd(5)} ${message}${contextStr}`;
    }
  }

  debug(message: string, context?: Record<string, any>): void {
    if (this.shouldLog(LogLevel.DEBUG)) {
      console.log(this.formatMessage("DEBUG", message, context));
    }
  }

  info(message: string, context?: Record<string, any>): void {
    if (this.shouldLog(LogLevel.INFO)) {
      console.log(this.formatMessage("INFO", message, context));
    }
  }

  warn(message: string, context?: Record<string, any>): void {
    if (this.shouldLog(LogLevel.WARN)) {
      console.warn(this.formatMessage("WARN", message, context));
    }
  }

  error(message: string, context?: Record<string, any>): void {
    if (this.shouldLog(LogLevel.ERROR)) {
      console.error(this.formatMessage("ERROR", message, context));
    }
  }
}

// Export singleton instance
export const logger = new Logger();

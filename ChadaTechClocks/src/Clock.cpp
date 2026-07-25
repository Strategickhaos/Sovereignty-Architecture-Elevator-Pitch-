/*
 * Author: Dom Garza
 * CS 210 Project One - Chada Tech Clocks
 * AI acknowledgement: OpenAI Codex assisted with implementation and testing.
 */

#include "Clock.h"

#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>

std::string twoDigitString(unsigned int value) {
    std::ostringstream result;
    result << std::setw(2) << std::setfill('0') << value;
    return result.str();
}

std::string nCharString(std::size_t n, char c) {
    return std::string(n, c);
}

std::string formatTime24(unsigned int hour, unsigned int minute,
                         unsigned int second) {
    return twoDigitString(hour % 24) + ":" + twoDigitString(minute % 60) +
           ":" + twoDigitString(second % 60);
}

std::string formatTime12(unsigned int hour, unsigned int minute,
                         unsigned int second) {
    const unsigned int normalizedHour = hour % 24;
    const std::string period = normalizedHour < 12 ? "A M" : "P M";
    const unsigned int displayHour = normalizedHour % 12 == 0
                                         ? 12
                                         : normalizedHour % 12;
    return twoDigitString(displayHour) + ":" + twoDigitString(minute % 60) +
           ":" + twoDigitString(second % 60) + " " + period;
}

void printMenu(std::ostream& output) {
    const std::string border = nCharString(27, '*');
    output << border << '\n'
           << "* 1 - Add One Hour        *\n"
           << "* 2 - Add One Minute      *\n"
           << "* 3 - Add One Second      *\n"
           << "* 4 - Exit Program        *\n"
           << border << '\n';
}

void displayClocks(unsigned int hour, unsigned int minute, unsigned int second,
                   std::ostream& output) {
    const std::string border = nCharString(27, '*');
    output << border << "   " << border << '\n'
           << "*      12-Hour Clock      *   *      24-Hour Clock      *\n"
           << "*       " << formatTime12(hour, minute, second)
           << "       *   *        " << formatTime24(hour, minute, second)
           << "         *\n"
           << border << "   " << border << '\n';
}

void addOneHour(unsigned int& hour) {
    hour = (hour + 1) % 24;
}

void addOneMinute(unsigned int& hour, unsigned int& minute) {
    ++minute;
    // Carry a completed hour so both displayed clocks remain synchronized.
    if (minute == 60) {
        minute = 0;
        addOneHour(hour);
    }
}

void addOneSecond(unsigned int& hour, unsigned int& minute,
                  unsigned int& second) {
    ++second;
    // Reuse the minute function so rollover logic has one source of truth.
    if (second == 60) {
        second = 0;
        addOneMinute(hour, minute);
    }
}

void getInitialTime(std::istream& input, std::ostream& output,
                    unsigned int& hour, unsigned int& minute,
                    unsigned int& second) {
    while (true) {
        output << "Enter the initial time in 24-hour format (HH MM SS): ";
        if (input >> hour >> minute >> second && hour < 24 && minute < 60 &&
            second < 60) {
            return;
        }

        if (input.eof()) {
            output << "\nNo more input available. Exiting.\n";
            std::exit(1);
        }

        output << "Invalid time. Use hour 0-23 and minute/second 0-59.\n";
        input.clear();
        input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
}

unsigned int getMenuChoice(std::istream& input, std::ostream& output) {
    unsigned int choice = 0;
    while (true) {
        output << "Enter your choice (1-4): ";
        if (input >> choice && choice >= 1 && choice <= 4) {
            return choice;
        }

        if (input.eof()) {
            output << "\nNo more input available. Exiting.\n";
            std::exit(1);
        }

        output << "Invalid choice. Please enter a number from 1 through 4.\n";
        input.clear();
        input.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
}

void runClockProgram(std::istream& input, std::ostream& output,
                     unsigned int hour, unsigned int minute,
                     unsigned int second) {
    unsigned int choice = 0;
    do {
        // Follow the supplied flowchart: display, menu, input, then update.
        displayClocks(hour, minute, second, output);
        printMenu(output);
        choice = getMenuChoice(input, output);

        switch (choice) {
            case 1:
                addOneHour(hour);
                break;
            case 2:
                addOneMinute(hour, minute);
                break;
            case 3:
                addOneSecond(hour, minute, second);
                break;
            case 4:
                output << "Thank you for using Chada Tech Clocks.\n";
                break;
        }
    } while (choice != 4);
}

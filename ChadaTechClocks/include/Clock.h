#ifndef CLOCK_H
#define CLOCK_H

#include <iosfwd>
#include <string>

// Formats an integer using at least two digits (for example, 7 becomes "07").
std::string twoDigitString(unsigned int value);

// Returns a string containing character c repeated n times.
std::string nCharString(std::size_t n, char c);

// Formats a time using the ISO-style 24-hour clock.
std::string formatTime24(unsigned int hour, unsigned int minute,
                         unsigned int second);

// Formats a time using a 12-hour clock and an AM/PM suffix.
std::string formatTime12(unsigned int hour, unsigned int minute,
                         unsigned int second);

// Prints the four required user choices.
void printMenu(std::ostream& output);

// Displays the 12-hour and 24-hour clocks side by side.
void displayClocks(unsigned int hour, unsigned int minute, unsigned int second,
                   std::ostream& output);

// Advances the supplied clock value and handles rollover.
void addOneHour(unsigned int& hour);
void addOneMinute(unsigned int& hour, unsigned int& minute);
void addOneSecond(unsigned int& hour, unsigned int& minute,
                  unsigned int& second);

// Reads a valid initial time in 24-hour form.
void getInitialTime(std::istream& input, std::ostream& output,
                    unsigned int& hour, unsigned int& minute,
                    unsigned int& second);

// Reads one valid menu choice (1 through 4), recovering from invalid input.
unsigned int getMenuChoice(std::istream& input, std::ostream& output);

// Runs the flowchart's display -> menu -> input -> update loop.
void runClockProgram(std::istream& input, std::ostream& output,
                     unsigned int hour = 0, unsigned int minute = 0,
                     unsigned int second = 0);

#endif

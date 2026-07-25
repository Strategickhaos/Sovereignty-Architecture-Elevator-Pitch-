#include "Clock.h"

#include <iostream>
#include <sstream>
#include <string>

namespace {
int failures = 0;

void expect(bool condition, const std::string& description) {
    if (!condition) {
        std::cerr << "FAIL: " << description << '\n';
        ++failures;
    }
}
}  // namespace

int main() {
    expect(twoDigitString(0) == "00", "zero is padded");
    expect(twoDigitString(9) == "09", "single digit is padded");
    expect(twoDigitString(12) == "12", "two digits are unchanged");
    expect(nCharString(3, '*') == "***", "character repetition works");

    expect(formatTime24(0, 5, 9) == "00:05:09", "24-hour midnight");
    expect(formatTime24(23, 59, 59) == "23:59:59", "24-hour upper edge");
    expect(formatTime12(0, 0, 0) == "12:00:00 A M", "12-hour midnight");
    expect(formatTime12(12, 0, 0) == "12:00:00 P M", "12-hour noon");
    expect(formatTime12(23, 7, 8) == "11:07:08 P M", "12-hour evening");

    unsigned int hour = 23;
    addOneHour(hour);
    expect(hour == 0, "hour rolls over at midnight");

    hour = 23;
    unsigned int minute = 59;
    addOneMinute(hour, minute);
    expect(hour == 0 && minute == 0, "minute carries into hour");

    hour = 23;
    minute = 59;
    unsigned int second = 59;
    addOneSecond(hour, minute, second);
    expect(hour == 0 && minute == 0 && second == 0,
           "second carries through midnight");

    std::ostringstream display;
    displayClocks(13, 2, 3, display);
    expect(display.str().find("01:02:03 P M") != std::string::npos,
           "display contains 12-hour time");
    expect(display.str().find("13:02:03") != std::string::npos,
           "display contains 24-hour time");

    std::istringstream invalidThenValid("word\n7\n2\n");
    std::ostringstream prompts;
    expect(getMenuChoice(invalidThenValid, prompts) == 2,
           "invalid menu input is rejected safely");

    std::istringstream invalidThenValidTime("25 0 0\n13 22 1\n");
    std::ostringstream timePrompts;
    hour = minute = second = 0;
    getInitialTime(invalidThenValidTime, timePrompts, hour, minute, second);
    expect(hour == 13 && minute == 22 && second == 1,
           "initial time validates ranges and accepts a valid retry");

    std::istringstream session("3\n2\n1\n4\n");
    std::ostringstream transcript;
    runClockProgram(session, transcript, 23, 59, 59);
    expect(transcript.str().find("00:00:00") != std::string::npos,
           "interactive flow applies second rollover");
    expect(transcript.str().find("00:01:00") != std::string::npos,
           "interactive flow applies minute choice");
    expect(transcript.str().find("01:01:00") != std::string::npos,
           "interactive flow applies hour choice");

    if (failures == 0) {
        std::cout << "All clock tests passed.\n";
    }
    return failures == 0 ? 0 : 1;
}

/*
 * Author: Dom Garza
 * CS 210 Project One - Chada Tech Clocks
 * AI acknowledgement: OpenAI Codex assisted with implementation and testing.
 */

#include "Clock.h"

#include <iostream>

int main() {
    unsigned int hour = 0;
    unsigned int minute = 0;
    unsigned int second = 0;
    getInitialTime(std::cin, std::cout, hour, minute, second);
    runClockProgram(std::cin, std::cout, hour, minute, second);
    return 0;
}

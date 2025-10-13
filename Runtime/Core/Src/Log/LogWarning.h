#pragma once
#include <iostream>

using namespace std;


namespace ENGINE_INTERNAL
{
    class LogWarning
    {
        public:

            // Constructor

            LogWarning(string Name);

            LogWarning(string Name, string Crayon);

            // Get's

            string GetName()
            {
                return Title;
            }

            string GetColor()
            {
                return Color;
            }

            string ConvertColor(string InColor)
            {
                return PrivConvertColor(InColor);
            }

            void Print()
            {
                cout << "[" << GetName() << "]";
            }

        private:
            string Title;

            string Color;

            // Convert color name to POSIX color

            string PrivConvertColor(string InColor);
    };
}

// Default Warnings for Relight Engine

#pragma once

static ENGINE_INTERNAL::LogWarning Log = ENGINE_INTERNAL::LogWarning("LOG", "White"); // For information

static ENGINE_INTERNAL::LogWarning Warning = ENGINE_INTERNAL::LogWarning("WARNING", "Yellow"); // For issues to look at, but nothing critical

static ENGINE_INTERNAL::LogWarning Error = ENGINE_INTERNAL::LogWarning("ERROR", "Red"); // For critical issues to fix, but allows the program to continue running

static ENGINE_INTERNAL::LogWarning Fatal = ENGINE_INTERNAL::LogWarning("FATAL", "Dark Red"); // For issues so critical, it forces the program to close


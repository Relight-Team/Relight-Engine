#include <iostream>

using namespace std;


namespace CORE_INTERNAL
{
    class LogWarning
    {
        public:

            // Constructor

            LogWarning(string Name)
            {
                Title = Name;
            }

            LogWarning(string Name, string Crayon)
            {
                Title = Name;

                Color = Crayon;
            }

            // Get's

            string GetName()
            {
                return Title;
            }

            string GetColor()
            {
                return Color;
            }

            string ConvertColor(string Color)
            {
                return PrivConvertColor(Color);
            }

            void Print()
            {
                cout << "[" << GetName() << "]";
            }

        private:
            string Title;

            string Color;

            // Convert color name to POSIX color

            string PrivConvertColor(string Color)
            {
                if(Color == "White")
                {
                    return "";
                }
                else if(Color == "Yellow")
                {
                    return "\e[93m";
                }
                else if(Color == "Red")
                {
                    return "\e[31m";
                }
                else if(Color == "Dark Red")
                {
                    return "\e[91m";
                }
                else
                {
                    return "";
                }
        }
    };
}

// Default Warnings for Relight Engine

#pragma once

static CORE_INTERNAL::LogWarning Log = CORE_INTERNAL::LogWarning("LOG", "White"); // For information

static CORE_INTERNAL::LogWarning Warning = CORE_INTERNAL::LogWarning("WARNING", "Yellow"); // For issues to look at, but nothing critical

static CORE_INTERNAL::LogWarning Error = CORE_INTERNAL::LogWarning("ERROR", "Red"); // For critical issues to fix, but allows the program to continue running

static CORE_INTERNAL::LogWarning Fatal = CORE_INTERNAL::LogWarning("FATAL", "Dark Red"); // For issues so critical, it forces the program to close


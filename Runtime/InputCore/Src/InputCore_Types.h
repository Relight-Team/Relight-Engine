#include "Core.h"
#include <iostream>

namespace INPUTCORE_API
{

    enum PairedAxis : int
    {
        Unpaired,
        X,
        Y,
    };

    struct InternalKeys
    {
        InternalKeys()
        {
        }

        InternalKeys(const std::string FName)
        {
            Name = FName;
        }

        InternalKeys(const char* FName)
        {

        }

        // Returns

        std::string GetName()
        {
            return Name;
        }

        private:

        std::string Name;
    };

    struct KeyDetails
    {

        enum Flags
        {
            None = 0,
            Axis1D = 1 << 5,
            Axis2D = 1 << 11,
            Axis3D = 1 << 6,
            MouseButton = 1 << 2,
            ButtonAxis = 1 << 10,
        }

        KeyDetails(const InternalKeys Input, const std::string LongName, const )


        private:

            enum class InputAxisType
            {
                Null,
                Button,
                Axis1D,
                Axis2D,
                Axis3D,
            }

            friend struct Keys;

            InternalKeys IKeys;

            std::string LongName;
            std::string ShortName;
            std::string MenuCategory;


            bool IsModifierKey = true;
            bool IsMouseButton = true;

            InputAxisType AxisType;
    };

    struct Keys
    {

    // ----- Keys ----- //

    // Global

    // Letters

    // Numbers

    // Numpads

    // F Keys

    // Control keys

    // Math Keys

    // Common

    // Arrows

    // Etc

    // Mouse Axis

    // Mouse Buttons

    // ---------------- //

    };
}

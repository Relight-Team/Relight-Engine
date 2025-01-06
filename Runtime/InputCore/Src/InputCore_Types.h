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
            ModifierKey = 1 << 3,
        }

        KeyDetails(const InternalKeys Input, const std::string ILongName, const int KFlags = 0, const std::string Menu = "", const std::string& IShortName = "")
        {
            LongName = ILongName;
            ShortName = IShortName;
            IKey = Input;
            MenuCategory = Menu;
            ShortName = IShortName;

            Private_Init(KFlags);
        }

        KeyDetails(const InternalKeys Input, const std::string ILongName, const std::string& IShortName, const int KFlags = 0, const std::string Menu = "")
        {
            LongName = ILongName;
            ShortName = IShortName;
            IKey = Input;
            MenuCategory = Menu;
            ShortName = IShortName;

            Private_Init(KFlags);
        }


        private:

            enum class InputAxisType
            {
                Null,
                Button,
                Axis1D,
                Axis2D,
                Axis3D,
            }

            // Set all internal key properties
            void Private_Init(int KeyFlag)
            {
                // Set Boolean values
                IsModifierKey = (KeyFlag & Flags::ModifierKey != 0);
                IsMouseButton = (KeyFlag & Flags::MouseButton != 0);

                // Set Axis Type

                if(KeyFlag & Flags::Axis1D != 0)
                {
                    AxisType = InputAxisType::Axis1D;
                }
                else if(KeyFlag & Flags::Axis2D != 0)
                {
                    AxisType = InputAxisType::Axis2D;
                }
                else if(KeyFlag & Flags::Axis3D != 0)
                {
                    AxisType = InputAxisType::Axis3D;
                }
                else
                {
                    AxisType = InputAxisType::Null;
                }
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

    // ----- Declaring Keys ----- //

    // Global

    static const InternalKeys AnyKey;

    // Letters

    static const InternalKeys A;
    static const InternalKeys B;
    static const InternalKeys C;
    static const InternalKeys D;
    static const InternalKeys E;
    static const InternalKeys F;
    static const InternalKeys G;
    static const InternalKeys H;
    static const InternalKeys I;
    static const InternalKeys J;
    static const InternalKeys K;
    static const InternalKeys L;
    static const InternalKeys M;
    static const InternalKeys N;
    static const InternalKeys O;
    static const InternalKeys P;
    static const InternalKeys Q;
    static const InternalKeys R;
    static const InternalKeys S;
    static const InternalKeys T;
    static const InternalKeys U;
    static const InternalKeys V;
    static const InternalKeys W;
    static const InternalKeys X;
    static const InternalKeys Y;
    static const InternalKeys Z;

    // Numbers

    static const InternalKeys Zero;
    static const InternalKeys One;
    static const InternalKeys Two;
    static const InternalKeys Three;
    static const InternalKeys Four;
    static const InternalKeys Five;
    static const InternalKeys Six;
    static const InternalKeys Seven;
    static const InternalKeys Eight;
    static const InternalKeys Nine;
    static const InternalKeys Ten;

    // Numpads

    static const InternalKeys NumPadZero;
    static const InternalKeys NumPadOne;
    static const InternalKeys NumPadTwo;
    static const InternalKeys NumPadThree;
    static const InternalKeys NumPadFour;
    static const InternalKeys NumPadFive;
    static const InternalKeys NumPadSix;
    static const InternalKeys NumPadSeven;
    static const InternalKeys NumPadEight;
    static const InternalKeys NumPadNine;
    static const InternalKeys NumPadTen;

    // F Keys

    static const InternalKeys F1;
    static const InternalKeys F2;
    static const InternalKeys F3;
    static const InternalKeys F4;
    static const InternalKeys F5;
    static const InternalKeys F6;
    static const InternalKeys F7;
    static const InternalKeys F8;
    static const InternalKeys F9;
    static const InternalKeys F10;
    static const InternalKeys F11;
    static const InternalKeys F12;

    // Control keys

    // Math Keys

    // Common

    // Arrows

    // Etc

    // Mouse Axis

    // Mouse Buttons

    // ---------------- //

    std::string Keyboard_Category;
    std::string Mouse_Category;

    };
}

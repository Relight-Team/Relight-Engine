#pragma once

#include "Core.h"
#include "InputCore_Types.h"
#include <iostream>

namespace INPUTCORE_API
{
    class GlobalInput
    {
        public:

        int GetKeyMap(int Codes, std::string Names, int MaxMap)
        {
            return -1;
        }

        int GetKeCharyMap(int Codes, std::string Names, int MaxMap)
        {
            return -1;
        }

        private:
    }

}

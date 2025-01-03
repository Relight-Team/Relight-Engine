#pragma once

#include "Core.h"
#include "SDL.h"

#include <iostream>

class LinuxInput
{
    public:
        int GetKeyMap(std::string* ANames, int* AKeys, int AMapMax)
        {
            Names = ANames;
            Keys = *AKeys;
            MaxMap = AMapMax;
            NumberMap = 0;


        }

    private:

        int NumberMap;
        int MaxMap;
        int Keys;
        std::string Names;

        void AddKeyMap(Code, Name)
        {
            if(NumberMap < MaxMap)
            {
                Keys[NumberMap] = Code;
                Names[NumberMap] = Name;
                NumberMap++;
            }
        }


};

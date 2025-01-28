#pragma once
#include "Log/Log.h"
#include <iostream>
#include <vector>


// Note, params for getting values in configs
// ------------------------------------------------
// PClass: the config class the value is stored in
// Value: the value name from the class to get
// Store: The value to store the config
// File: The file location that stores the configs

class Config
{

    public:

        // Get values

        static void GetString(std::string PClass, std::string Value, std::string& Store, std::string File);


        static void GetInt(std::string PClass, std::string Value, int& Store, std::string File);


        static void GetDouble(std::string PClass, std::string Value, double& Store, std::string File);


        static void GetBool(std::string PClass, std::string Value, bool& Store, std::string File);

};

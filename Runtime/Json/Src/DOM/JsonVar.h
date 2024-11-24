#pragma once

#include "GlobalJson.h"
#include "Serialization/Types.h"
#include "DOM/JsonClass.h" // For storing
#include <iostream>
#include <typeinfo>

namespace JSON_API
{
    class JsonValue:
        public:

            // Constructer

            template <typename T> Input;
            JsonValue(Input VarInput, std::string NameInput)
            {
                Var = VarInput;
                Name = NameInput;
            }

            std::string GetName()
            {
                return Name;
            }

            bool TryGetNumber(int& Ref)
            {
                if(IsValid("int"))
                {
                    Ref = GetNumber();
                    return true;
                }
                else
                {
                    return false;
                }
            }

            bool TryGetNumber(double& Ref)
            {
                if(IsValid("double"))
                {
                    Ref = GetNumber();
                    return true;
                }
                else
                {
                    return false;
                }
            }

            bool TryGetString(std::string& Ref)
            {
                if(IsValid("std::string"))
                {
                    Ref = GetString();
                    return true;
                }
                else
                {
                    return false;
                }
            }

            bool TryGetBool(bool& Ref)
            {
                if(IsValid("bool"))
                {
                    Ref = GetBool();
                    return true;
                }
                else
                {
                    return false;
                }
            }

            std::string ReturnType()
            {
                return str(typeid(Var));
            }

            template <typename T> Any;

            // Will attempted to return the value, no matter what type it is

            bool TryGet(Any& Ref)
            {
                std::string Type = ReturnType();

                if(Type != "")
                {
                    if(Type == "int" || Type == "double")
                    {
                        return TryGetNumber(Ref);
                    }

                    if(Type == "std::string")
                    {
                        return TryGetString(Ref);
                    }
                    if(Type == "bool")
                    {
                        return TryGetBool(Ref);
                    }
                }
                return false;
            }

            //TODO: Array and Object support

        private:

            template <typename T> Var;

            std::string Name;

            // Get's

            int GetNumber()
            {
                return Var;
            }

            double GetNumber()
            {
                return Var;
            }

            std::string GetString()
            {
                return Var;
            }

            bool GetBool()
            {
                return Var;
            }


            bool IsValid(std::string Type)
            {
                if(typeid(Var) == typeid(Type))
                {
                    return true;
                }
                return false;
            }
}

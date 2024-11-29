#pragma once

#include "GlobalJson.h"
//#include "Serialization/Types.h"
#include "DOM/JsonClass.h" // For storing
#include <iostream>
#include <typeinfo>
#include <variant>

namespace JSON_API
{
    template <typename C>
    class JsonValue
    {
        public:

            // Constructer

            template <typename Input>
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
                    Ref = std::get<int>(Var);
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
                    Ref = std::get<double>(Var);
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
                return typeid(Var).name();
            }

            template <typename Any>

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

            std::variant<int, double, std::string, bool> Var;

            std::string Name;

            // Get's


            std::string GetString()
            {
                return std::get<std::string>(Var);
            }

            bool GetBool()
            {
                return std::get<bool>(Var);;
            }


            bool IsValid(std::string Type)
            {
                if(typeid(Var) == typeid(Type))
                {
                    return true;
                }
                return false;
            }
    };
}

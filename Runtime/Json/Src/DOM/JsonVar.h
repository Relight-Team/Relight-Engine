#pragma once

#ifndef GlobalJson
#define GlobalJson

#include "GlobalJson.h"

#endif


#pragma once
//#include "Serialization/Types.h"
#include "DOM/JsonClass.h" // For storing
#include "Core.h"
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

            JsonValue(std::variant<int, std::string, double, bool> VarInput)
            {
                Var = VarInput;
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
                    JSON_INTERNAL::PrintJsonError(Error, "Json Value tried to get int, but instead got incompatible variable type instead");
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
                    JSON_INTERNAL::PrintJsonError(Error, "Json Value tried to get int, but instead got incompatible variable type instead");
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
                    JSON_INTERNAL::PrintJsonError(Error, "Json Value tried to get int, but instead got incompatible variable type instead");
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
                    JSON_INTERNAL::PrintJsonError(Error, "Json Value tried to get int, but instead got incompatible variable type instead");
                    return false;
                }
            }

            std::string ReturnType()
            {
                return typeid(Var).name();
            }

            template <typename Any>

            // Will attempted to return the value, no matter what type it is

            //TODO: What I manage to get when asking the issue to ChatGPT for the 100000 time, now it brings up no errors? Anyways, because it's AI, it could be unstable. Please review this code!

            bool TryGet(Any& Ref)
            {
                // Check the type of 'Var' using holds_alternative
                if (std::holds_alternative<int>(Var))
                {
                    if constexpr (std::is_same_v<Any, int>)
                    {
                        Ref = std::get<int>(Var);
                        return true;
                    }
                }
                else if (std::holds_alternative<double>(Var))
                {
                    if constexpr (std::is_same_v<Any, double>)
                    {
                        Ref = std::get<double>(Var);
                        return true;
                    }
                }
                else if (std::holds_alternative<std::string>(Var))
                {
                    if constexpr (std::is_same_v<Any, std::string>)
                    {
                        Ref = std::get<std::string>(Var);
                        return true;
                    }
                }
                else if (std::holds_alternative<bool>(Var))
                {
                    if constexpr (std::is_same_v<Any, bool>)
                    {
                        Ref = std::get<bool>(Var);
                        return true;
                    }
                }

                return false;  // If the types do not match
            }

            //TODO: Array and Object support

        private:

            std::variant<int, std::string, double, bool> Var;

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

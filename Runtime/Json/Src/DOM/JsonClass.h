#pragma once

#ifndef GlobalJson
#define GlobalJson

#include "GlobalJson.h"

#endif

#include "GlobalJson.h"
#include "DOM/JsonVar.h"
#include "Core.h"
#include <iostream>
#include <typeinfo>
#include <map>
#include <variant>

namespace JSON_API
{
    class JsonObject
    {

        public:

            template <typename A>
            void AddValue(std::string& Name, JsonValue<A>& Value)
            {
                A Tmp;
                Value.TryGet(Tmp);
                JsonMap[Name] = Tmp;
            }

            void RemoveValue(std::string& Name)
            {
                JsonMap.erase(Name);
            }


            // Only check for name
            bool ValueExist(std::string& Name)
            {
                if(JsonMap.find(Name) != JsonMap.end())
                {
                    return true;
                }
                return false;
            }

            template <typename A>
            void SetValue(std::string& Name, JsonValue<A>& Value)
            {
                AddValue(Name, Value);
            }

            // ValueTypeExist will check for both Name AND type
            bool ValueTypeExist(std::string& Type, std::string& Name)
            {
                for(const auto& Pair : JsonMap)
                {
                    if(Pair.first == Name && typeid(Pair.second).name() == Type)
                    {
                        return true;
                    }
                }
                return false;
            }





            // please make this work


            bool TryGetNumber(std::string Key, int& Output)
            {
                auto i = JsonMap.find(Key);

                if (i == JsonMap.end())
                {
                    JSON_INTERNAL::PrintJsonError(Error, "Couldn't find " + Key + " key when running TryGetNumber()");
                    return false;
                }


                if (auto p = std::get_if<int>(&i->second))
                {
                    Output = *p;
                    JSON_INTERNAL::PrintJsonError(Log, "Successfully retrieved " + Key + " as int: " + std::to_string(Output));
                    return true;
                }


                JSON_INTERNAL::PrintJsonError(Error, "Attempting to get " + Key + " key as a int, but got " + typeid(i->second).name() + " instead");
                return false;


                if(i != JsonMap.end())
                {
                    int a;
                    VarientToInt(i->second, a);

                    Output = a;
                    return true;
                }
                return false;
            }

            // TODO: Array and Object support


            // set's

            void SetNumber(std::string Name, int Input)
            {
                JsonMap[Name] = Input;
            }

            void SetNumber(std::string Name, double Input)
            {
                JsonMap[Name] = Input;
            }

            void SetString(std::string Name, std::string Input)
            {
                JsonMap[Name] = Input;
            }

            void SetBool(std::string Name, bool Input)
            {
                JsonMap[Name] = Input;
            }

        private:

            using ValueType = std::variant<int, std::string, double, bool>;

            std::map<std::string, ValueType> JsonMap;

    };


}

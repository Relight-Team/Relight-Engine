#pragma once
#include "GlobalJson.h"
#include "DOM/JsonVar.h"
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

                // If the type is incorrect, return error

                if(typeid(i->second).name() != "int")
                {
                    return false;
                }


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

            using ValueType = std::variant<int, double, std::string, bool>;

            std::map<std::string, ValueType> JsonMap;

    };


}

#include "GlobalJson.h"
#include "DOM/JsonVar.h"
#include <iostream>
#include <typeinfo>
#include <map>
#include <variant>

namespace JSON_API
{
    class JsonObject:

        public:

            void AddValue(std::string& Name, JsonValue& Value)
            {
                template <typename T> T;

                JsonMap[Name] = Value.TryGet(T);
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

            void SetValue(std::string& Name, JsonValue& Value)
            {
                AddValue(Name, Value);
            }

            // ValueTypeExist will check for both Name AND type
            bool ValueTypeExist(std::string& Type, std::string& Name)
            {
                for(const auto& Pair : JsonMap)
                {
                    if(Pair.first == Name && typeid(Pair.second) == Type)
                    {
                        return true;
                    }
                }
                return false;
            }


            // Get stuff from map

            int GetNumber(std::string Key)
            {
                return JsonMap.find(Key);
            }

            // please make this work

            double GetNumberDouble(std::string Key)
            {
                return JsonMap.find(Key);
            }

            bool TryGetNumber(std::string Key, int& Output)
            {
                i = GetNumber(Key)

                if(i != JsonMap.end())
                {
                    Output = i;
                    return true
                }
                return false
            }

            bool TryGetNumber(std::string Key, double& Output)
            {
                i = GetNumberDouble(Key)

                if(i != JsonMap.end())
                {
                    Output = i;
                    return true
                }
                return false
            }

            bool TryGetString(std::string Key, std::string& Output)
            {
                i = JsonMap.find(Key)

                if(i != JsonMap.end())
                {
                    Output = i;
                    return true
                }
                return false
            }

            bool TryGetBool(std::string Key, bool& Output)
            {
                i = JsonMap.find(Key)

                if(i != JsonMap.end())
                {
                    Output = i;
                    return true
                }
                return false
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



}

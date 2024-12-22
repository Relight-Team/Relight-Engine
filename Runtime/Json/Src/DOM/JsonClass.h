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
                JsonMap.SetAdd(Name, Tmp);
            }

            void RemoveValue(std::string& Name)
            {
                JsonMap.Remove(Name);
            }


            // Only check for name
            bool ValueExist(std::string& Name)
            {
                if(JsonMap.Exist(Name))
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
                for(int i = 0; i < JsonMap.Size(); i++)
                {
                    if(JsonMap.First(i) == Name && typeid(JsonMap.Second(i)).name() == Type)
                    {
                        return true;
                    }
                }
                return false;
            }





            // please make this work



            // set's

            void SetNumber(std::string Name, int Input)
            {
                JsonMap.SetAdd(Name, Input);
            }

            void SetNumber(std::string Name, double Input)
            {
                JsonMap.SetAdd(Name, Input);
            }

            void SetString(std::string Name, std::string Input)
            {
                JsonMap.SetAdd(Name, Input);
            }

            void SetBool(std::string Name, bool Input)
            {
                JsonMap.SetAdd(Name, Input);
            }

        private:

            using ValueType = std::variant<int, std::string, double, bool>;

            Map<std::string, JsonValue<std::variant<ValueType>>> JsonMap;

    };


}

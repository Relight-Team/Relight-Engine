#pragma once

#ifndef GlobalJson
#define GlobalJson

#include "GlobalJson.h"

#endif

#include "CoreMinimal.h"

#include "Serial/JsonTypes.h"

#include <string>


namespace JSON_API
{
    class JsonValue
    {
        public:

        JsonValue()
        {
            EnumJson = ENGINE_INTERNAL::Enum_Json::None;
        }

        double AsNumber()
        {
            double Number = 0.0;

            if(!(GetNumber(Number)))
            {
                ErrorMessage("Number");
            }
            return Number;
        }

        virtual const bool GetNumber(int& Output)
        {
            if(GetType() == "Number")
            {
                Output = 0;
                return true;
            }
            return false;
        }

        virtual const bool GetNumber(double& Output)
        {
            if(GetType() == "Number")
            {
                Output = 0.0;
                return true;
            }
            return false;
        }

        virtual const bool GetString(std::string& Output)
        {
            if(GetType() == "String")
            {
                Output = "";
                return true;
            }
            return false;
        }

        virtual const bool GetBool(bool& Output)
        {
            if(GetType() == "Boolean")
            {
                Output = false;
                return true;
            }
            return false;
        }

        virtual const bool GetArray(void* Output)
        {
            if(GetType() == "Array")
            {
                Output = 0;
                return true;
            }
            return false;
        }

        const bool IsNull()
        {
         return (EnumJson == ENGINE_INTERNAL::Enum_Json::None || EnumJson == ENGINE_INTERNAL::Enum_Json::Null);
        }

        ENGINE_INTERNAL::Enum_Json EnumJson;

        protected:

            //virtual ~JsonValue();

            virtual std::string GetType()
            {
                return "";
            }

            const void ErrorMessage(std::string Input)
            {
                JSON_INTERNAL::PrintJsonError(Error, "Json Value is '" + GetType() + "' but is being treated as a '" + Input + "' instead.");
            }
    };

    class JsonValueNull : public JsonValue
    {
        public:
            JsonValueNull()
            {
                EnumJson = ENGINE_INTERNAL::Enum_Json::Null;
            }

        protected:
            virtual std::string GetType() override
            {
                return "Null";
            }
    };

    class JsonValueNumber : public JsonValue
    {
        public:

            JsonValueNumber(double Input)
            {
                Value = Input;
            }

            virtual const bool GetNumber(double& Output) override
            {
                Output = Value;
                return true;
            }

            virtual const bool GetNumber(int& Output) override
            {
                Output = (int)Value;
                return true;
            }

            virtual const bool GetBool(bool& Output) override
            {
                if(Value == 0.0)
                {
                    Output = false;
                }
                else
                {
                    Output = true;
                }
                return true;
            }

            virtual const bool GetString(std::string& Output) override
            {
                Output = std::to_string(Value);
                return true;
            }

        protected:

            double Value;

            virtual std::string GetType() override
            {
                return "Number";
            }
    };

    class JsonValueBool : public JsonValue
    {
        public:

            JsonValueBool(bool Input)
            {
                Value = Input;
            }

            virtual const bool GetNumber(double& Output) override
            {
                if(Value == true)
                {
                    Output = 1;
                }
                else
                {
                    Output = 0;
                }
                return true;
            }

            virtual const bool GetNumber(int& Output) override
            {
                if(Value == true)
                {
                    Output = 1;
                }
                else
                {
                    Output = 0;
                }
                return true;
            }

            virtual const bool GetBool(bool& Output) override
            {
                Output = Value;
                return true;
            }

            virtual const bool GetString(std::string& Output) override
            {
                if(Value == true)
                {
                    Output = "true";
                }
                else
                {
                    Output = "false";
                }
                return true;
            }

        protected:

            bool Value;

            virtual std::string GetType() override
            {
                return "Boolean";
            }
    };


    template <typename T>
    class JsonValueArray : public JsonValue
    {
        public:

            JsonValueArray(Array<T> Input)
            {
                Value = Input;
            }

            virtual const bool GetArray(Array<T>& Output) override
            {
                Value = Output;
                return true;
            }

        protected:

            Array<T> Value;

            virtual std::string GetType() override
            {
                return "Array";
            }
    };
}

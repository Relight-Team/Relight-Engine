using namespace std;
#pragma once
#include "Containers/String.h"
// LogCategory
namespace CORE_API
{

    class LogCategory
    {
        public:
            LogCategory() = default;

            LogCategory(String Name)
            {
                HName = Name;
            }

            void SetName(String Name)
            {
                HName = Name;
            }

            String GetName()
            {
                return HName;
            }

        private:
            String HName;
    };

}

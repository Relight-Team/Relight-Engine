#include <iostream>
#include <string>

using namespace std;

// LogCategory



namespace CORE_API
{

    class LogCategory
    {
        public:
            LogCategory(string Name)
            {
                HName = Name;
            }

            void SetName(string Name)
            {
                HName = Name;
            }

            std::string GetName()
            {
                return HName;
            }

        private:
            string HName;
    };

}

#pragma once
#include "Containers/String.h"
#include "Containers/Array.h"
#include "BasePlatform/BasePlatformMisc.h"

class UnixPlatformMisc : public BasePlatformMisc
{
    public:

        static bool ExeDir(String& Output)
        {

            // Get Running exe path
            char Path[PATH_MAX];
            ssize_t Size = readlink("/proc/self/exe", Path, PATH_MAX);

            if(Size == -1)
            {
               return false;
            }

            Path[Size] = '\0';

            // Convert it to Array
            Array<char> RetArr;

            for(int I = 0; I < Size; I++)
            {
                RetArr.Add(Path[I]);
            }

            // Split it
            int LastInd;

            bool Check = RetArr.FindLast('/', LastInd);

            if(Check == false)
            {
                return false;
            }

            // Convert back to String
            String Ret;
            for(int I = 0; I < LastInd; I++)
            {
                Ret.Append(RetArr[I]);
            }


            Output = Ret;
            return true;
        }

        static bool ConfigDir(String& Output)
        {
            String Ret;
            bool Check = ExeDir(Ret);
            if(Check == false)
            {
                return false;
            }
            Output = Ret + "/Config";
            return true;
        }

        static bool ContentDir(String& Output)
        {
            String Ret;
            bool Check = ExeDir(Ret);
            if(Check == false)
            {
                return false;
            }
            Output = Ret + "/Content";
            return true;
        }

        static bool ShaderDir(String& Output)
        {
            String Ret;
            bool Check = ExeDir(Ret);
            if(Check == false)
            {
                return false;
            }
            Output = Ret + "/Shader";
            return true;
        }

        static bool SavedDir(String& Output)
        {
            String Ret;
            bool Check = ExeDir(Ret);
            if(Check == false)
            {
                return false;
            }
            Output = Ret + "/Saved";
            return true;
        }

        static bool SavedConfigDir(String& Output)
        {
            String Ret;
            bool Check = ExeDir(Ret);
            if(Check == false)
            {
                return false;
            }
            Output = Ret + "/Saved/Config";
            return true;
        }

        static bool EngineDir(String& Output)
        {
            String Ret;
            bool Check = ExeDir(Ret);
            if(Check == false)
            {
                return false;
            }
            Output = Ret + "/Engine";
            return true;
        }
};

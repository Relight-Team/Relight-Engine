#include "Core.h"

// store config file

std::string Wrap;



//LOG(JSONWRAPPER_ERR, FATAL, "");


void Init()
{
    if(Wrap == "nlohmann")
    {
        #include "nlohmannWrap/NlohmannCommon.h"
    }
    else
    {
        LOG(JSONWRAPPER_ERR, FATAL, "Incorrect or unable to read Json Wrapper config");
    }

    Config::GetString("Relight/Wrappers", JSON, Wrap, std::string(ENGINEDIR) + "/Configs/Wrapper.cfg");

    CORE_API::LogCategory* JSONWRAPPER_ERR = new CORE_API::LogCategory("JSON WRAPPER");
}

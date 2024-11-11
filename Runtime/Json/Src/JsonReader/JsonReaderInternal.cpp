#include <iostream>
#include <fstream>
#include <vector>

#include "Log/Log.h"


CORE_API::LogCategory* JSON_PARSE_ERR = new CORE_API::LogCategory("JSON PARSING");

// Relight's own json parsing function //

// each value will be stored like this
// "ValueString=hi | ValueInt=5 | ValueDoubleFloat=1.1 | ValueBool=true | ValueArray=[1, 2, 3, 4]

// if it's a structure, it will look like this
// ParentStructure.ChildStructure.Value=3


std::vector<std::string> Parse(std::string JsonFile)
{

}

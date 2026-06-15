#pragma once
#include "Templates/Template.h"
#include "Templates/Invoke.h"
namespace CORE_API::Internal::FunctionRunner
{

    template <typename FunctionObjType, typename ReturnType, typename... ParamTypes>
    struct FunctionRunner
    {
        static ReturnType Run(void* Obj, ParamTypes... Params)
        {
            // So I had to use look up a lot to get help with this
            // this is the best result.
            // In the first *, we are casting back to original callable type
            // In the FunctionObjType pointer, we are dereferecing back to actual callable object
            // The Forward on param types ensures that all original references and value category
            // Google is your friend
            return Invoke(*(FunctionObjType*)Obj, Params...);
        }
    };
}

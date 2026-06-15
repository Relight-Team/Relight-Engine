#pragma once

// A system that manages and owns a callable object
namespace CORE_API::Internal::FunctionReference
{
    struct CallableObjectOwnerBase
    {
        virtual ~CallableObjectOwnerBase() = default;

        virtual void* GetAddress() = 0;
        virtual void Destroy() = 0;
    };
}

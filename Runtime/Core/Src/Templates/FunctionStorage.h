#pragma once
#include "RemoveReference.h"

// A system that holds how a function should be holded (I.E raw pointer, heap, inline, etc)
namespace CORE_API::Internal::FunctionReference
{
    struct FunctionStorageBase
    {
        virtual void* GetPointer() const = 0;

        virtual void Unbind() = 0;
    };

    struct FunctionReferenceStorage : public FunctionStorageBase
    {

        // Binds the reference to the function, return's the pointer to the function (with references removed)
        template <typename AnyCallableObject>
        typename RemoveReference<AnyCallableObject>::Type* Bind(AnyCallableObject& Input)
        {
            FunctionPointer = (void*)&Input;
            return &Input;
        }

        template <typename AnyCallableObject>
        typename RemoveReference<AnyCallableObject>::Type* Bind(AnyCallableObject&&) = delete;

        // Return's the pointer
        void* GetPointer() const override
        {
            return FunctionPointer;
        }

        // When unbinding, set the pointer to null
        void Unbind() override
        {
            FunctionPointer = nullptr;
        }

        private:

            void* FunctionPointer = nullptr;
    };
}

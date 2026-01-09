#pragma once
#include "Containers/String.h"
#include "Etc/ToString.h"
#include "Serialization/Archive.h"
#include <type_traits>

namespace CORE_API
{
namespace Math
{
// 3 value class for position, rotations, scaling, and much more (X, Y, Z)
template <typename FloatType>
class Vector
{
    union
    {
        struct
        {
            // (X, Y, Z)
            FloatType X;
            FloatType Y;
            FloatType Z;
        };
    };

public:
    Vector()
    {
        X = 0;
        Y = 0;
        Z = 0;
    }

    Vector(FloatType InX, FloatType InY, FloatType InZ)
    {
        X = InX;
        Y = InY;
        Z = InZ;
    }

    Vector(FloatType All)
    {
        X = All;
        Y = All;
        Z = All;
    }

    String ToString()
    {
        String StrX = CORE_API::ToString(X);
        String StrY = CORE_API::ToString(Y);
        String StrZ = CORE_API::ToString(Z);

        return "(" + StrX + ", " + StrY + ", " + StrZ + ")";
    }

    FloatType GetX()
    {
        return X;
    }

    FloatType GetY()
    {
        return Y;
    }

    FloatType GetZ()
    {
        return Z;
    }

    void SetX(FloatType Input)
    {
        X = Input;
    }

    void SetY(FloatType Input)
    {
        Y = Input;
    }

    void SetZ(FloatType Input)
    {
        Z = Input;
    }

    void Set(FloatType InX, FloatType InY, FloatType InZ)
    {
        X = InX;
        Y = InY;
        Z = InZ;
    }

    bool Serialize(Archive& Container)
    {
        Container.Serialize(*this);
        return true;
    }



};
}
}

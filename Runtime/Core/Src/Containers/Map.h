// RELIGHT ENGINE'S MAP SYSTEM!


#pragma once

#include "Log/Log.h"

#include "Containers/Array.h"

template <typename KeyType, typename ValueType>

class Map
{

    public:

    // Read

    // Write


    // Set's a value, if it doesn't exist, add it
    void SetAdd(KeyType K, ValueType V)
    {
        // Key found, replacing value with new value
        if(Key.Contains(K))
        {
            int i;
            K.find(K, i);
            Value[i] = V;
        }

        // Key not found, adding key with value
        else
        {
            Key.Add(K);
            Value.Add(V);
        }

    }

    // Operators

    ValueType& operator[](KeyType K)
    {
        if(Key.Contains(K))
        {
            int i;
            Key.Find(K, i);

            return Value[i];
        }
        return Value[0]; //TODO: Placeholder, this could cause errors, please find a ray for it to return something better
    }
    private:

        Array<KeyType> Key;

        Array<ValueType> Value;

        int SizeVal = 0;
};

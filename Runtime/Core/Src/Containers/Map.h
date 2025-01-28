// RELIGHT ENGINE'S MAP SYSTEM!

// Reminder: This is UNRELEATED to any level/world system, this is simply a Relight replacement for std::map


#pragma once

#include "Log/Log.h"

#include "Containers/Array.h"

#include <iostream>

CORE_API::LogCategory* Map_Error = new CORE_API::LogCategory("Map");

template <typename KeyType, typename ValueType>

class Map
{

    public:

    // Read

    int Size();

    bool Exist(KeyType Name);

    int Find(KeyType A);

    KeyType First(int i);

    ValueType Second(int i);

    // Write


    // Set's a value, if it doesn't exist, add it
    void SetAdd(KeyType K, ValueType V);

    void Remove(KeyType K);

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
};

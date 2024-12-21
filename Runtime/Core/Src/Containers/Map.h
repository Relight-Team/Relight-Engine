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

    int Size()
    {
        return Key.Size();
    }

    bool Exist(KeyType Name)
    {
        if(Key.Contains(Name))
        {
            return true;
        }
        return false;
    }

    int Find(KeyType A)
    {
        int i;
        Key.Find(A, i);
        return i;
    }

    KeyType First(int i)
    {
        return Key[i];
    }

    ValueType Second(int i)
    {
        return Value[i];
    }

    // Write


    // Set's a value, if it doesn't exist, add it
    void SetAdd(KeyType K, ValueType V)
    {
        // Key found, replacing value with new value
        if(Key.Contains(K))
        {
            int i;
            Key.Find(K, i);
            Value[i] = V;
        }

        // Key not found, adding key with value
        else
        {
            Key.Add(K);
            Value.Add(V);
        }

    }

    void Remove(KeyType K)
    {
        if(Key.Contains(K))
        {
            int i;
            Key.Find(K, i);
            Key.RemoveAt(i);
            Value.RemoveAt(i);
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
};

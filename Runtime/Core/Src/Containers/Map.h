// RELIGHT ENGINE'S MAP SYSTEM!


#pragma once

#include "Log/Log.h"

#include "Containers/Array.h"

#include <iostream>

template <typename KeyType, typename ValueType>

class Map
{

    public:

    // Read

    int Indices()
    {
        return Key.Indices();
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
        bool Err = Key.Find(A, i);

        if(Err == false)
        {
            return -1;
        }
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
            Value.Replace(V, i);
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

    Array<KeyType> GetKeys()
    {
        return Key;
    }

    Array<ValueType> GetValues()
    {
        return Value;
    }

    // Operators

    ValueType& operator[](const KeyType& K)
    {
        int i;
        if(Key.Contains(K))
        {
            Key.Find(K, i);
        }
        else
        {
            Key.Add(K);
            Value.Add(ValueType()); // default-constructed ValueType
            i = Value.Indices() - 1;
        }
        return Value[i];
    }
    private:

        Array<KeyType> Key;

        Array<ValueType> Value;

        int SizeVal = 0;
};

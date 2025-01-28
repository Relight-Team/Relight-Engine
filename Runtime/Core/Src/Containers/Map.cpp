// RELIGHT ENGINE'S MAP SYSTEM!

// Reminder: This is UNRELEATED to any level/world system, this is simply a Relight replacement for std::map

#include "Containers/Map.h"

#include "Log/Log.h"

#include "Containers/Array.h"

#include <iostream>

template <typename KeyType, typename ValueType>
int Map<KeyType, ValueType>::Size()
{
    return Key.Size();
}

template <typename KeyType, typename ValueType>
bool Map<KeyType, ValueType>::Exist(KeyType Name)
{
    if(Key.Contains(Name))
    {
        return true;
    }
    return false;
}

template <typename KeyType, typename ValueType>
int Map<KeyType, ValueType>::Find(KeyType A)
{
    int i;
    Key.Find(A, i);
    return i;
}


template <typename KeyType, typename ValueType>
KeyType Map<KeyType, ValueType>::First(int i)
{
    return Key[i];
}

template <typename KeyType, typename ValueType>
ValueType Map<KeyType, ValueType>::Second(int i)
{
    return Value[i];
}

template <typename KeyType, typename ValueType>
void Map<KeyType, ValueType>::SetAdd(KeyType K, ValueType V)
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

template <typename KeyType, typename ValueType>
void Map<KeyType, ValueType>::Remove(KeyType K)
{
    if(Key.Contains(K))
        {
            int i;
            Key.Find(K, i);
            Key.RemoveAt(i);
            Value.RemoveAt(i);
        }
}


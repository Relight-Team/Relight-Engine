// Owned by Relight Engine 2024
#include <iostream>
#include <vector>
#include <functional>



using namespace std;

template<typename T>

static std::vector<T> ConvertAllItems(std::vector<T> input, std::function<T(T)> func)
{
  vector<T> output(input.size());

  for(int i = 0; i < sizeof(input); i++)
    {
      output[i] = func(input[i]);
    }
  return output;
}

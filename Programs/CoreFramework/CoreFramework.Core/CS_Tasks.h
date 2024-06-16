// Owned by Relight Engine 2024


// this file handles both "task" and "token" classes from C# to C++, to make the codebase easier to read

#include <iostream>
#include <future>
#include <thread>
#include <functional>
#include <mutex>
#include <condition_variable>


template<typename T>
// task: allows for a function to be called asynchronously


class Task
{

  std::function<T> m_func;

  bool running = false;

  std::future<T> fut;


  public:
    Task(std::function<T()> func)
    {
      m_func = func;
    }


    void start()
    {
      if(!running)
      {
        running = true;
        fut = std::async(std::launch::async, m_func);
      }
    }

    void wait()
    {
      if(running)
      {
        fut.wait();
        running = false;
      }
    }

    void wait(int milisecs)
    {
      if(running)
      {
        fut.wait(milisecs);
        running = false;
      }
    }

    void delay(int milisecs)
    {
      std::this_thread::sleep_for(std::chrono::milliseconds(milisecs));
      fut();
    }
};

template<typename T>

// TODO: Need help with this part, as the original functions highly relies on .NET, and idk what 'token' means in the context of C#.
class CancellationToken
{
  std::mutex m_mutex;
  std::condition_variable m_cond;

  std::future<T> fut;

  bool m_cancelled = false;

  public:
      bool IsCancellationRequested()
      {
        return m_cancelled;
      }

      std::future<T> getToken()
      {
        return fut;
      }
};
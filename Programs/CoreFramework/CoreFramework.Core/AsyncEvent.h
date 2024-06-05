// Owned by Relight Engine 2024
#include <iostream>
#include <future>
#include <atomic>



class AsyncEvent
{
  public:
    std::promise<bool> promise;

    // Get the future associated with the promise
    std::future<bool> future = promise.get_future();


    //TODO:
    // No idea how to test the original code... or this one, no idea if this even works correctly
// find a way to test the original code to  compare
    void Start()
      {
        std::future<bool> PrevFuture = promise.get_future();
        
        while(true)
          {
            if(IsComplete(PrevFuture))
            {
              break;
            }          
            std::atomic<bool> atomicVal(PrevFuture.valid());
            if(atomicVal.exchange(future.valid()) == PrevFuture.valid())
            {
              std::promise<bool> NewProm;
              NewProm.set_value(true);
              std::future<bool> PrevFuture = NewProm.get_future();
              break; 
            }
          }
      }

    void Restart()
    {
      while(true)
      {
        std::future<bool> PrevFuture = promise.get_future();
        std::atomic<bool> atomicVal(PrevFuture.valid());
        if(!IsComplete(PrevFuture))
        {
          break;
        }
        else if(atomicVal.exchange(future.valid()) == PrevFuture.valid())
        {
          break;
        }
      }
     
    }

    void ChangeToComplete()
    {
      promise.set_value(true);  
    }

    bool isReady()
    {
      return IsComplete(future);
    }

  private:
    bool IsComplete(std::future<bool>& fut)
      {
        if(fut.wait_for(std::chrono::milliseconds(0)) == std::future_status::ready)
        {
          return fut.get();
        }
        else
        {
          return false;
        }
      }
};

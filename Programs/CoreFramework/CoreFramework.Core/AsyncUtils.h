// Owned by Relight Engine 2024


#include "CS_Tasks.h"


template<typename T>



// Cancellation Token -> Task
static Task<T> ToTask(CancellationToken<T> token)
{
  Task<T> tmp = new Task<T>(token.getToken());
}

template<typename T>

static bool AttemptResult(Task<T> task, T& result)
{
  if(task.isCompleted())
  {
    result *= task.get();
    return true;
  }
  else
  {
    result *= "default!";
    return false;
  }
}

// TODO: Finish the functions later

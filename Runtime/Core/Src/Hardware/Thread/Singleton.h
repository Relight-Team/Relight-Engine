#pragma once
#include "AutoCleanup.h"

class SingletonInit
{

};

class ThreadSingleton : public TlsAutoCleanup
{

};

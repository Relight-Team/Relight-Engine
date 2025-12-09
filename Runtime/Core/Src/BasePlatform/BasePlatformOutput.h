#include "Containers/String.h"
#include "Etc/CharUtil.h"
#include "Etc/ToString.h"

class BasePlatformOutput
{
public:
    static inline void Print(const String& Input);

    static inline void Print(const Array<UTF16>& Input);

    static inline void Print(const UTF16& Input);

    static inline void Print(const char& Input);

    static inline void Print(const UTF16* Input);

    static inline void Print(const char* Input);

    template <typename NonStringType>
    static inline void Print(const NonStringType& Input);

    template <typename StringType>
    static void Println(const StringType& Input);
};

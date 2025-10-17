#pragma once
#include "RangeBound.h"

// Range

// Range are like arrays, but contains 'lower bounds' and 'upper bounds'

// The range then fills in the gap between these 2 bounds

// This is very usefule for memory and performance

namespace CORE_API
{
    namespace Math
    {
        template<typename T>

        class Range
        {
          public:

            // [A, A]

            Range(T Both)
            {
                LowerBound = RangeBound<T>::Inclusive(Both);
                UpperBound = RangeBound<T>::Inclusive(Both);
            }

            // [A, B)

            Range(T Lower, T Higher)
            {
                LowerBound = RangeBound<T>::Inclusive(Lower);
                UpperBound = RangeBound<T>::Exclusive(Higher);
            }

            // Range determined by RangeBound

            Range(RangeBound<T> Lower, RangeBound<T> Higher)
            {
                LowerBound = Lower;
                UpperBound = Higher;
            }

            bool IsAdjoint(Range& Second)
            {
                if(UpperBound.IsNotOpen() && Second.LowerBound.IsNotOpen() && UpperBound.GetValue() == Second.LowerBound.GetValue())
                {
                    return (UpperBound.IsInclusive() && Second.LowerBound.IsExclusive()) || (UpperBound.IsExclusive && Second.LowerBound.IsInclusive());
                }

                else if(Second.UpperBound.IsNotOpen() && LowerBound.IsNotOpen() && Second.UpperBound.GetValue() == LowerBound.GetValue())
                {
                    return (Second.UpperBound.IsInclusive() && LowerBound.IsExclusive()) || (Second.UpperBound.IsExclusive && LowerBound.IsInclusive());
                }
                else
                {
                    return false;
                }

            }

            bool Contains(T Value)
            {
                return (RangeBound<T>::LesserOfLow(LowerBound, Value) == LowerBound) && (RangeBound<T>::GreaterOfUp(UpperBound, Value) == UpperBound);
            }

          private:

            RangeBound<T> LowerBound;

            RangeBound<T> UpperBound;

        };
    }
}

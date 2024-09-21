// Range Bound

// Handles bound values for Range


namespace CORE_API
{
    namespace Math
    {
        #pragma once
        enum RangeBoundType
        {
            Inclusive,
            Exclusive,
            Open
        };

        template<typename T>
        class RangeBound
        {
          public:

            RangeBound()
            {
                Type = RangeBoundType::Open;
            }

            RangeBound(T Value)
            {
                Bound = Value;
                Type = RangeBoundType::Inclusive;
            }

            bool IsNotOpen()
            {
                if(Type != RangeBoundType::Open)
                {
                    return true;
                }
                return false;
            }

            T ReturnNotOpen()
            {
                if(IsNotOpen())
                {
                    return Bound;
                }
            }

            void SetNotOpen(T Value)
            {
                if(IsNotOpen())
                {
                    Bound = Value;
                }
            }

            bool IsInclusive()
            {
                if(Type == RangeBoundType::Inclusive)
                {
                    return true;
                }
                return false;
            }

            bool IsExclusive()
            {
                if(Type == RangeBoundType::Exclusive)
                {
                    return true;
                }
                return false;
            }

            bool IsOpen()
            {
                if(Type == RangeBoundType::Open)
                {
                    return true;
                }
                return false;
            }

            T GetValue()
            {
                if(Type != RangeBoundType::Open)
                {
                    return Bound;
                }
            }

            static RangeBound LesserOfLow(RangeBound Range1, RangeBound Range2)
            {
                if(Range1.IsOpen())
                {
                    return Range1;
                }

                else if(Range2.IsOpen())
                {
                    return Range2;
                }

                else if(Range1.GetValue > Range2.GetValue)
                {
                    return Range2;
                }

                else if(Range1.GetValue < Range2.GetValue)
                {
                    return Range1;
                }

                else if(Range1.IsInclusive())
                {
                    return Range1;
                }
                else
                {
                    return Range2;
                }
            }

            static RangeBound GreaterOfLow(RangeBound Range1, RangeBound Range2)
            {
                if(Range1.IsOpen())
                {
                    return Range2;
                }

                else if(Range2.IsOpen())
                {
                    return Range1;
                }

                else if(Range1.GetValue > Range2.GetValue)
                {
                    return Range1;
                }

                else if(Range1.GetValue < Range2.GetValue)
                {
                    return Range2;
                }

                else if(Range1.IsInclusive())
                {
                    return Range1;
                }
                else
                {
                    return Range2;
                }
            }



            static RangeBound LesserOfUp(RangeBound Range1, RangeBound Range2)
            {
                if(Range1.IsOpen())
                {
                    return Range2;
                }

                else if(Range2.IsOpen())
                {
                    return Range1;
                }

                else if(Range1.GetValue > Range2.GetValue)
                {
                    return Range2;
                }

                else if(Range1.GetValue < Range2.GetValue)
                {
                    return Range1;
                }

                else if(Range1.IsInclusive())
                {
                    return Range1;
                }
                else
                {
                    return Range2;
                }
            }


            static RangeBound GreaterOfUp(RangeBound Range1, RangeBound Range2)
            {
                if(Range1.IsOpen())
                {
                    return Range1;
                }

                else if(Range2.IsOpen())
                {
                    return Range2;
                }

                else if(Range1.GetValue > Range2.GetValue)
                {
                    return Range1;
                }

                else if(Range1.GetValue < Range2.GetValue)
                {
                    return Range2;
                }

                else if(Range1.IsInclusive())
                {
                    return Range1;
                }
                else
                {
                    return Range2;
                }
            }

        private:
            T Bound; // The Bound Value

            RangeBoundType Type;
        };
    }
}

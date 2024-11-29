#include "Core.h"

namespace JSON_API
{

enum ValueTypes
{
    None,
    String,
    Number,
    Boolean,
    Array,
    Object,
    Null
};

enum Token
{
    None,
    Number,
    String,
    True,
    False,
    Null,

    Comma,
    Colon,

    Identify,

    CurlyOpen,
    CurlyClose,
    SquareOpen,
    SquareClose

};

enum Notation
{
    Null,
    Error,

    Boolean,
    String,
    Number

    ArrayStart,
    ArrayEnd,

    ObjectStart,
    ObjectEnd

};

}

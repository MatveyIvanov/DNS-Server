using System;
using System.Collections.Generic;
using System.Text;

namespace DNS_Server
{
    enum DataType
    {
        Unicode,
        ASCII
    }
    class UDP
    {

        public static byte[] Build(string message, DataType dataType = DataType.Unicode)
        {
            switch (dataType)
            {
                case DataType.Unicode:
                {
                    return Encoding.Unicode.GetBytes(message); 
                }
                case DataType.ASCII:
                {
                    return Encoding.ASCII.GetBytes(message);
                }
            }
            return new byte[64];
        }
    }
}

using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;

namespace DNS_Server
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Введите порт для приема сообщений: ");
            int localPort = Int32.Parse(Console.ReadLine());
            Console.Write("Введите порт для отправки сообщений: ");
            int remotePort = Int32.Parse(Console.ReadLine());
            Console.Write("Введите адрес (IPv4), с которого принимать пакеты: ");
            string remoteIP = Console.ReadLine();

            Client client = new Client(localPort, remotePort, remoteIP);
            client.start();
        }
    }
}

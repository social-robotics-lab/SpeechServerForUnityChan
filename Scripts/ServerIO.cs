using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using UnityEngine;

public class ServerIO
{
    private NetworkStream stream;

    public ServerIO(NetworkStream stream)
    {
        this.stream = stream;
    }

    public byte[] Read()
    {
        int size = ReadSize();
        if (size == 0) return new byte[0];
        return ReadData(size);
    }

    public void write(byte[] data)
    {
        int size = data.Length;
        byte[] buf = System.BitConverter.GetBytes(size);
        stream.Write(buf, 0, 4);
        stream.Write(data, 0, size);
        stream.Flush();
    }


    private int ReadSize()
    {
        byte[] buf = new byte[4];
        int size = 0;
        while (size < 4)
        {
            size += stream.Read(buf, size, 4 - size);
        }
        Array.Reverse(buf);
        return BitConverter.ToInt32(buf, 0);
    }

    private byte[] ReadData(int dataSize)
    {
        byte[] buf = new byte[dataSize];
        int size = 0;
        while (size < dataSize)
        {
            size += stream.Read(buf, size, dataSize - size);
        }
        return buf;
    }



    
}

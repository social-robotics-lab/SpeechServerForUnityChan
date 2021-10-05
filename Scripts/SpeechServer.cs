using System;
using System.Collections.Concurrent;
using System.Net;
using System.Net.Sockets;
using System.Threading.Tasks;
using UnityEngine;

public class SpeechServer : MonoBehaviour
{
    public String ip = "0.0.0.0";
    public int port = 13000;

    private AudioSource audioSource;
    private ConcurrentQueue<byte[]> q;

    // Start is called before the first frame update
    void Start()
    {
        audioSource = gameObject.GetComponent<AudioSource>();

        // Queue for receiving data from the thread of 'recv'
        q = new ConcurrentQueue<byte[]>();

        // Server settings
        TcpListener server = new TcpListener(IPAddress.Parse(ip), port);
        server.Start();
        Task.Run(() => { 
            while (true)
            {
                TcpClient client = server.AcceptTcpClient();
                Task.Run(() => recv(client));
            }
        });
    }

    // Update is called once per frame
    void Update()
    {
        byte[] audioData;
        if (q.TryDequeue(out audioData))
        {
            AudioClip clip = WavUtility.ToAudioClip(audioData);
            audioSource.PlayOneShot(clip);            
        }
    }

    private void recv(TcpClient client)
    {
        try
        {
            NetworkStream stream = client.GetStream();
            ServerIO io = new ServerIO(stream);
            byte[] bytes = io.Read();
            q.Enqueue(bytes);
        }
        catch (SocketException e)
        {
            Console.WriteLine("SocketException: {0}", e);
        }
        finally
        {
            client.Close();
        }
    }





}

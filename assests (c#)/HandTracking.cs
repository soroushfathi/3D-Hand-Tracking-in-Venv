using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandTracking : MonoBehaviour
{
    // Start is called before the first frame update
    public UDPReceive updReceive;
    public GameObject[] handPoints;
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        string data = updReceive.data;
        data = data.Remove(0, 1);
        data = data.Remove(data.Length-1, 1);
        string[] points = data.Split(',');

        if (data.Length == 0) {
            for (int i=0; i<42; i++) {
                handPoints[i].transform.localPosition = new Vector3(0, 0, 0);
            }
        } else if (data.Length == 21) {
            for (int i=0; i<21; i++) {
                float x = float.Parse(points[i*3]) / 100 - 10;
                float y = float.Parse(points[i*3 + 1]) / 100 - 5;
                float z = - float.Parse(points[i*3 + 2]) / 4 + 10;
                handPoints[i].transform.localPosition = new Vector3(x, y, z);
            }
            for (int i=21; i<42; i++) {
                handPoints[i].transform.localPosition = new Vector3(0, 0, 0);
            }
        } else if (data.Length > 21) {
            for (int i=0; i<21; i++) {
                float x = float.Parse(points[i*3]) / 100 - 10;
                float y = float.Parse(points[i*3 + 1]) / 100 - 5;
                float z = - float.Parse(points[i*3 + 2]) / 4 + 10;
                handPoints[i].transform.localPosition = new Vector3(x, y, z);
            }
            for (int i=21; i<42; i++) {
                float x = float.Parse(points[i*3]) / 100 - 10;
                float y = float.Parse(points[i*3 + 1]) / 100 - 5;
                float z = - float.Parse(points[i*3 + 2]) / 4 + 10;
                handPoints[i].transform.localPosition = new Vector3(x, y, z);
            }
        } 
    }
}

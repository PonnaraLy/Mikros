using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class LineRendererScript : MonoBehaviour
{
    private LineRenderer line;
    public GameObject startPoint;
    public GameObject endPoint;
    private Vector3 startPointPos;
    private Vector3 endPointPos;
    public int nbPoints;
    private Vector3 AB;
    public Pause pauseScript;
    public float amplitude;

    void Start()
    {
        pauseScript = GameObject.Find("UIScript").GetComponent<Pause>();
        line = GetComponent<LineRenderer>();
        startPointPos = new Vector3(-1.75f, 0, 0);
        endPointPos = new Vector3(1.75f, 0,0);
        AB = endPointPos - startPointPos;

    }

    void Update()
    {
        
        line.sortingLayerName = "OnTop";
        line.sortingOrder = 5;
        line.numPositions = nbPoints + 1;
        line.widthMultiplier = 0.1f;

        for (int i = 0; i < nbPoints; i++)
        {
            Vector3 newPos;
            newPos = startPointPos + i * (AB / nbPoints);
            line.SetPosition(i, newPos);
        }
        line.SetPosition(nbPoints, endPointPos);
        if (Input.GetButtonDown("Jump"))
        {
            sinusCurve();
        }
    }

    //Create sinus on the line
    void sinusCurve()
    {
        
        for (int i=0;i< nbPoints; i++)
        {
            Vector3 newPos;
            float piRatio;
            newPos = startPointPos + i * (AB / nbPoints);
            piRatio = newPos.x * (Mathf.PI)/ endPointPos.x;
            if (i != 0) newPos.y = Mathf.Sin(piRatio)*amplitude;
            line.SetPosition(i, newPos);
        }
        line.SetPosition(nbPoints, endPointPos);
    }

}

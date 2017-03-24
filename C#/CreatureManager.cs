using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class CreatureManager : MonoBehaviour {

    //Lova variables
	private bool timeToLove;
    private float timer;
    public float timerBeforeLove;

    //Creatures List
    public GameObject[] creatureList;
    public List<string> tetesList = new List<string>();
    public List<string> corpsList = new List<string>();
    public List<Color> colorList = new List<Color>();

    public void addObjectOnArray(string _object, List<string> _objectList)
    {
        _objectList.Add(_object);
    }

    public void addColorOnArray(Color _color)
    {
        colorList.Add(_color);
    }

    public void removeObjectArray(string _object, List<string> _objectList)
    {
        _objectList.Remove(_object);
    }

    public void removeColorToArray(Color _color)
    {
        colorList.Remove(_color);
    }

    void Update () {
        loveManager();
	}

    //Love Manager
    void loveManager()
    {
        if (!timeToLove)
        {
            timer += Time.deltaTime;

            if (timer >= timerBeforeLove)
            {
                timeToLove = true;
                timer = 0.0f;
            }
        }
    }

    public void setTimeToLove(bool _love)
    {
        timeToLove = _love;
    }

    public bool isTimeToLove()
    {
        return timeToLove;
    }
}

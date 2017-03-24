using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/**
 * Creature Behaviour
 */

public class CreatureBehaviour : MonoBehaviour {
    public GameObject target;
    private float speed = 0.01f;

    int etat;

    private float timeToThink = 5.0f;
    private float timeThinking;

    private bool readyToKill;

    private bool hasMadeBaby;
    private bool inLove;

    private CreatureManager creaManagerScript;

    public bool parternerHasBaby()
    {
        return hasMadeBaby;
    }

    public void setPartnerBaby(bool _bool)
    {
        hasMadeBaby = _bool;
    }

	void Awake () {
        creaManagerScript = GameObject.Find("creatureManager").GetComponent<CreatureManager>();

        //Add Sparkling
        Quaternion rotation = Quaternion.identity;
        rotation.eulerAngles = new Vector3(270, 0, 0);
        GameObject sparkle = (GameObject)Instantiate(Resources.Load("SparklingParticle", typeof(GameObject)), new Vector3(0, 0, 0), rotation);
        sparkle.transform.parent =  gameObject.transform;
        sparkle.layer = LayerMask.NameToLayer("Oculus");
        sparkle.GetComponent<Particle>().playAndDestroyParticle();

        foreach (Transform child in transform.parent)
        {
            if (child.name == "Target")
            {
                target = child.gameObject;
            }
        }
    }

    void removeAttributesOnArray()
    {
        List<string> bodyToDelete = new List<string>();
        foreach (Transform child in transform.parent.GetChild(0))
        {
            string childString = child.ToString().Replace("(Clone) (UnityEngine.Transform)", "");
            bodyToDelete.Add(childString);
            
        }

        Debug.Log("Tete: " + bodyToDelete[0]);
        Debug.Log(transform.parent.GetChild(0).GetChild(0).FindChild("tete"));
        Debug.Log("Tete: " + bodyToDelete[1]);
        creaManagerScript.removeObjectArray(bodyToDelete[0], creaManagerScript.tetesList);
        creaManagerScript.removeObjectArray(bodyToDelete[1], creaManagerScript.corpsList);
        Color colorToRemove = transform.parent.GetChild(0).GetChild(0).FindChild("tete").GetComponent<Renderer>().material.color;

        creaManagerScript.removeColorToArray(colorToRemove);
    }

    void Update () {

        inLove = creaManagerScript.isTimeToLove();

        //Destroy Creature
        if(Input.GetKey("a") && readyToKill)
        {
            removeAttributesOnArray();
            GameObject particle = transform.Find("Explode(Clone)").gameObject;
            particle.GetComponent<Particle>().playAndDestroyParticle();
            particle.transform.parent = null;          
            Destroy(transform.parent.gameObject);
        }

        //Move
        switch (etat)
        {
            case 0:
                timeThinking += Time.deltaTime;
                if (timeThinking >= timeToThink)
                {
                    timeThinking = 0.0f;
                    etat = 1;
                }
                break;
            case 1:
                target.transform.position = getNewLocation();
                etat = 2;
                break;
            case 2:
                move(target);
                float dist = Vector3.Distance(target.transform.position, transform.position);
                if(dist<= 0.1)
                {
                    etat = 0;
                } 
                break;
        }
    }

    void move(GameObject _target)
    {
        transform.position = Vector3.Lerp(transform.position,target.transform.position,speed);
        transform.LookAt(target.transform);
    }

    Vector3 getNewLocation()
    {
        float x;
        float y;
        float z;
        Vector3 pos;

        x = Random.Range(-20, 20);
        y = 0;
        z = Random.Range(-20,20);
        pos = new Vector3(x, y, z);

        return pos;
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.tag == "PlayerOculus") {
            readyToKill = true;
        }

        if (other.tag == "Creature" && !hasMadeBaby && !other.gameObject.GetComponent<CreatureBehaviour>().parternerHasBaby())
        {
            birthCreature(transform.gameObject, other.gameObject);
            hasMadeBaby = true;
            other.gameObject.GetComponent<CreatureBehaviour>().setPartnerBaby(true);
            creaManagerScript.setTimeToLove(false);
        }
    }

    void OnTriggerExit(Collider other)
    {
        if (other.tag == "PlayerOculus")
        {
            readyToKill = false;
        }
        
    }

    void birthCreature(GameObject creature1, GameObject creature2)
    {
        string child1 = creature1.transform.GetChild(0).ToString();
        child1 = child1.Replace("(Clone) (UnityEngine.Transform)", "");
        string child2 = creature2.transform.GetChild(1).ToString();
        child2 = child2.Replace("(Clone) (UnityEngine.Transform)", "");

        //Generate a empty creature and his appearance
        GameObject mygameobject = new GameObject(generateCode());
        GameObject monsterAppeareance = new GameObject("Creature");
        GameObject tete = (GameObject)Instantiate(Resources.Load(child1, typeof(GameObject)), new Vector3(0, 3, 0), Quaternion.identity);
        tete.transform.localScale += new Vector3(3, 3, 3);
        tete.transform.parent = monsterAppeareance.transform;

        GameObject corps = (GameObject)Instantiate(Resources.Load(child2, typeof(GameObject)), new Vector3(0, 0.5f, 0), Quaternion.identity);
        corps.transform.parent = monsterAppeareance.transform;
        corps.transform.localScale += new Vector3(3, 3, 3);
        monsterAppeareance.transform.parent = mygameobject.transform;

        Material newMat = new Material(Shader.Find("Transparent/Diffuse"));
        newMat.color = new Color(Random.value, Random.value, Random.value, 1.0f);
        foreach (Transform child in tete.transform)
        {
            child.GetComponent<Renderer>().material = newMat;
        }
        corps.GetComponent<Renderer>().material = newMat;

        //Add values on creatureManager
        creaManagerScript.addObjectOnArray(child1, creaManagerScript.tetesList);
        creaManagerScript.addObjectOnArray(child2, creaManagerScript.corpsList);
        creaManagerScript.addColorOnArray(newMat.color);

        //Add the script CreatureBehaviour
        GameObject monsterTarget = new GameObject("Target");
        monsterTarget.transform.parent = mygameobject.transform;
        CreatureBehaviour creaBehaviour = monsterAppeareance.AddComponent<CreatureBehaviour>();
        monsterAppeareance.AddComponent<BoxCollider>();
        monsterAppeareance.GetComponent<BoxCollider>().isTrigger = true;

        //Add Explode
        GameObject explode = (GameObject)Instantiate(Resources.Load("Explode", typeof(GameObject)), new Vector3(0, 0, 0), Quaternion.identity);
        explode.GetComponent<ParticleSystem>().startColor = newMat.color;
        explode.transform.parent = monsterAppeareance.transform;

        //Place the creature
        mygameobject.transform.position = transform.position;
        monsterAppeareance.tag = "Creature";

        //Add the Creature in the "Creature List"
        mygameobject.transform.parent = GameObject.Find("Creatures").transform;

        //Set Layer
        foreach (Transform child in tete.transform)
        {
            child.gameObject.layer = LayerMask.NameToLayer("Oculus");
        }
        corps.layer = LayerMask.NameToLayer("Oculus");
        explode.layer = LayerMask.NameToLayer("Oculus");

    }

    string generateCode()
    {
        string characters = "0123456789abcdefghijklmnopqrstuvwxABCDEFGHIJKLMNOPQRSTUVWXYZ";
        int codeLength = 10;
        string code = "";

        for (int i = 0; i < codeLength; i++)
        {
            int a = Random.Range(0, characters.Length);
            code = code + characters[a];
        }

        return code;
    }
}

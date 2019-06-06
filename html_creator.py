from content_management import Content,Level1List
import os


TOPIC_DICT = Content()
LEVEL_1_DICT = Level1List()


# ORDER OF %S: "Basics" , "Basics", "Basics, "Basics"

HTML_TEMPLATE = """
{% extends "header.html" %}
{% block body %}
<!--       <pre class="prettyprint">              width="750" height="423"    -->


<body class="body">
    <div class="container" align="left" style="max-width:800px">
            <div class="jumbotron">
                <h1>DataSpark App</h1>
                <h2>Census Data</h2>
                <p class="lead"></p>
                <form action="/action_page.php">
                    {% for t in LEVEL_1_DICT %}
                        <select name = "{{ t }}">
                        {%for item in LEVEL_1_DICT[t]%}
                                <option value = "{{item}}">{{item}}</option>
                        {% endfor %}
                        </select>
                    {% endfor %}
                    <br><br>
                    <a class="btn btn-lg btn-success" href='/abs_tables' role="button">Table Select</a>
                </form>             
            </div>
        </div>
        <div class="row">
            <div class="col l6">
                <p></p>
            </div>
        </div>
    </div>
</body>

{% endblock %}

"""

for each_topic in TOPIC_DICT:
    print(each_topic)
    os.makedirs('tutorials'+'/'+each_topic)

    for eachele in TOPIC_DICT[each_topic]:
        try:

            filename = (eachele[1]+'.html').replace("/","")
            print(filename)
            savePath ='tutorials'+'/'+each_topic+'/'+filename

            saveData = (HTML_TEMPLATE.replace("%s",each_topic))

            template_save = open(savePath,"w")
            template_save.write(saveData)
            template_save.close()
        except Exception as e:
            print(str(e))


	  
	
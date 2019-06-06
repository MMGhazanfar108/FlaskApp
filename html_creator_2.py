from content_management import Content
import os


TOPIC_DICT = Content()


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
            <select name="Year">
               <option value="2016">2016</option>
               <option value="2011">2011</option>
            </select>
            <select name="Geographies">
               <option value="All">All</option>
               <option value="SA">SA</option>
               <option value="NSW">NSW</option>
               <option value="VIC">VIC</option>
            </select>
            <select name="By">
               <option value="PostCodes">PostCodes</option>
               <option value="Region">Region</option>
               <option value="Suburb">Suburb</option>
            </select>
            <br><br>
            <a class="btn btn-lg btn-success" href="item2.html" role="button">Catalog</a>
         </form>
      </div>
   </div>
   <div class="row">
      <div class="col l6">
         <pre  class="prettyprint">
CODE HERE
		</pre>
      </div>
      <div class="col l6">
         <p>EXPLANATION</p>
      </div>
   </div>
   <p>The next tutorial: <a title="{{nextTitle}}" href="{{nextLink}}?completed={{curLink}}"><button class="btn btn-primary">{{nextTitle}}</button></a></p>
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


	  
	
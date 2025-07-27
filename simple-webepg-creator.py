from flask import Flask, render_template_string, request
import xml.etree.ElementTree as ET

app = Flask(__name__)
programs = []

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head><title>Môj EPG editor</title></head>
<body>
  <h2>Pridaj program</h2>
  <form method="post">
    Názov: <input name="title"><br>
    Začiatok (YYYYMMDDHHMMSS +0200): <input name="start"><br>
    Koniec (YYYYMMDDHHMMSS +0200): <input name="stop"><br>
    Popis: <input name="desc"><br>
    <input type="submit" value="Pridať">
  </form>
  <h3>Pridané programy:</h3>
  <ul>
    {% for p in programs %}
      <li>{{p[1]}} - {{p[0]}}</li>
    {% endfor %}
  </ul>
  <form method="post" action="/export">
    <input type="submit" value="Exportovať do XMLTV">
  </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        start = request.form["start"]
        stop = request.form["stop"]
        desc = request.form["desc"]
        programs.append((title, start, stop, desc))
    return render_template_string(HTML_FORM, programs=programs)

@app.route("/export", methods=["POST"])
def export():
    tv = ET.Element("tv")
    channel = ET.SubElement(tv, "channel", id="my_channel")
    ET.SubElement(channel, "display-name").text = "Môj Kanál"

    for title, start, stop, desc in programs:
        programme = ET.SubElement(tv, "programme", {
            "start": start,
            "stop": stop,
            "channel": "my_channel"
        })
        ET.SubElement(programme, "title").text = title
        ET.SubElement(programme, "desc").text = desc

    tree = ET.ElementTree(tv)
    tree.write("moje_epg.xml", encoding="utf-8", xml_declaration=True)
    return "EPG bol exportovaný do 'moje_epg.xml'!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

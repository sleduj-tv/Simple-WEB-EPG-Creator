from flask import Flask, render_template, request, redirect, send_file
from datetime import datetime
import pytz
import xml.etree.ElementTree as ET

app = Flask(__name__)
programs = []
channels = {}

def get_texts(lang):
    translations = {
        "sk": {
            "lang_select": "Jazyk",
            "tz_select": "Časové pásmo",
            "add": "Pridaj program",
            "title": "Názov",
            "start": "Začiatok",
            "stop": "Koniec",
            "desc": "Popis",
            "channel": "TV kanál",
            "tvgid": "TVG-ID",
            "submit": "Pridať",
            "export": "Exportovať do XMLTV",
            "program_list": "Programy:",
            "no_programs": "Žiadne programy zatiaľ nepridané.",
            "download": "Stiahnuť XMLTV súbor"
        },
        "en": {
            "lang_select": "Language",
            "tz_select": "Timezone",
            "add": "Add Program",
            "title": "Title",
            "start": "Start Time",
            "stop": "End Time",
            "desc": "Description",
            "channel": "TV Channel",
            "tvgid": "TVG-ID",
            "submit": "Add",
            "export": "Export to XMLTV",
            "program_list": "Programs:",
            "no_programs": "No programs added yet.",
            "download": "Download XMLTV file"
        },
        "pl": {
            "lang_select": "Język",
            "tz_select": "Strefa czasowa",
            "add": "Dodaj program",
            "title": "Tytuł",
            "start": "Początek",
            "stop": "Koniec",
            "desc": "Opis",
            "channel": "Kanał TV",
            "tvgid": "TVG-ID",
            "submit": "Dodaj",
            "export": "Eksportuj do XMLTV",
            "program_list": "Programy:",
            "no_programs": "Nie dodano jeszcze żadnych programów.",
            "download": "Pobierz plik XMLTV"
        }
    }
    return translations.get(lang, translations["sk"])

@app.route("/", methods=["GET", "POST"])
def index():
    lang = request.args.get("lang", "sk")
    tz = request.args.get("tz", "Europe/Bratislava")
    texts = get_texts(lang)

    if request.method == "POST":
        if "export" in request.form:
            file_path = export_xmltv(lang, tz)
            return render_template("index.html", texts=texts, current_lang=lang, current_tz=tz, programs=[], file_ready=True)
        else:
            title = request.form.get("title", "")
            start = request.form.get("start", "")
            stop = request.form.get("stop", "")
            description = request.form.get("description", "")
            channel = request.form.get("channel", "")
            tvgid = request.form.get("tvgid", "")
            programs.append({
                "title": title,
                "start": start,
                "stop": stop,
                "description": description,
                "channel": channel,
                "tvgid": tvgid
            })
            channels[tvgid] = channel
            return redirect(f"/?lang={lang}&tz={tz}")

    return render_template("index.html", texts=texts, current_lang=lang, current_tz=tz, programs=programs, file_ready=False)

@app.route("/download")
def download():
    return send_file("epg.xml", as_attachment=True)

def export_xmltv(lang, tz):
    root = ET.Element("tv")

    for tvgid, name in channels.items():
        ch = ET.SubElement(root, "channel", {"id": tvgid})
        ET.SubElement(ch, "display-name").text = name

    for p in programs:
        elem = ET.SubElement(root, "programme", {
            "start": format_time(p["start"], tz),
            "stop": format_time(p["stop"], tz),
            "channel": p["tvgid"]
        })
        ET.SubElement(elem, "title", {"lang": lang}).text = p["title"]
        ET.SubElement(elem, "desc", {"lang": lang}).text = p["description"]

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

    programs.clear()
    channels.clear()
    return "epg.xml"

def format_time(dt_str, tz_name):
    local_tz = pytz.timezone(tz_name)
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
    localized_dt = local_tz.localize(dt)
    return localized_dt.strftime("%Y%m%d%H%M%S %z")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


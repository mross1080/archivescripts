import os
import json
import unidecode
from archive_scripts.extract_data_from_translation import extract_english_translations
import shutil

dirs = ["chatdata"]
count = 0
# prefix = "/mnt/c"
prefix = "C:"
file_list = os.listdir("{}/workspace/chat_installation/archive_data/".format(prefix))

img_names = []
audio_names = []

assets_folder = "{}/workspace/chat_installation/webapp/public".format(prefix)


# assets_folder = "{}/workspace/WebScrapingWorkshop/chat_assets".format(prefix)


def strip_sentence(line):
    split = line.split(". -")
    split_variation_2 = line.split(": ")
    if len(split_variation_2) == 2:
        # print(line)
        msg_body = split_variation_2[1]
    elif len(split) == 2:
        # print(line)
        msg_body = split[1]
    else:
        msg_body = line
    return msg_body

blacklisted_answers = ["Mi respuesta es","12 PM] - +1 (809) 818-9460","13 PM] - +1 (809) 818-9460"]
files_to_skip = ["Chat de WhatsApp con +1 (646) 831-3883.txt","Chat de WhatsApp con +1 (809) 618-9623.txt","Chat de WhatsApp con +1 (829) 636-5319as.txt"]
# files_to_skip = []
processed_files = []

def extract_content_from_archive(current_file):
    archive_text = []
    # print(current_file)
    msg_type = ""
    msg_file_type = "text"
    msg_body = ""
    try:
        file1 = open(current_file, 'r', encoding="utf8")
        Lines = file1.readlines()
        for line in Lines:
            try:
                if "Los mensajes y las llamadas" not in line:
                    strip_line = line.strip()
                    if "Toca para más información" in line:
                        pass
                    if "I.I.R.D:" in line:
                        msg_sender = "admin"
                    else:
                        msg_sender = "participant"

                    if "I.I.R.D" not in line and "+1" not in line:
                        split = line.split(". -")
                        split_variation_2 = line.split(": ")
                        split_variation_3 = line.split("20 ,")
                        if len(split_variation_2) == 2:
                            msg_body = split_variation_2[1]
                        elif len(split) == 2:
                            msg_body = split[1]
                        else:
                            msg_body = line
                    else:
                        if "Toca para más información" in line:
                            pass
                        elif msg_sender == "participant" and "https://" in line:
                            msg_body = line.split(": ")[1]
                        elif msg_sender == "admin" and "https://" in line:
                            msg_body = line.split(": ")[1].replace("\n","")
                        elif line.__contains__("20, "):
                            msg_body = line.split(":")[3]
                        else:
                            msg_body = line.split(":")[2]

                        # Any phrases that just cannot be in there
                        msg_body.replace("Ahhh si. ","")

                    if ".m4a" in msg_body:
                        msg_body = msg_body.replace(".m4a",".mp3").strip(" ")
                        msg_file_type = "audio"
                    elif ".jpg" in line:
                        msg_file_type = "image"
                    elif ".opus" in line:
                        msg_file_type = "audio"
                    elif ".webp" in line:
                        print("WEBP ",line)
                        msg_file_type = "image"
                        msg_body = msg_body.split(" ")[1]
                        print("formatted" , msg_body)
                    else:
                        msg_file_type = "text"
                    if (msg_body.strip(" ") not in blacklisted_answers):
                        archive_text.append({
                            "msg_sender": msg_sender,
                            "msg_body": msg_body,
                            "msg_file_type": msg_file_type
                        })
                    else:
                        print("")
            except Exception as e:
                print(e, line)
                pass

    except Exception as e:
        print(e)
    return archive_text


name_to_question_lookup = {
    " Vivir en una isla": "¿Volveria usted a vivir en una isla sin frontera y por qué?",
    "Colón": "¿Qué aprendió usted sobre Colón en la escuela que considere es la historia verídica?",
    " La Virgen de las Mercedes": "¿Por qué cree usted que la virgen de las mercedes protegió a los españoles y no a los indígenas en la batalla del santo cerro en 1495?",
    " Personas Esclavizadas": "¿Qué sabe usted sobre las personas negras esclavizadas en la Rep. Dom.?",
    "Mang\u00fa": "¿Usted come platano? ¿Sabía usted que el mangú es una comida popularizada por las personas negras esclavidas en Rep. Dom.?",
    "Salsa, Merengue, Bachata": "¿Cuándo y dónde baila usted música con influencias Africanas; Salsa, Merengue, Bachata?",
    " Cedula Vieja": "En su vieja cédula, ¿Fue usted denominado como Indio? ¿Por qué?",
    " V Centenario": "¿Por qué cree usted que la celebración del V Centenario fue importante para el gobierno y los empresarios de Rep. Dom.?",

    "Peña Gómez": "¿Cree usted que Peña Gómez tenia derecho a ser presidente, y por qué?",

}

number_to_name_lookup = [
" Vivir en una isla",
"Colón",
" La Virgen de las Mercedes",
" Personas Esclavizadas",
"Mang\u00fa",
"Salsa, Merengue, Bachata",
" Cedula Vieja",
" V Centenario",
"Peña Gómez"

]

extracted_archive = {
    "es": [],
    "en": []
}

def create_archive():
    json_archive = []
    # Archive Category refers to the individual groups of questions, which should be in subfolders matching the name
    for archive_category in file_list:
        try:
            archive_category_dir = "{}/Users/mattr/Downloads/chatdata1216/chatdata/{}".format(prefix, archive_category)
            archive_category_dir = "{}/workspace/chat_installation/archive_data/{}".format(prefix, archive_category)

            archive_num = int(archive_category.split(" ")[0]) -1
            archive_category_name = number_to_name_lookup[archive_num]
            # json_archive[archive_category_name] = []
            found_testimonies = []
            testimonies_for_archive = os.listdir(archive_category_dir)
            for count, t in enumerate(testimonies_for_archive):

                file_path = "{}/{}".format(archive_category_dir, t)
                files_for_testimony = os.listdir(file_path)
                for f in files_for_testimony:
                    count += 1
                    if ".txt" in f and f.strip(" ") not in files_to_skip and f not in processed_files:
                        current_file = '{}/{}'.format(file_path, f)
                        # print("CURRENT FILE NAME", f)
                        cleansed_archive = extract_content_from_archive(current_file)
                        # json_archive[archive_category_name].append(cleansed_archive)
                        found_testimonies.append(cleansed_archive)
                        processed_files.append(f)
                    elif f  in files_to_skip:
                        print("SKIPPING FILE", f)


                    if ".opus" in f or ".jpg" in f or ".webp" in f:
                        current_file = '{}/{}'.format(file_path, f)
                        t = t.replace(" ", "")
                        if ".opus" in f:
                            audio_names.append(f)
                        else:
                            img_names.append(f)
                        media_file_path = "{}/{}/".format(assets_folder, t)
                        # print(t)
                        # print("FILE TO MAKE", media_file_path)
                        if not os.path.exists(media_file_path):
                            # print("MADE NEW DIRECTORY", media_file_path)
                            os.makedirs(media_file_path)
                        file_to_copy = assets_folder + "/" + f
                        # print("Copying from {} to {}".format(current_file, file_to_copy))
                        shutil.copyfile(current_file, file_to_copy)
            question = name_to_question_lookup[archive_category_name]
            # print(question)

            json_archive.append({"id": unidecode.unidecode(archive_category_name.strip(" ").lower().replace(" ", "_")),
                                 "name": archive_category_name, "question": question, "data": found_testimonies})

            # print(strip_line)
            #     archive = os.listdir("{}/Users/mattr/Downloads/chatdata/chatdata/{}".format(dir_name))
            #     for a in archive:
            #         print(a)



        except Exception as e:
            print(e)
            print("\n\n\n\n\n")
    print("found {} files ".format(count))

    extracted_archive["es"] = json_archive
    extracted_archive["en"] = extract_english_translations()
    with open('archive.json', 'w') as outfile:
        json.dump(extracted_archive, outfile)
    return extracted_archive


json_archive = create_archive()

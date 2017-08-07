from bs4 import BeautifulSoup


with open("../acm_site/proftalks.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

talk_list = []

def create_panel(talk_id, talk_title):
    column_div = soup.new_tag("div")
    column_div["class"] = "col-md-3"

    a_tag = soup.new_tag("a")
    a_tag["data-toggle"] = "modal"
    a_tag["data-target"] = "#"+talk_id


    outer_panel = soup.new_tag("div")
    outer_panel["class"] = "panel panel-default"

    panel_title = soup.new_tag("div")
    panel_title["class"] = "panel-heading"
    title_tag = soup.new_tag("h4")
    title_tag.string = talk_title
    panel_title.insert(0, title_tag)

    panel_body = soup.new_tag("div")
    panel_body["class"] = "panel-body"
    panel_img = soup.new_tag("img")
    panel_img["src"] = "assets/img/proftalks/tim.jpg"
    panel_img["width"] = "100%"
    panel_img["height"] = "100%"

    panel_body.insert(0, panel_img)
    outer_panel.insert(0, panel_title)
    outer_panel.insert(1, panel_body)
    a_tag.insert(0, outer_panel)
    column_div.insert(0, a_tag)

    return column_div

def create_modal(talk_id, talk_title, talk_abstract):
    outer_modal = soup.new_tag("div")
    outer_modal["id"] = talk_id
    outer_modal["class"] = "modal fade"
    outer_modal["role"] = "dialog"

    dialog_div = soup.new_tag("div")
    dialog_div["class"] = "modal-dialog"

    modal_content = soup.new_tag("div")
    modal_content["class"] = "modal-content"

    modal_header = soup.new_tag("div")
    modal_header["class"] = "modal-header"
    close_button = soup.new_tag("button")
    close_button["type"] = "button"
    close_button["class"] = "close"
    close_button["data-dismiss"] = "modal"
    close_button.string = "&times;"

    modal_title = soup.new_tag("h4")
    modal_title["class"] = "modal-title"
    modal_title.string = talk_title

    modal_header.insert(0, close_button)
    modal_header.insert(1, modal_title)

    modal_body = soup.new_tag("div")
    modal_body["class"] = "modal-body"
    modal_body_text = soup.new_tag("p")
    modal_body_text.string = talk_abstract
    modal_body.insert(0, modal_body_text)

    modal_content.insert(0, modal_header)
    modal_content.insert(1, modal_body)

    dialog_div.insert(0, modal_content)
    outer_modal.insert(0, dialog_div)

    return outer_modal

def reset_screen():
    print(chr(27) + "[2J")
    print(chr(27) + "[1;1H")

def create_id(talk):
    id = talk["professor"].replace(" ", "")
    id += talk["date"].replace(" ", "")
    return id

def export_html():
    prof_tag = soup.select("#prof-talks")
    for i in talk_list:
        talk_id = create_id(i)
        prof_tag[0].insert(0, create_panel(talk_id, i["title"]))
        prof_tag[0].insert(1, create_modal(talk_id, i["title"], i["abstract"]))

    print(soup.prettify(formatter=None))
    with open("output.html", "w") as output:
        output.write(str(soup.prettify(formatter=None)))

def add_talk_menu():
    title = ""
    professor = ""
    date = ""
    abstract = ""

    keep_running = True

    while keep_running:
        reset_screen()

        print("Add New Talk:")
        print("-------------\n")

        print("Title: " + title)
        print("Professor: " + professor)
        print("Date: " + date)
        print("Abstract: " + abstract)

        print("1. Set Title")
        print("2. Set Professor")
        print("3. Set Date")
        print("4. Set Abstract")
        print("5. Save and Exit")
        print("6. Just Exit (no saving)")

        selection = int(input("Enter selection: "))

        if selection == 1:
            title = input("Enter talk title: ")

        elif selection == 2:
            professor = input("Enter Professor Name: ")

        elif selection == 3:
            date = input("Enter talk date: ")

        elif selection == 4:
            abstract = input("Enter abstract text: ")

        elif selection == 5:
            talk_list.append({"title": title, "professor": professor, "date": date, "abstract": abstract})
            keep_running = False
            return 1

        elif selection == 6:
            keep_running = False
            return 0

        else:
            print("Invalid selection")

def main_menu():
    keep_running = True
    pending_updates = 0
    while keep_running:
        reset_screen()

        print("----------------")
        print("Proftalk Manager")
        print("----------------\n")

        print(str(pending_updates) + " new proftalks to add")
        print("1. Add new proftalk")
        print("2. Publish pending talks")
        print("3. Exit")

        selection = input("Selection: ")

        if int(selection) == 1:
            pending_updates += add_talk_menu()

        elif int(selection) == 2:
            export_html()
            keep_running = False

        elif int(selection) == 3:
            print("Exiting...")
            keep_running = False

        else:
            print("Invalid input!")

main_menu()

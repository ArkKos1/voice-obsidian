import tkinter as tk
from tkinter import ttk,messagebox
import json
from pathlib import Path

LABELS = [ 
          "FOLDER",
          "NOTE",
          "TEXT",
          "POSITION",
          "FORMAT",
          "REFERENCE",
          "ROW",
          "COLUMN",
          "LATEX",
          "PROPERTY"
]
intents = ["create_folder","create_note",
           "open_folder","open_note",
           "insert_text","delete_text",
           "back","undo","redo",
           "create_table","table_new_cell","table_new_row_or_column",
           "format_text","insert_latex",
           "change_property","add_property",
           "insert_template","insert_link",
           "insert_file", "search",
           "rename_note","rename_folder",
           "delete_note","delete_folder",
           "move_note","move_folder",
           ]

DATASET_PATH = Path(__file__).resolve().parent/"datasets"/"dataset.jsonl"

class DatasetMakerApp:
  def __init__(self,root):
    self.entities =[]
    self.root = root 
    self.root.title("Dataset Maker")
    self.root.geometry("800x600")
    
    ttk.Label(root,text="Input Command",font=("Arial",14)).pack()

    self.text_entry = tk.Entry(root,font=("Arial",14))
    self.text_entry.pack(fill="x",padx=10,pady=5)
    self.text_entry.configure(exportselection=False)

    controls = ttk.Frame(root)
    controls.pack(fill="x",padx=10,pady=5)

    controls.columnconfigure(0,weight=1)
    controls.columnconfigure(1,weight=1)

    # =======================LEFT SIDE=======================

    intent_frame = ttk.Frame(controls)
    intent_frame.grid(row=0,column=0,sticky="ew",padx=(10,0))

    ttk.Label(intent_frame,text="Choose Intent",font=("Arial",14)).pack(anchor="w")

    self.intent_choose = ttk.Combobox(
      intent_frame,
      values=intents,
      state="readonly"
    )
    self.intent_choose.pack(anchor="w")
    self.intent_choose.set("create_note")

    # =======================RIGHT SIDE=======================

    label_frame = ttk.Frame(controls)
    label_frame.grid(row=0,column=1,sticky="ew",padx=(10,0))
    
    box_frame = ttk.Frame(label_frame)
    box_frame.grid(row=0,column=0,sticky="ew")

    ttk.Label(box_frame,text="Choose Label",font=("Arial",14)).pack(anchor="w")

    self.label_choose = ttk.Combobox(
      box_frame,
      values=LABELS,
      state="readonly"
    )
    self.label_choose.pack(side="left")
    self.label_choose.set("NOTE")

    button_frame = ttk.Frame(label_frame)
    button_frame.grid(row=0,column=1,sticky="w")

    ttk.Label(button_frame,text="Press Button",font=("Arial",14)).pack(anchor="w")

    ttk.Button(
      button_frame,
      text="Choose",
      command=self.add_entity,
    ).pack(side="left")

    ttk.Button(root,text="Finish command",command=self.finish).pack(anchor="n",fill="x")

    ttk.Label(root,text="Choosed entity",font=("Arial",14)).pack(anchor="n")

    self.entity_list = tk.Listbox(root,font=("Arial",12),selectmode=tk.SINGLE)
    self.entity_list.pack(fill="both",padx=10,pady=(5,10))

  def add_entity(self):
    text = self.text_entry.get()

    if not self.text_entry.selection_present():
      messagebox.showwarning("Select Entity")
      return 
    
    label = self.label_choose.get()

    if not label:
      messagebox.showwarning("Select label")
      return
    
    start = self.text_entry.index("sel.first")
    end = self.text_entry.index("sel.last")

    selected_text = text[start:end]
    if not selected_text:
      return
    entity = {
      "start":start,
      "end":end,
      "label":label
    }
    self.entities.append(entity)
    self.entities.sort(key=lambda e: e["start"])

    self.refresh_list()

  def refresh_list(self):
    self.entity_list.delete(0,tk.END)
    text = self.text_entry.get()
    for entity in self.entities:
      selected_text = text[entity["start"]:entity["end"]]
      self.entity_list.insert(tk.END,f"{entity['label']} - {selected_text}")
  
  def finish(self):
    text = self.text_entry.get()
    intent = self.intent_choose.get()

    if not text.strip():
      messagebox.showwarning("Input command")
      return
    if not intent:
      messagebox.showwarning("Choose intent")
      return
    
    record = {"text":text.lower(),"intent":intent,"entities":self.entities}

    for entity in self.entities:
      start = entity["start"]
      end = entity["end"]
      if not (0<=start<end<=len(text)):
        messagebox.showerror(f"Error, invalid borders of {entity}")
        return
      
    output_path = (Path(__file__).resolve().parent/"datasets"/"dataset.jsonl")
    try:
      output_path.parent.mkdir(
        parents=True,
        exist_ok=True
      )
      with output_path.open("a",encoding="utf-8") as file:
        file.write(json.dumps(record,ensure_ascii=False,)+"\n")
    except OSError:
      messagebox.showerror(f"Error, {str(OSError)}")

    self.text_entry.delete(0,tk.END)
    self.entities.clear()
    self.refresh_list()
    self.text_entry.focus_set()  






if __name__=="__main__":
  root=tk.Tk()
  app = DatasetMakerApp(root)
  root.mainloop()


import tkinter as tk
from gui import ApplicationVentes

def main():
    root = tk.Tk()
    app = ApplicationVentes(root)
    
    root.protocol("WM_DELETE_WINDOW", app.fermer_application)
    
    root.mainloop()

if __name__ == "__main__":
    main()
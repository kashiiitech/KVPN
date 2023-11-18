import tkinter as tk
import vpn

def main():
    def connect():
        status_label.config(text="Connected")
        vpn.Click(True)

    def disconnect():
        status_label.config(text="Disconnected")
        vpn.Click(False)

    root = tk.Tk()
    root.title("Kashiiitech -- VPN 20P-0648")

    # Create widgets
    title_label = tk.Label(root, text="KVPN", font=("Arial", 80), fg="blue")
    connect_button = tk.Button(root, text="Connect", command=connect)
    disconnect_button = tk.Button(root, text="Disconnect", command=disconnect)
    status_label = tk.Label(root, text="", font=("Arial", 20), pady=20)

    # Center widgets in window
    title_label.grid(row=0, column=0, columnspan=2, pady=50)
    connect_button.grid(row=1, column=0, padx=10, pady=20)
    disconnect_button.grid(row=1, column=1, padx=10, pady=20)
    status_label.grid(row=2, column=0, columnspan=2, pady=20)

    # Center window on screen
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()

if __name__ == "__main__":
    main()

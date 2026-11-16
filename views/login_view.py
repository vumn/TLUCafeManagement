import customtkinter as ctk
from database.db import db
from tkinter import messagebox

ctk.set_appearance_mode("Light")

class LoginView(ctk.CTkFrame):
    BG_COLOR = "#F3F4F6"
    CARD_COLOR = "#FFFFFF"
    TEXT_COLOR = "#1E3A8A"
    BLUE_COLOR = "#0056B3"
    RED_COLOR = "#D90429"
    HOVER_COLOR = "#B8001F"

    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color=self.BG_COLOR, corner_radius=0)
        self.master = master
        self.on_login_success = on_login_success
        self.pack(fill="both", expand=True)

        self._build_ui()
    
    def _build_ui(self):
        card = ctk.CTkFrame(
            self,
            width=380,
            height=430,
            fg_color=self.CARD_COLOR,
            corner_radius=15,
            border_width=2,
            border_color="#EAECEF"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False) # cố định kích thước card

        self.footer_lbl = ctk.CTkLabel(
            card,
            text="© 2026 Nhom 2 Python. All rights reserved.",
            font=("Arial", 11),
            text_color="#9CA3AF"
        )
        self.footer_lbl.pack(side="bottom", pady=25)
        
        # title
        ctk.CTkLabel(
            card,
            text="TLU CAFÉTERIA",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=self.TEXT_COLOR
        ).pack(pady=(30, 2))

        # Username label
        ctk.CTkLabel(
            card,
            text="Tài khoản:",
            font=ctk.CTkFont("Segoe UI", 13,"bold"),
            text_color=self.TEXT_COLOR
        ).pack(anchor="w", padx=40)

        self.ent_username = ctk.CTkEntry(
            card, 
            width=300,
            height=40,
            placeholder_text="Tên đăng nhập",
            fg_color="#F8FAFC",
            text_color=self.TEXT_COLOR,
            border_color="#D1D5DB",
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.ent_username.pack(padx=40, pady=(5, 15))
        self.ent_username.focus()

        ctk.CTkLabel(
            card,
            text="Mật khẩu:",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=self.BLUE_COLOR
        ).pack(anchor="w", padx=40)

        self.ent_password = ctk.CTkEntry(
            card,
            width=300,
            height=40,
            placeholder_text="••••••••",
            show="*",
            fg_color="white",
            text_color=self.BLUE_COLOR,
            border_color="#D1D5DB",
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.ent_password.pack(padx=40, pady=(5, 10))

        self.ent_password.bind("<Return>", lambda event: self.handle_login())

        #Checkbox
        self.chk_show_pass = ctk.CTkCheckBox(
            card,
            text="Hiện mật khẩu",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.BLUE_COLOR,
            fg_color=self.BLUE_COLOR,
            hover_color=self.BLUE_COLOR,
            checkbox_width=18,
            checkbox_height=18,
            command=self.toggle_password
        )
        self.chk_show_pass.pack(anchor="w", padx=40, pady=(0, 20))

        btn_login = ctk.CTkButton(
            card,
            text="ĐĂNG NHẬP",
            width=300,
            height=42,
            fg_color=self.BLUE_COLOR,
            hover_color=self.HOVER_COLOR,
            text_color="#FFFFFF",
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self.handle_login
        )
        btn_login.pack(padx=40)

    def toggle_password(self):
        if self.chk_show_pass.get() == 1:
            self.ent_password.configure(show="")
        else:
            self.ent_password.configure(show="*")

    def handle_login(self):
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin")
            return
    # Truy vấn chống SQL Injection
        sql = """
            SELECT user_id, username, full_name, role 
            FROM users 
            WHERE username = %s AND password = %s
        """
        user = db.fetch_one(sql, (username, password))

        if user:
            # Gọi hàm callback chuyển sang màn hình chính
            self.on_login_success(user)
        else:
            messagebox.showerror("Đăng nhập thất bại", "Tài khoản hoặc mật khẩu không chính xác!")

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Đăng nhập")
    app.geometry("500x520")
    app.resizable(False, False)

    def test_success(user_data):
        messagebox.showinfo(
            "Đăng nhập thành công",
            f"Xin chào: {user_data['full_name']}\nQuyền hạn: {user_data['role']}"
        )

    LoginView(app, on_login_success=test_success)
    app.mainloop()
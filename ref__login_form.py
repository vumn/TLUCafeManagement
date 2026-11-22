import customtkinter as ctk
from PIL import Image

# Cấu hình giao diện sáng
ctk.set_appearance_mode("light")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shoplite POS - Login")
        self.geometry("600x650")
        self.configure(fg_color="#F3F4F6")  # Màu nền xám nhạt bên ngoài

        # --- KHUNG TRẮNG CHÍNH (CARD) ---
        self.card = ctk.CTkFrame(
            self, 
            width=420, 
            height=540, 
            corner_radius=16, 
            fg_color="#FFFFFF"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)  # Giữ cố định kích thước khung

        # --- 1. LOGO ---
        # (Ở đây dùng khung giả lập logo, bạn có thể thay bằng ctk.CTkImage)
        self.logo_box = ctk.CTkFrame(
            self.card, width=65, height=65, corner_radius=8, fg_color="#F8FAFC"
        )
        self.logo_box.pack(pady=(35, 15))
        self.logo_box.pack_propagate(False)
        
        self.logo_lbl = ctk.CTkLabel(
            self.logo_box, text="📦\nPOS", font=("Arial", 13, "bold"), text_color="#0284C7"
        )
        self.logo_lbl.place(relx=0.5, rely=0.5, anchor="center")

        # --- 2. TIÊU ĐỀ ---
        self.title_lbl = ctk.CTkLabel(
            self.card, 
            text="Welcome Back", 
            font=("Arial", 28, "bold"), 
            text_color="#111827"
        )
        self.title_lbl.pack(pady=(0, 5))

        self.sub_lbl = ctk.CTkLabel(
            self.card, 
            text="Sign in to your account", 
            font=("Arial", 14), 
            text_color="#6B7280"
        )
        self.sub_lbl.pack(pady=(0, 25))

        # --- 3. Ô NHẬP USERNAME ---
        self.user_label = ctk.CTkLabel(
            self.card, text="Username", font=("Arial", 13, "bold"), text_color="#374151"
        )
        self.user_label.pack(anchor="w", padx=45, pady=(0, 6))

        self.username_entry = self.create_input_with_icon(
            parent=self.card, 
            icon_text="👤", 
            placeholder="Enter your username"
        )

        # --- 4. Ô NHẬP PASSWORD ---
        self.pass_label = ctk.CTkLabel(
            self.card, text="Password", font=("Arial", 13, "bold"), text_color="#374151"
        )
        self.pass_label.pack(anchor="w", padx=45, pady=(15, 6))

        self.password_entry = self.create_input_with_icon(
            parent=self.card, 
            icon_text="🔒", 
            placeholder="••••••••", 
            is_password=True
        )

        # --- 5. NÚT ĐĂNG NHẬP ---
        self.login_btn = ctk.CTkButton(
            self.card,
            text="Sign In",
            font=("Arial", 15, "bold"),
            fg_color="#1D63ED",       # Màu xanh dương giống ảnh
            hover_color="#154EC1",
            height=45,
            corner_radius=8,
            command=self.login_event
        )
        self.login_btn.pack(fill="x", padx=45, pady=(25, 30))

        # --- 6. FOOTER BẢN QUYỀN ---
        self.footer_lbl = ctk.CTkLabel(
            self.card,
            text="© 2026 ShopLite Cloud. All rights reserved.",
            font=("Arial", 11),
            text_color="#9CA3AF"
        )
        self.footer_lbl.pack(side="bottom", pady=25)

    def create_input_with_icon(self, parent, icon_text, placeholder, is_password=False):
        """Hàm tạo ô nhập liệu có chứa icon bên trong"""
        frame = ctk.CTkFrame(
            parent,
            height=45,
            fg_color="#FFFFFF",
            border_color="#D1D5DB",
            border_width=1,
            corner_radius=8
        )
        frame.pack(fill="x", padx=45)
        frame.pack_propagate(False)

        # Icon bên trái
        icon_lbl = ctk.CTkLabel(
            frame, text=icon_text, font=("Arial", 15), text_color="#9CA3AF"
        )
        icon_lbl.pack(side="left", padx=(14, 6))

        # Ô Entry không viền bên phải
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            placeholder_text_color="#9CA3AF",
            font=("Arial", 14),
            fg_color="transparent",
            border_width=0,
            text_color="#111827",
            show="•" if is_password else ""
        )
        entry.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=2)

        # Hiệu ứng đổi màu viền thành xanh khi click vào ô nhập
        entry.bind("<FocusIn>", lambda e: frame.configure(border_color="#1D63ED", border_width=1.5))
        entry.bind("<FocusOut>", lambda e: frame.configure(border_color="#D1D5DB", border_width=1))

        return entry

    def login_event(self):
        print("Username:", self.username_entry.get())
        print("Password:", self.password_entry.get())

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()

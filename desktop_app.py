import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import os
from dotenv import load_dotenv
import sys

class DeploymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI API Stripe Deployment")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # Set style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.root.configure(bg='#1a1a2e')
        
        # Main frame
        main_frame = tk.Frame(root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with avatar
        header_frame = tk.Frame(main_frame, bg='#1a1a2e')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Avatar (emoji circle)
        avatar_label = tk.Label(
            header_frame,
            text="🚀",
            font=("Arial", 60),
            bg='#1a1a2e',
            fg='#00d4ff'
        )
        avatar_label.pack()
        
        title_label = tk.Label(
            header_frame,
            text="AI API with Stripe",
            font=("Arial", 24, "bold"),
            bg='#1a1a2e',
            fg='#00d4ff'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="One-Click Deployment",
            font=("Arial", 12),
            bg='#1a1a2e',
            fg='#888888'
        )
        subtitle_label.pack()
        
        # Separator
        separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=20)
        
        # Form frame
        form_frame = tk.Frame(main_frame, bg='#1a1a2e')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # HF Username
        tk.Label(form_frame, text="HF Username:", font=("Arial", 10, "bold"), bg='#1a1a2e', fg='#ffffff').pack(anchor=tk.W, pady=(10, 5))
        self.hf_username = ttk.Entry(form_frame, width=50)
        self.hf_username.insert(0, "klenz1984")
        self.hf_username.pack(anchor=tk.W, pady=(0, 15))
        
        # HF Token
        tk.Label(form_frame, text="HF Token:", font=("Arial", 10, "bold"), bg='#1a1a2e', fg='#ffffff').pack(anchor=tk.W, pady=(10, 5))
        self.hf_token = ttk.Entry(form_frame, width=50, show="*")
        self.hf_token.pack(anchor=tk.W, pady=(0, 15))
        
        # Stripe Secret Key
        tk.Label(form_frame, text="Stripe Secret Key:", font=("Arial", 10, "bold"), bg='#1a1a2e', fg='#ffffff').pack(anchor=tk.W, pady=(10, 5))
        self.stripe_secret = ttk.Entry(form_frame, width=50, show="*")
        self.stripe_secret.pack(anchor=tk.W, pady=(0, 15))
        
        # Stripe Publishable Key
        tk.Label(form_frame, text="Stripe Publishable Key:", font=("Arial", 10, "bold"), bg='#1a1a2e', fg='#ffffff').pack(anchor=tk.W, pady=(10, 5))
        self.stripe_pub = ttk.Entry(form_frame, width=50, show="*")
        self.stripe_pub.pack(anchor=tk.W, pady=(0, 15))
        
        # Starter Price ID
        tk.Label(form_frame, text="Stripe Starter Price ID:", font=("Arial", 10, "bold"), bg='#1a1a2e', fg='#ffffff').pack(anchor=tk.W, pady=(10, 5))
        self.starter_price = ttk.Entry(form_frame, width=50)
        self.starter_price.insert(0, "price_1U9FgZIcqdz5i1m1vYH1gvvL")
        self.starter_price.pack(anchor=tk.W, pady=(0, 15))
        
        # Pro Price ID
        tk.Label(form_frame, text="Stripe Pro Price ID:", font=("Arial", 10, "bold"), bg='#1a1a2e', fg='#ffffff').pack(anchor=tk.W, pady=(10, 5))
        self.pro_price = ttk.Entry(form_frame, width=50)
        self.pro_price.insert(0, "price_1U9GpvIcqdz5i1m1pfGb9rXp")
        self.pro_price.pack(anchor=tk.W, pady=(0, 15))
        
        # Separator
        separator2 = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
        separator2.pack(fill=tk.X, pady=20)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#1a1a2e')
        button_frame.pack(fill=tk.X, pady=20)
        
        # Deploy button
        self.deploy_btn = tk.Button(
            button_frame,
            text="🚀 Deploy Now",
            font=("Arial", 14, "bold"),
            bg='#00d4ff',
            fg='#1a1a2e',
            padx=40,
            pady=12,
            cursor="hand2",
            command=self.deploy
        )
        self.deploy_btn.pack(side=tk.LEFT, padx=5)
        
        # Open Local button
        self.local_btn = tk.Button(
            button_frame,
            text="🖥️ Run Local",
            font=("Arial", 14, "bold"),
            bg='#16c784',
            fg='#1a1a2e',
            padx=40,
            pady=12,
            cursor="hand2",
            command=self.run_local
        )
        self.local_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(fill=tk.X, pady=20)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to deploy!",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#888888'
        )
        self.status_label.pack(anchor=tk.W)
        
        self.deploying = False
    
    def validate_inputs(self):
        if not self.hf_username.get():
            messagebox.showerror("Error", "Please enter HF Username")
            return False
        if not self.hf_token.get():
            messagebox.showerror("Error", "Please enter HF Token")
            return False
        if not self.stripe_secret.get():
            messagebox.showerror("Error", "Please enter Stripe Secret Key")
            return False
        if not self.stripe_pub.get():
            messagebox.showerror("Error", "Please enter Stripe Publishable Key")
            return False
        if not self.starter_price.get():
            messagebox.showerror("Error", "Please enter Starter Price ID")
            return False
        if not self.pro_price.get():
            messagebox.showerror("Error", "Please enter Pro Price ID")
            return False
        return True
    
    def create_env_file(self):
        env_content = f"""HF_USERNAME={self.hf_username.get()}
HF_TOKEN={self.hf_token.get()}
STRIPE_SECRET_KEY={self.stripe_secret.get()}
STRIPE_PUBLISHABLE_KEY={self.stripe_pub.get()}
STRIPE_STARTER_PRICE_ID={self.starter_price.get()}
STRIPE_PRO_PRICE_ID={self.pro_price.get()}
"""
        with open(".env", "w") as f:
            f.write(env_content)
        self.update_status("✓ .env file created")
    
    def update_status(self, message):
        self.status_label.config(text=message, fg='#00d4ff')
        self.root.update()
    
    def deploy(self):
        if not self.validate_inputs():
            return
        
        if self.deploying:
            messagebox.showwarning("Warning", "Deployment already in progress")
            return
        
        self.deploying = True
        self.deploy_btn.config(state=tk.DISABLED)
        self.local_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        thread = threading.Thread(target=self._deploy_thread)
        thread.daemon = True
        thread.start()
    
    def _deploy_thread(self):
        try:
            self.update_status("Creating .env file...")
            self.create_env_file()
            
            self.update_status("Installing dependencies...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception("Failed to install dependencies")
            
            self.update_status("✓ Ready to deploy to HF Spaces!")
            
            # Show success message
            messagebox.showinfo(
                "Success! 🎉",
                "Your credentials are saved!\n\n"
                "Next steps:\n"
                "1. Go to https://huggingface.co/spaces/new\n"
                "2. Choose Docker SDK\n"
                "3. Connect GitHub: juankhernan34-droid/ai-api-stripe\n"
                "4. Add your secrets\n"
                "5. Click Create Space\n\n"
                "Your API will be live in minutes!"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Deployment failed: {str(e)}")
            self.update_status("❌ Deployment failed")
        
        finally:
            self.progress.stop()
            self.deploying = False
            self.deploy_btn.config(state=tk.NORMAL)
            self.local_btn.config(state=tk.NORMAL)
    
    def run_local(self):
        if not self.validate_inputs():
            return
        
        if self.deploying:
            messagebox.showwarning("Warning", "Operation already in progress")
            return
        
        self.deploying = True
        self.deploy_btn.config(state=tk.DISABLED)
        self.local_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        thread = threading.Thread(target=self._run_local_thread)
        thread.daemon = True
        thread.start()
    
    def _run_local_thread(self):
        try:
            self.update_status("Creating .env file...")
            self.create_env_file()
            
            self.update_status("Installing dependencies...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception("Failed to install dependencies")
            
            self.update_status("Starting API locally...")
            
            messagebox.showinfo(
                "Starting API 🚀",
                "Your API is starting on http://localhost:7860\n\n"
                "The app will stay open while the API runs.\n"
                "Close this window to stop the API."
            )
            
            subprocess.run([sys.executable, "app.py"])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run local API: {str(e)}")
            self.update_status("❌ Failed to run local API")
        
        finally:
            self.progress.stop()
            self.deploying = False
            self.deploy_btn.config(state=tk.NORMAL)
            self.local_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeploymentApp(root)
    root.mainloop()

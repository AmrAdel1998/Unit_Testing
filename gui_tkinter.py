import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
import webbrowser
from docs_parser import DocumentManager
from c_parser import CProjectParser
from test_generator import TestGenerator
from test_runner import TestRunner
from ai_document_analyzer import AIDocumentAnalyzer
import json


class PytestToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧪 Pytest Tool - Automated C Test Generator")
        self.root.geometry("1000x700")
        
        # Initialize managers
        self.dm = DocumentManager('data/docs')
        self.tr = TestRunner('data/generated_tests', 'data/reports')
        self.ai_analyzer = AIDocumentAnalyzer()  # AI document analyzer
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_parse_tab()
        self.create_tests_tab()
        self.create_run_tab()
        
        # Status bar for API Key
        self.status_bar = ttk.Frame(root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=2)
        
        self.api_status_label = ttk.Label(self.status_bar, text="AI Status: Checking...")
        self.api_status_label.pack(side=tk.RIGHT)
        
        self.update_api_status()
        
        # Auto-parse on startup
        self.root.after(100, self.parse_project)
    
    def update_api_status(self):
        """Update the AI status indicator based on API key availability"""
        if self.ai_analyzer.use_ai:
            self.api_status_label.config(text="● AI Enabled (OpenAI)", foreground="green")
        else:
            self.api_status_label.config(text="○ AI Disabled (Fallback Mode)", foreground="red")
    
    def create_parse_tab(self):
        """C Project parsing tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔍 Parse C Project")
        
        # Project path
        path_frame = ttk.LabelFrame(frame, text="Project Path", padding=10)
        path_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.project_path = tk.StringVar(value="examples")
        ttk.Entry(path_frame, textvariable=self.project_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(path_frame, text="Browse", command=self.browse_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(path_frame, text="Parse Project", command=self.parse_project).pack(side=tk.LEFT, padx=5)
        
        # Results
        result_frame = ttk.LabelFrame(frame, text="Parsed Functions", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for functions
        tree_scroll = ttk.Scrollbar(result_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.function_tree = ttk.Treeview(result_frame, columns=("Return", "Args"), show="tree headings", yscrollcommand=tree_scroll.set)
        self.function_tree.heading("#0", text="Function Name")
        self.function_tree.heading("Return", text="Return Type")
        self.function_tree.heading("Args", text="Arguments")
        self.function_tree.column("#0", width=200)
        self.function_tree.column("Return", width=150)
        self.function_tree.column("Args", width=400)
        self.function_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.function_tree.yview)
        
        self.parse_status = ttk.Label(frame, text="Ready to parse")
        self.parse_status.pack(pady=5)
    
    def create_tests_tab(self):
        """Generated tests tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝 Generated Tests")
        
        # Generate button
        gen_frame = ttk.Frame(frame)
        gen_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(gen_frame, text="Generate Tests", command=self.generate_tests).pack(side=tk.LEFT, padx=5)
        self.gen_status = ttk.Label(gen_frame, text="")
        self.gen_status.pack(side=tk.LEFT, padx=10)
        
        # Test files list
        list_frame = ttk.LabelFrame(frame, text="Generated Test Files", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons for test file management
        btn_frame_top = ttk.Frame(list_frame)
        btn_frame_top.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame_top, text="View Selected", command=self.view_test_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_top, text="Delete Selected", command=self.delete_test_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_top, text="Refresh", command=self.refresh_tests).pack(side=tk.LEFT, padx=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.test_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode=tk.EXTENDED)
        self.test_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.test_listbox.yview)
        
        # Selection info label
        self.test_selection_info = ttk.Label(list_frame, text="Tip: Hold Ctrl/Cmd to select multiple test files")
        self.test_selection_info.pack(pady=5)
        
        # Test content view
        self.test_view = scrolledtext.ScrolledText(frame, height=15, wrap=tk.WORD)
        self.test_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.refresh_tests()
    
    def create_run_tab(self):
        """Run tests and reports tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="▶️ Run & Reports")
        
        # Test selection
        select_frame = ttk.LabelFrame(frame, text="Select Tests to Run", padding=10)
        select_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Select/Deselect buttons
        select_btn_frame = ttk.Frame(select_frame)
        select_btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(select_btn_frame, text="Select All", command=self.select_all_tests).pack(side=tk.LEFT, padx=5)
        ttk.Button(select_btn_frame, text="Deselect All", command=self.deselect_all_tests).pack(side=tk.LEFT, padx=5)
        ttk.Button(select_btn_frame, text="Refresh", command=self.refresh_test_selection).pack(side=tk.LEFT, padx=5)
        
        # Checkboxes frame with scrollbar
        canvas = tk.Canvas(select_frame)
        scrollbar = ttk.Scrollbar(select_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.test_checkboxes = {}
        self.test_vars = {}
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.checkbox_frame = scrollable_frame
        
        # Run button
        run_frame = ttk.Frame(frame)
        run_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(run_frame, text="Run Selected Tests", command=self.run_tests).pack(side=tk.LEFT, padx=5)
        self.run_status = ttk.Label(run_frame, text="")
        self.run_status.pack(side=tk.LEFT, padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(run_frame, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Error display area
        error_frame = ttk.LabelFrame(frame, text="Test Execution Log", padding=10)
        error_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.error_text = scrolledtext.ScrolledText(error_frame, height=8, wrap=tk.WORD)
        self.error_text.pack(fill=tk.BOTH, expand=True)
        
        # Reports
        report_frame = ttk.LabelFrame(frame, text="Reports", padding=10)
        report_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(report_frame, text="Open HTML Report", command=self.open_html_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(report_frame, text="Open XML Report", command=self.open_xml_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(report_frame, text="Open Excel Report", command=self.open_excel_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(report_frame, text="Open Reports Folder", command=self.open_reports_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(report_frame, text="View Error Log", command=self.view_error_log).pack(side=tk.LEFT, padx=5)
        
        self.refresh_test_selection()
    
    # Parse tab methods
    def browse_project(self):
        path = filedialog.askdirectory(title="Select C Project Folder")
        if path:
            self.project_path.set(path)
    
    def parse_project(self):
        project_dir = self.project_path.get()
        if not os.path.exists(project_dir):
            messagebox.showerror("Error", f"Path does not exist: {project_dir}")
            return
        
        self.parse_status.config(text="Parsing...")
        self.function_tree.delete(*self.function_tree.get_children())
        
        def parse():
            try:
                cpp = CProjectParser(project_dir)
                functions = cpp.parse_project()
                
                # Save to JSON
                os.makedirs('data/parsed_c', exist_ok=True)
                with open('data/parsed_c/functions.json', 'w') as f:
                    json.dump(functions, f, indent=2)
                
                # Cleanup old test files that don't match new project
                self.root.after(0, lambda: self.cleanup_old_tests(functions))
                
                # Update UI in main thread
                self.root.after(0, lambda: self.update_function_tree(functions))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Parse failed: {str(e)}"))
        
        threading.Thread(target=parse, daemon=True).start()
    
    def cleanup_old_tests(self, functions):
        """Remove test files for functions that no longer exist in the parsed project"""
        try:
            # Get current function signatures
            current_function_files = set()
            for fn in functions:
                fname = fn['name']
                mod = ''.join(c if c.isalnum() or c=='_' else '_' for c in fn['file'].replace('/', '_'))
                outname = f'test_{mod}_{fname}.py'
                current_function_files.add(outname)
            
            # Find and remove old test files
            if os.path.exists('data/generated_tests'):
                existing_files = [f for f in os.listdir('data/generated_tests') if f.startswith('test_') and f.endswith('.py')]
                removed_count = 0
                for old_file in existing_files:
                    if old_file not in current_function_files:
                        try:
                            os.remove(os.path.join('data/generated_tests', old_file))
                            removed_count += 1
                        except Exception as e:
                            print(f"Failed to remove {old_file}: {e}")
                
                if removed_count > 0:
                    self.root.after(0, lambda: self.refresh_tests())
                    self.root.after(0, lambda: self.refresh_test_selection())
                    self.root.after(0, lambda: messagebox.showinfo("Cleanup", f"Removed {removed_count} old test file(s) that don't match the new project."))
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def update_function_tree(self, functions):
        self.function_tree.delete(*self.function_tree.get_children())
        for fn in functions:
            self.function_tree.insert("", tk.END, text=fn['name'], 
                                    values=(fn['return'], fn['args']),
                                    tags=(os.path.basename(fn['file']),))
        self.parse_status.config(text=f"Found {len(functions)} functions")
    
    # Tests tab methods
    def generate_tests(self):
        self.gen_status.config(text="Generating...")
        project_dir = self.project_path.get()
        
        def generate():
            try:
                cpp = CProjectParser(project_dir)
                functions = cpp.parse_project()
                docs_meta = self.dm.get_all_parsed() if hasattr(self, 'dm') else {}
                
                # Use AI analysis if available to enhance test generation
                if self.ai_analyzer.use_ai:
                    # Analyze documents with AI for better test generation
                    enhanced_docs = {}
                    for doc_name, doc_content in docs_meta.items():
                        analysis = self.ai_analyzer.analyze_document(doc_content, doc_name)
                        enhanced_docs[doc_name] = {
                            'content': doc_content,
                            'analysis': analysis
                        }
                    # Pass enhanced docs to generator (if generator supports it)
                    docs_meta = enhanced_docs
                
                tg = TestGenerator('data/generated_tests')
                # Cleanup old tests and generate new ones
                tg.generate_tests(functions, docs_meta, cleanup_old=True)
                self.root.after(0, lambda: self.gen_status.config(text="Tests generated!"))
                self.root.after(0, self.refresh_tests)
                self.root.after(0, self.refresh_test_selection)
            except Exception as e:
                self.root.after(0, lambda: self.gen_status.config(text="Generation failed"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Generation failed: {str(e)}"))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def refresh_tests(self):
        self.test_listbox.delete(0, tk.END)
        if os.path.exists('data/generated_tests'):
            files = [f for f in os.listdir('data/generated_tests') if f.endswith('.py')]
            for f in files:
                self.test_listbox.insert(tk.END, f)
    
    def view_test_file(self):
        selections = self.test_listbox.curselection()
        if not selections:
            messagebox.showinfo("Info", "Please select one or more test files to view.\n\nTip: Hold Ctrl (Windows/Linux) or Cmd (Mac) to select multiple files.")
            return
        
        # Get all selected filenames
        selected_files = [self.test_listbox.get(idx) for idx in selections]
        
        if len(selected_files) == 1:
            # Single file - show content
            filename = selected_files[0]
            filepath = os.path.join('data/generated_tests', filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.test_view.delete(1.0, tk.END)
                self.test_view.insert(1.0, f"=== {filename} ===\n\n{content}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
        else:
            # Multiple files - show combined content
            combined_content = f"=== Viewing {len(selected_files)} Test Files ===\n"
            combined_content += "=" * 70 + "\n\n"
            
            for idx, filename in enumerate(selected_files, 1):
                filepath = os.path.join('data/generated_tests', filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    combined_content += f"\n{'='*70}\n"
                    combined_content += f"FILE {idx}/{len(selected_files)}: {filename}\n"
                    combined_content += "=" * 70 + "\n"
                    combined_content += content + "\n\n"
                except Exception as e:
                    combined_content += f"\n{'='*70}\n"
                    combined_content += f"ERROR reading {filename}: {str(e)}\n"
                    combined_content += "=" * 70 + "\n\n"
            
            self.test_view.delete(1.0, tk.END)
            self.test_view.insert(1.0, combined_content)
    
    def delete_test_file(self):
        selections = self.test_listbox.curselection()
        if not selections:
            messagebox.showinfo("Info", "Please select one or more test files to delete.\n\nTip: Hold Ctrl (Windows/Linux) or Cmd (Mac) to select multiple files.")
            return
        
        # Get all selected filenames
        selected_files = [self.test_listbox.get(idx) for idx in selections]
        
        if len(selected_files) == 1:
            confirm_msg = f"Delete test file: {selected_files[0]}?"
        else:
            confirm_msg = f"Delete {len(selected_files)} test files?\n\n" + "\n".join(f"  • {f}" for f in selected_files)
        
        if messagebox.askyesno("Confirm Delete", confirm_msg):
            deleted = []
            failed = []
            
            for filename in selected_files:
                filepath = os.path.join('data/generated_tests', filename)
                try:
                    os.remove(filepath)
                    deleted.append(filename)
                except Exception as e:
                    failed.append(f"{filename}: {str(e)}")
            
            # Refresh the list
            self.refresh_tests()
            self.test_view.delete(1.0, tk.END)
            
            # Show results
            if failed:
                msg = f"Deleted {len(deleted)} file(s) successfully.\n\n"
                msg += f"Failed to delete {len(failed)} file(s):\n" + "\n".join(failed)
                messagebox.showwarning("Partial Success", msg)
            else:
                if len(deleted) == 1:
                    messagebox.showinfo("Success", f"Deleted: {deleted[0]}")
                else:
                    messagebox.showinfo("Success", f"Deleted {len(deleted)} test files successfully.")
    
    # Run tab methods
    def refresh_test_selection(self):
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()
        self.test_checkboxes.clear()
        self.test_vars.clear()
        
        files = self.tr.list_tests()
        for f in files:
            var = tk.BooleanVar(value=True)
            self.test_vars[f] = var
            cb = ttk.Checkbutton(self.checkbox_frame, text=f, variable=var)
            cb.pack(anchor=tk.W, padx=5, pady=2)
            self.test_checkboxes[f] = cb
    
    def select_all_tests(self):
        for var in self.test_vars.values():
            var.set(True)
    
    def deselect_all_tests(self):
        for var in self.test_vars.values():
            var.set(False)
    
    def run_tests(self):
        selected = [f for f, var in self.test_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one test file")
            return
        
        self.run_status.config(text="Running tests...")
        self.progress.start()
        self.error_text.delete(1.0, tk.END)
        self.error_text.insert(1.0, "Running tests...\n")
        
        def run():
            try:
                result = self.tr.run_tests(selected)
                html, xml = result[0], result[1]
                error_info = result[2] if len(result) > 2 else None
                
                # Update UI in main thread
                self.root.after(0, self.progress.stop)
                
                if error_info:
                    # Tests failed - show error details
                    error_msg = f"Tests completed with errors (Exit code: {error_info['returncode']})\n\n"
                    error_msg += "STDOUT:\n" + error_info['stdout'][:2000] + "\n\n"
                    error_msg += "STDERR:\n" + error_info['stderr'][:2000]
                    
                    self.root.after(0, lambda: self.error_text.delete(1.0, tk.END))
                    self.root.after(0, lambda: self.error_text.insert(1.0, error_msg))
                    self.root.after(0, lambda: self.run_status.config(text="Tests completed with errors"))
                    self.root.after(0, lambda: messagebox.showwarning("Tests Completed", 
                        f"Tests finished with exit code {error_info['returncode']}. Check error log for details."))
                else:
                    # Tests passed
                    self.root.after(0, lambda: self.error_text.delete(1.0, tk.END))
                    self.root.after(0, lambda: self.error_text.insert(1.0, "All tests passed successfully!\n"))
                    self.root.after(0, lambda: self.run_status.config(text="Tests completed successfully!"))
                    self.root.after(0, lambda: messagebox.showinfo("Success", "All tests passed! Check reports folder."))
                    
            except Exception as e:
                error_msg = f"Error running tests:\n{str(e)}\n\n"
                self.root.after(0, lambda: self.error_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.error_text.insert(1.0, error_msg))
                self.root.after(0, lambda: self.run_status.config(text="Error occurred"))
                self.root.after(0, self.progress.stop)
                self.root.after(0, lambda: messagebox.showerror("Error", f"Run failed: {str(e)}"))
        
        threading.Thread(target=run, daemon=True).start()
    
    def view_error_log(self):
        log_path = os.path.join('data/reports', 'latest_stdout.txt')
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.error_text.delete(1.0, tk.END)
                self.error_text.insert(1.0, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read log: {str(e)}")
        else:
            messagebox.showinfo("Info", "No error log found. Run tests first.")
    
    def open_html_report(self):
        report_path = os.path.join('data/reports', 'report.html')
        if os.path.exists(report_path):
            webbrowser.open(f'file:///{os.path.abspath(report_path)}')
        else:
            messagebox.showinfo("Info", "No HTML report found. Run tests first.")
    
    def open_xml_report(self):
        report_path = os.path.join('data/reports', 'junit.xml')
        if os.path.exists(report_path):
            webbrowser.open(f'file:///{os.path.abspath(report_path)}')
        else:
            messagebox.showinfo("Info", "No XML report found. Run tests first.")
    
    def open_excel_report(self):
        report_path = os.path.join('data/reports', 'report.xlsx')
        if os.path.exists(report_path):
            try:
                os.startfile(os.path.abspath(report_path))
            except Exception as e:
                 messagebox.showerror("Error", f"Failed to open Excel report: {str(e)}")
        else:
            messagebox.showinfo("Info", "No Excel report found. Run tests first.")
    
    def open_csv_report(self):
        report_path = os.path.join('data/reports', 'report.csv')
        if os.path.exists(report_path):
            try:
                os.startfile(os.path.abspath(report_path))
            except Exception as e:
                 messagebox.showerror("Error", f"Failed to open CSV report: {str(e)}")
        else:
            messagebox.showinfo("Info", "No CSV report found. Run tests first.")
    
    def open_reports_folder(self):
        reports_dir = os.path.abspath('data/reports')
        if os.path.exists(reports_dir):
            os.startfile(reports_dir)
        else:
            messagebox.showinfo("Info", "Reports folder does not exist.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PytestToolGUI(root)
    root.mainloop()


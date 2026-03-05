import os
import subprocess

class TestRunner:
    def __init__(self, tests_dir='data/generated_tests', reports_dir='data/reports'):
        os.makedirs(reports_dir, exist_ok=True)
        self.tests_dir = tests_dir
        self.reports_dir = reports_dir

    def list_tests(self):
        if not os.path.exists(self.tests_dir):
            return []
        return [f for f in os.listdir(self.tests_dir) if f.startswith('test_') and f.endswith('.py')]

    def run_tests(self, selected_files):
        # write pytest incantation
        selected_paths = [os.path.join(self.tests_dir, f) for f in selected_files]
        
        # Verify files exist
        missing_files = [f for f in selected_paths if not os.path.exists(f)]
        if missing_files:
            raise FileNotFoundError(f"Test files not found: {[os.path.basename(f) for f in missing_files]}")

        html_report = os.path.join(self.reports_dir, 'report.html')
        xml_report = os.path.join(self.reports_dir, 'junit.xml')

        # Change to tests directory so pytest can find the files
        original_dir = os.getcwd()
        try:
            # Use absolute paths for reports
            abs_html_report = os.path.abspath(html_report)
            abs_xml_report = os.path.abspath(xml_report)
            
            cmd = [
                'pytest',
                '--tb=short',  # Shorter traceback
                '--disable-warnings',
                f'--html={abs_html_report}',
                f'--junitxml={abs_xml_report}',
                '-o', 'junit_logging=system-out', # Capture stdout to XML
            ] + [os.path.basename(f) for f in selected_paths]

            print('Running', ' '.join(cmd))

            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=self.tests_dir)

            # Save logs
            log_dir = os.path.abspath(self.reports_dir)
            with open(os.path.join(log_dir, 'latest_stdout.txt'), 'w', encoding='utf-8') as f:
                f.write(proc.stdout)
            with open(os.path.join(log_dir, 'latest_stderr.txt'), 'w', encoding='utf-8') as f:
                f.write(proc.stderr)
            
            # Generate Reports
            try:
                self.generate_csv_report(xml_report)
                self.generate_excel_report(xml_report)
            except Exception as e:
                print(f"Failed to generate reports: {e}")

            # Return error info if tests failed
            error_info = None
            if proc.returncode != 0:
                error_info = {
                    'returncode': proc.returncode,
                    'stdout': proc.stdout,
                    'stderr': proc.stderr
                }

            return (html_report, xml_report, error_info)
        finally:
            os.chdir(original_dir)

    def generate_csv_report(self, xml_path):
        import csv
        import xml.etree.ElementTree as ET
        
        report_data = []
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            for testcase in root.iter('testcase'):
                # name usually format: test_function_scenario
                name = testcase.get('name')
                
                # extract function name from test name (test_FUNC_scenario)
                parts = name.split('_')
                if len(parts) >= 3:
                    # Remove test_ prefix and scenario suffix
                    # Assumption: test_funcname_scenario
                    func_name = '_'.join(parts[1:-1]) 
                    scenario = parts[-1]
                else:
                    func_name = name
                    scenario = "General"
                
                # Check status
                failure = testcase.find('failure')
                error = testcase.find('error')
                skipped = testcase.find('skipped')
                
                status = "Pass"
                if failure is not None: status = "Fail"
                elif error is not None: status = "Error"
                elif skipped is not None: status = "Skipped"
                
                # Get steps from system-out
                sys_out = testcase.find('system-out')
                steps = []
                if sys_out is not None and sys_out.text:
                    for line in sys_out.text.splitlines():
                        if "STEP:" in line:
                            steps.append(line.split("STEP:")[1].strip())
                
                # Default steps if missing or if it was skipped/error before printing
                if not steps:
                    if status == "Skipped":
                        steps = ["Test Skipped"]
                    else:
                        steps = ["Execution"]
                    
                # Add rows
                for i, step in enumerate(steps):
                    step_status = "Pass"
                    if status in ["Fail", "Error"]:
                        # If test failed, the last recorded step likely failed or the assertion after it
                        # Since we only print "STEP: ..." before doing the work,
                        # if the test failed, it failed during or after one of these steps.
                        # Simple logic: All Pass except the last one if the test failed.
                        # However, if we have 3 steps and it failed, maybe it failed at step 2.
                        # But we print STEP 1, do work, print STEP 2, do work.
                        # If it fails at step 2 work, we see STEP 1 and STEP 2 in stdout.
                        # So STEP 2 is the one that failed.
                        if i == len(steps) - 1:
                            step_status = status
                    elif status == "Skipped":
                        step_status = "Skipped"
                    
                    report_data.append([func_name, f"{scenario} - {name}", step, step_status])
            
            # Write CSV
            csv_path = os.path.join(self.reports_dir, 'report.csv')
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Function Name', 'Test Case', 'Test Step', 'Status'])
                writer.writerows(report_data)
                print(f"CSV Report generated at: {csv_path}")
                
        except Exception as e:
            print(f"Error parsing JUnit XML for CSV: {e}")

    def generate_excel_report(self, xml_path):
        """Generate Excel report from JUnit XML using pandas"""
        import xml.etree.ElementTree as ET
        try:
            import pandas as pd
        except ImportError:
            print("pandas not installed. Skipping Excel report.")
            return

        report_data = []
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            for testcase in root.iter('testcase'):
                name = testcase.get('name')
                parts = name.split('_')
                if len(parts) >= 3:
                    func_name = '_'.join(parts[1:-1]) 
                    scenario = parts[-1]
                else:
                    func_name = name
                    scenario = "General"
                
                failure = testcase.find('failure')
                error = testcase.find('error')
                skipped = testcase.find('skipped')
                
                status = "Pass"
                if failure is not None: status = "Fail"
                elif error is not None: status = "Error"
                elif skipped is not None: status = "Skipped"
                
                sys_out = testcase.find('system-out')
                steps = []
                if sys_out is not None and sys_out.text:
                    for line in sys_out.text.splitlines():
                        if "STEP:" in line:
                            steps.append(line.split("STEP:")[1].strip())
                
                if not steps:
                    steps = ["Execution"]
                    
                for i, step in enumerate(steps):
                    step_status = "Pass"
                    if status in ["Fail", "Error"]:
                        if i == len(steps) - 1:
                            step_status = status
                    elif status == "Skipped":
                        step_status = "Skipped"
                    
                    report_data.append({
                        'Function Name': func_name,
                        'Test Case': f"{scenario} - {name}",
                        'Test Step': step,
                        'Status': step_status
                    })
            
            if report_data:
                df = pd.DataFrame(report_data)
                excel_path = os.path.join(self.reports_dir, 'report.xlsx')
                df.to_excel(excel_path, index=False)
                print(f"Excel Report generated at: {excel_path}")
                
        except Exception as e:
            print(f"Error generating Excel report: {e}")

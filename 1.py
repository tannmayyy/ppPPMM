import subprocess
import re
import streamlit as st
import webbrowser

def get_sso_url_via_subprocess():
    try:
        # Use SnowSQL CLI with dummy query to trigger the login
        result = subprocess.run(
            [
                "snowsql",
                "-a", "your_account",
                "-u", "your_email",
                "--authenticator", "externalbrowser",
                "-q", "SELECT 1;"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            input="\n"
        )
        
        # Catch the URL from stdout
        match = re.search(r"Going to open:\s+(https?://\S+)", result.stderr)
        if match:
            return match.group(1)
        else:
            st.error("Unable to extract SSO URL.")
            return None
    except Exception as e:
        st.error(f"Error during SSO subprocess: {e}")
        return None
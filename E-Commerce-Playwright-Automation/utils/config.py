import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Ensure directories exist
SCREENSHOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

class Config:
    """Central configuration for test automation suite."""
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    
    # Credentials
    STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_OUT_USER = os.getenv("LOCKED_OUT_USER", "locked_out_user")
    PROBLEM_USER = os.getenv("PROBLEM_USER", "problem_user")
    PERFORMANCE_GLITCH_USER = os.getenv("PERFORMANCE_GLITCH_USER", "performance_glitch_user")
    PASSWORD = os.getenv("PASSWORD", "secret_sauce")
    INVALID_PASSWORD = "invalid_password_123"
    INVALID_USERNAME = "invalid_user_xyz"

    # Default Timeouts (in ms)
    DEFAULT_TIMEOUT = 10000
    NAVIGATION_TIMEOUT = 30000

    # Checkout Test Data
    DEFAULT_FIRST_NAME = "John"
    DEFAULT_LAST_NAME = "Doe"
    DEFAULT_POSTAL_CODE = "90210"
